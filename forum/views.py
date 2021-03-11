from django.contrib import auth, messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic

from forum.form import EditProfileForm, ProfileForm
from forum.models import Blog, Profile


def index(request):
    return render(request, 'forum/index.html')


def signup(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['conf_password']:
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'registration/signup.html',
                              {'error': 'Username Unavailable! '
                                        'PLease Try a Different Username!'})
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
            return render(request, 'registration/login.html',
                          {'error': 'Invalid Username or Password!'})
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


@login_required()
def profile_edit(request):
    profile = get_object_or_404(Profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save()
            # profile.customer = profile.id
            profile.updated_date = timezone.now()
            profile.save()
            return render(request, 'forum/index.html')
    else:
        form = ProfileForm(instance=profile)
        return render(request, 'forum/profile_edit.html', {'form': form})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form
    })


def blogs(request):
    post = Blog.objects
    return render(request, 'forum/blogs.html', {'post': post})


def detail(request, blogs_id):
    post_detail = get_object_or_404(Blog, pk=blogs_id)
    return render(request, 'forum/detail.html', {'post_detail': post_detail})
