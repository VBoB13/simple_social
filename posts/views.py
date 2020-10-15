from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import generic, View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from .models import Post, Comment
from . import forms

# Create your views here.

class IndexView(generic.ListView):
    paginate_by = 5
    template_name = 'posts/index.html'
    context_object_name = 'posts'
    queryset = Post.objects.all().select_related("user")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = "Posts"
        return context   


class PostDetailView(generic.DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_title"] = "{}".format(self.object)
        context["comment_form"] = forms.CommentForm()
        context["comments"] = self.object.comment_set.all().select_related("user")
        return context


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    login_url = "posts/login/"
    redirect_field_name = "posts/post_form.html"

    model = Post
    form_class = forms.PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_title"] = "Create Post"
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    login_url = "posts/login/"
    redirect_field_name = "posts/post_form.html"

    model = Post
    form_class = forms.PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_title"] = "Update Post"
        return context


class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
    login_url = "posts/login/"
    redirect_field_name = "post/post_confirm_delete.html"

    model = Post
    success_url = reverse_lazy('posts:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_title"] = "Delete: {}".format(self.object)
        return context


@login_required
def create_comment(request, **kwargs):
    post_pk = kwargs.pop('pk')
    if request.method == "POST":
        comment_form = forms.CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            post = get_object_or_404(Post, pk=post_pk)
            comment.post = post
            
            comment.save()
        else:
            print(comment_form.errors)
    
    return HttpResponseRedirect(reverse('posts:post_detail',
                                        kwargs={"pk":post_pk}))

def register(request):
    registered = False

    if request.method == "POST":
        user_form = forms.UserForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = forms.UserForm()

    return render(request, 'posts/register.html',
                {'user_form': user_form,
                   'registered': registered,
                   'view_title': 'Register'})


@login_required
def posts_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('posts:index'))

def posts_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('posts:index'))

            else:
                return HttpResponse("Account Not Active")
        else:
            print("Someone tried to login and failed!")
            print("Username: {} and password: {}".format(username, password))
            return HttpResponse("Invalid login details supplied!")
    else:
        return render(request, 'posts/login.html', {})
