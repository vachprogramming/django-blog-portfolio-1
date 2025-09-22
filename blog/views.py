from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .models import Post, Comment
from .forms import CommentForm
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q 


class PostListView(ListView):
    """
    View to display a list of all posts.
    """
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts' # Name of the object list in the template
    ordering = ['-created_at']    # Order posts by creation date, newest first
    paginate_by = 3 # Add this line to limit posts per page to 3

    def get_queryset(self):
        """
        Override the default queryset to filter by search query if it exists.
        """
        query = self.request.GET.get('q')
        if query:
            # Filter posts where the title OR content contains the query (case-insensitive)
            return Post.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            ).order_by('-created_at')
        return Post.objects.order_by('-created_at')


class PostDetailView(DetailView):
    """
    View to display the details of a single post and handle comments.
    """
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        """Add comment form to the context."""
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        """Handle POST requests for comment submission."""
        self.object = self.get_object() # Get the post object
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = request.user
            comment.save()
            return redirect('post-detail', pk=self.object.pk)
        else:
            # If form is not valid, re-render the page with the form and errors
            context = self.get_context_data()
            context['comment_form'] = form
            return self.render_to_response(context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content'] # Fields the user can fill out
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post-list') # Where to redirect after success

    def form_valid(self, form):
        """
        This method is called when valid form data has been POSTed.
        It should return an HttpResponse.
        """
        form.instance.author = self.request.user # Set author to current user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        """
        Prevent a user from updating other people's posts.
        """
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        """
        Prevent a user from deleting other people's posts.
        """
        post = self.get_object()
        return self.request.user == post.author

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login') # Redirect to login page after successful sign up
    template_name = 'registration/signup.html'    