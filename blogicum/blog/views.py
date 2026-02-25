from django.shortcuts import render, get_object_or_404
from blog.models import Post, Category
from django.utils import timezone


def index(request):
    post_list = {'post_list': Post.objects.select_related(
        'category'
        ).filter(
            is_published=True
            ).filter(
                created_at__lte=timezone.now()
                ).filter(category__is_published=True)[0:5]}
    return render(request, 'blog/index.html', post_list)


def post_detail(request, id):
    template_name = 'blog/detail.html'
    post = get_object_or_404(Post, pk=id)
    context = {'post': post}
    return render(request, template_name, context)


def category_posts(request, category_slug):
    template_name = 'blog/category.html'
    category = get_object_or_404(Category, slug=category_slug, is_published=True)
    post_list = Post.objects.select_related('category', 'location', 
                                            'author').filter(category=category, 
                                                             is_published=True, 
                                                             pub_date__lte=timezone.now())
    context = {
        'category': category,
        'post_list': post_list
    }
    return render(request, template_name, context)
