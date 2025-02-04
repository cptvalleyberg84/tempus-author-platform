from django.views.generic import ListView, DetailView
from .models import Post
from django.shortcuts import redirect
from django.contrib import messages
from .forms import CommentForm


class BlogListView(ListView):
    model = Post
    template_name = 'blog/blog.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        return Post.objects.filter(post_status=1).order_by('-post_created_on')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Blog'
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    slug_url_kwarg = 'slug'
    slug_field = 'post_slug'

    def get_queryset(self):
        return Post.objects.filter(post_status=1)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(active=True)
        if self.request.user.is_authenticated:
            context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
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
