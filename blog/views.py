from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Post, Comment
from .forms import CommentForm


class StartingPage(ListView):
    template_name = "blog/index.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"

    def get_queryset(self):
        query_set = super().get_queryset()
        data = query_set[:3]
        return data

# def starting_page(request):
#     latest_posts = Post.objects.all().order_by("-date")[:3]
#     return render(request, 'blog/index.html', {
#         "posts": latest_posts
#     })


class AllPosts(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "all_posts"

# def posts(request):
#     all_posts = Post.objects.all().order_by("-date")
#     return render(request, "blog/all-posts.html", {
#         "all_posts": all_posts
#     })


class PostDetail(View):
    def is_stored_post(self, request, post_id):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later = False
        return is_saved_for_later
    
    def get(self, request, slug):
        ident_post = Post.objects.get(slug=slug)
        
        context = {
            "post": ident_post,
            "post_tags": ident_post.tag.all(),
            "comment": CommentForm(),
            "all_comments": ident_post.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_post(request, ident_post.id),
        }
        return render(request, "blog/post-detail.html", context)

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        ident_post = Post.objects.get(slug=slug)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = ident_post
            comment.save()
            return HttpResponseRedirect(reverse("post_detail_page", args=[slug]))

        context = {
            "post": ident_post,
            "post_tags": ident_post.tag.all(),
            "comment": comment_form,
            "all_comments": ident_post.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_post(request, ident_post.id),
        }
        return render(request, "blog/post-detail.html", context)

# class PostDetail(DetailView):
    # template_name = "blog/post-detail.html"
    # model = Post

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["post_tags"] = self.object.tag.all()
    #     context["comment"] = CommentForm()
    #     return context

# def post_detail(request, slug):
#     identified_post = get_object_or_404(Post, slug=slug)
#     return render(request, "blog/post-detail.html", {
#         "post": identified_post,
#         "post_tags": identified_post.tag.all()
#     })


class ReadLaterView(View):
    def get(self, request):
        stored_posts = request.session.get("stored_posts")
        context = {}

        if stored_posts is None or len(stored_posts) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            context["posts"] = posts
            context["has_posts"] = True

        return render(request, "blog/stored-posts.html", context)

    def post(self, request):
        post_id = int(request.POST["post_id"])
        ident_post = Post.objects.get(id=post_id)
        stored_posts = request.session.get("stored_posts")
        if stored_posts is None:
            stored_posts = []

        if post_id not in stored_posts:
            stored_posts.append(post_id)
            request.session["stored_posts"] = stored_posts
            return HttpResponseRedirect(reverse("post_detail_page", args=[ident_post.slug]))

        else:
            stored_posts.remove(post_id)
            request.session["stored_posts"] = stored_posts
            return HttpResponseRedirect(reverse("post_detail_page", args=[ident_post.slug]))
