import braintree
from django.conf import settings
from django.contrib import auth, messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

# import weasyprint

# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views import generic
from django.views.decorators.http import require_POST

from forum.cart import Cart
from forum.form import EditProfileForm, CartAddProductForm, OrderCreateForm
from forum.models import Product, Category, Order, OrderItem


def index(request):
    return render(request, 'forum/index.html')


def signup(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['conf_password']:
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'registration/signup.html',
                              {'error': 'Username Unavailable! '
                                        'PLease Try a Different Username '
                                        'or Proceed to Log In!'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'],
                                                password=request.POST['password'],
                                                first_name=request.POST['first_name'],
                                                last_name=request.POST['last_name'],
                                                email=request.POST['email'])
                auth.login(request, user)
                return redirect('edit_profile')
        else:
            return render(request, 'registration/signup.html',
                          {'error': 'Please Check for Matching Password and Try Again!'})
    else:
        return render(request, 'registration/signup.html')


def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'],
                                 password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            return render(request, 'registration/login.html')
    else:
        return render(request, 'registration/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('index')


class UserEditView(generic.UpdateView):
    form_class = EditProfileForm
    template_name = 'forum/edit_profile.html'
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        return self.request.user


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form
    })


@login_required()
def user_list(request):
    users = User.objects
    return render(request, 'forum/user_list.html', {'users': users})


@staff_member_required
def edit_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
        if request.method == 'POST':
            form = EditProfileForm(request.POST, instance=user)
            if form.is_valid():
                customer = form.save(commit=False)
                customer.updated_date = timezone.now()
                customer.save()
                return redirect('user_list')
        else:
            form = EditProfileForm(instance=user)
            return render(request, 'forum/user_list.html', {'form': form})
            # return redirect('crm:customer_list')
    except User.DoesNotExist:
        return render(request, 'forum/user_list.html')


@staff_member_required
def del_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
        user.delete()
        return redirect('user_list')
    except User.DoesNotExist:
        return redirect('forum/user_list.html')


@staff_member_required
def upgrade_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
        user.is_staff = True
        user.save()
        return redirect('user_list')
    except User.DoesNotExist:
        return redirect('forum/user_list.html')


@staff_member_required
def downgrade_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
        user.is_staff = False
        user.save()
        return redirect('user_list')
    except User.DoesNotExist:
        return redirect('forum/user_list.html')


@staff_member_required
def suspend_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
        user.is_active = False
        user.save()
        return redirect('user_list')
    except User.DoesNotExist:
        return redirect('forum/user_list.html')


@staff_member_required
def activate_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
        user.is_active = True
        user.save()
        return redirect('user_list')
    except User.DoesNotExist:
        return redirect('forum/user_list.html')


# Product views start

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'forum/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    return render(request,
                  'forum/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})


# cart views


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'],
                     'update': True})
    return render(request, 'forum/cart/detail.html', {'cart': cart})


# order views


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('forum/order/pdf.html',
                            {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=\
        "order_{}.pdf"'.format(order.id)
    import weasyprint
    weasyprint.HTML(string=html).write_pdf(response,
                                           stylesheets=[weasyprint.CSS(
                                               settings.STATIC_ROOT + 'css/pdf.css')])
    return response


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'forum/admin/order/detail.html',
                  {'order': order})


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # clear the cart
            cart.clear()
            # set the order in the session
            request.session['order_id'] = order.id
            # redirect for payment
            return redirect(reverse('process'))

    else:
        form = OrderCreateForm()
    return render(request,
                  'forum/order/create.html',
                  {'cart': cart, 'form': form})


# payment views


def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        # retrieve nonce
        nonce = request.POST.get('payment_method_nonce', None)
        # create and submit transaction
        result = braintree.Transaction.sale({
            'amount': '{:.2f}'.format(order.get_total_cost()),
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True
            }
        })
        if result.is_success:
            # mark the order as paid
            order.paid = True
            # store the unique transaction id
            order.braintree_id = result.transaction.id
            order.save()
            # create invoice e-mail
            subject = 'Fun for Kids Store - Invoice no. {}'.format(order.id)
            message = 'Thank you for shopping at Fun for Kids. Your total bill card to CC is.'
            email = EmailMessage(subject,
                                 message,
                                 'admin@myshop.com',
                                 [order.email])
            # generate PDF
#            html = render_to_string('orders/order/pdf.html', {'order': order})
#            out = BytesIO()
#            stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
#            weasyprint.HTML(string=html).write_pdf(out,
#                                                  stylesheets=stylesheets)
            # attach PDF file
#            email.attach('order_{}.pdf'.format(order.id),
#                         out.getvalue(),
#                         'application/pdf')
            # send e-mail
            email.send()
            return redirect('done')
        else:
            return redirect('canceled')
    else:
        # generate token
        client_token = braintree.ClientToken.generate()
        return render(request,
                      'forum/payment/process.html',
                      {'order': order,
                       'client_token': client_token})


def payment_done(request):
    return render(request, 'forum/payment/done.html')


def payment_canceled(request):
    return render(request, 'forum/payment/canceled.html')
