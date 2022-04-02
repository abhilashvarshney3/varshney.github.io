from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth.models import User


from django.urls import reverse

from django.contrib.auth.decorators import login_required

# Create your views here.
from post.models import Post, Stream, Tag, Likes, PostFileContent, Follow
from authy.models import Profile
from post.forms import NewPostForm
from comment.models import Comment
from comment.forms import CommentForm

@login_required
def index(request):
    user = request.user
    posts = Stream.objects.filter(user=user)

    group_ids = []

    for post in posts:
        group_ids.append(post.post_id)

    post_items = Post.objects.filter(id__in=group_ids).all().order_by('-posted')
    random_users = User.objects.order_by('?')[:4]

    template = loader.get_template('index.html')

    context = {
        'post_items': post_items,
        'random_users': random_users,
    }

    return HttpResponse(template.render(context, request))


    


@login_required

def NewPost(request,):
    user = request.user
    tags_objs = []
    files_objs = []
    
    if request.method == "POST":
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('content')
            caption = form.cleaned_data.get('caption')
            tags_form = form.cleaned_data.get('tags')
            
            tags_list = list(tags_form.split(','))
            
            for tag in tags_list:
                t, created = Tag.objects.get_or_create(title=tag)
                tags_objs.append(t)
                
            for file in files:
                file_instance = PostFileContent(file=file, user=user)
                file_instance.save()
                files_objs.append(file_instance)
                
            p, created = Post.objects.get_or_create(caption=caption, user=user)
            p.tags.set(tags_objs)
            p.content.set(files_objs)
            p.save()
            return HttpResponseRedirect(reverse( 'profile',  args=[request.user]))
            #return redirect('index')
        
    else:
            form = NewPostForm()
            
    context = {
            'form': form,
        }    
        
    return render(request, 'newpost.html', context)

@login_required

def PostDetails(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user=request.user
    favorited = False
    liked = False
    
    comments = Comment.objects.filter(post=post).order_by('date')
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = user
            comment.save()
            return HttpResponseRedirect(reverse('postdetails', args=[post_id]))
    else:
        form = CommentForm()
            
    
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        
        if profile.favorites.filter(id=post_id).exists():
            favorited = True
            
    if request.user.is_authenticated:
        post = Post.objects.get(id=post_id)
       
        if Likes.objects.filter(user=user, post=post).count():
            liked = True
    
    template = loader.get_template('post_detail.html')
    
    context = {
        'post': post,
        'liked': liked,
        'favorited': favorited,
        'form': form,
        'comments': comments,
        
    }
    
    return HttpResponse(template.render(context, request))
    

@login_required
def tags(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags=tag).order_by('-posted')
    
    template = loader.get_template('tag.html')
    
    context = {
        'posts': posts,
        'tag': tag,
    }
    
    return HttpResponse(template.render(context, request))



@login_required
def search(request):
    query = request.GET['query']
    #posts = Post.objects.all()
    posts = Post.objects.filter(Q(user__username__icontains=query)|Q(tags__slug__icontains=query)).order_by('-posted')
    params = {'posts': posts}
    return render(request, 'search_tag.html', params)

@login_required
def like(request, post_id):
    user=request.user
    post = Post.objects.get(id=post_id)
    current_likes = post.likes
    
    liked = Likes.objects.filter(user=user, post=post).count()
    
    if not liked:
        like = Likes.objects.create(user=user, post=post)        
        current_likes = current_likes + 1
        
    else:
        Likes.objects.filter(user=user, post=post).delete()
        current_likes = current_likes - 1
        
    post.likes = current_likes
    post.save()
    

    return HttpResponseRedirect(reverse('postdetails', args=[post_id]))
    
@login_required
def favorite(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    profile = Profile.objects.get(user=user)
    
    if profile.favorites.filter(id=post_id).exists():
        profile.favorites.remove(post)
        
    else:
        profile.favorites.add(post)
        
    return HttpResponseRedirect(reverse('postdetails', args=[post_id]))



@login_required
def deletepost(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    profile = Profile.objects.get(user=user)
    
    Post.objects.filter(user=user, id=post_id).delete()
    
    return HttpResponseRedirect(reverse( 'profile',  args=[request.user]))
    
