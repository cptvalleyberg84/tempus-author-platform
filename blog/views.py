from django.http import HttpResponseForbidden
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Comment
from .forms import CommentForm


class BlogListView(ListView):
    """
    View for displaying a paginated list of published blog posts.
    """
    model = Post
    template_name = 'blog/blog.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        """
        Returns queryset of published posts ordered by creation date.
        """
        return Post.objects.filter(post_status=1).order_by('-post_created_on')

    def get_context_data(self, **kwargs):
        """
        Adds title to the context data.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Blog'
        return context


class PostDetailView(DetailView):
    """
    View for displaying a single blog post with its comments.
    """
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    slug_url_kwarg = 'slug'
    slug_field = 'post_slug'

    def get_queryset(self):
        """
        Returns queryset of published posts only.
        """
        return Post.objects.filter(post_status=1)

    def get_context_data(self, **kwargs):
        """
        Adds comments and comment form to the context data.
        """
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(active=True)
        if self.request.user.is_authenticated:
            context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        """
        Handles comment submission on a blog post.
        """
        self.object = self.get_object()
        if not request.user.is_authenticated:
            messages.error(request, 'Please log in to comment.')
            return redirect('login')

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been posted.')
            return redirect('post_detail', slug=self.object.post_slug)

        context = self.get_context_data(object=self.object)
        context['comment_form'] = form
        return self.render_to_response(context)


@login_required
def comment_edit(request, post_slug, comment_id):
    """
    View for editing an existing comment.
    """
    comment = get_object_or_404(
        Comment, id=comment_id, post__post_slug=post_slug)

    if not request.user == comment.author:
        return HttpResponseForbidden(
            "You don't have permission to edit this comment."
        )

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comment updated successfully.')
            return redirect('post_detail', slug=post_slug)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'blog/comment_edit.html', {
        'form': form,
        'comment': comment,
        'post': comment.post
    })


@login_required
def comment_delete(request, post_slug, comment_id):
    """
    View for deleting an existing comment.
    """
    comment = get_object_or_404(
        Comment, id=comment_id, post__post_slug=post_slug)

    if not (request.user == comment.author or request.user.is_staff):
        return HttpResponseForbidden(
            "You don't have permission to delete this comment."
        )

    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Comment deleted successfully.')

    return redirect('post_detail', slug=post_slug)
