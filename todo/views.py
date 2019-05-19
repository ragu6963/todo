from django.shortcuts import render, redirect  
from .models import Post
from datetime import datetime, timedelta


def main(request):
    posts = Post.objects.all()
    context = {
        'posts':posts, 
    }
    return render(request, 'main.html', context) 

def index(request):
    if request.is_ajax():
        sort_filter = request.GET['sort_filter']
        if sort_filter == "all":
            posts = Post.objects.all()
        elif sort_filter =="confirm":
            posts = Post.objects.filter(confirm=True)
        elif sort_filter =="un_confirm":
            posts = Post.objects.filter(confirm=False)
        elif sort_filter =="end_post":
            post = Post.objects.all()
            posts = [] 
            for p in post:
                if p.end_at != None:
                    time = p.end_at+timedelta(days=1) - datetime.now()
                    if time.days < 0:
                        posts.append(p)   
            context={'posts':posts} 
            return render(request, 'index.html', context)

        else:
            posts = Post.objects.order_by(sort_filter) 

        context = {
            'posts': posts,
        }
        return render(request, 'index.html', context) 

    else:  
        posts = Post.objects.all()
        context = { 
            'posts': posts, 
        }
        return render(request, 'index.html', context) 

def read(request):
    post_id = request.GET['post_id']
    post = Post.objects.get(id=post_id)
    context={
        "post":post,
    }
    return render(request, 'read.html',context)

def create(request):
    if request.method == "POST": 
        now = datetime.now()
        post = Post()
        post.title = request.POST['title']
        post.content = request.POST['content']
        post.priority = request.POST['priority'] 
        try:
            post.end_at = request.POST['end_at']
        except:
            post.end_at = None
        post.save()
        return redirect('main')   
    else: 
        if request.is_ajax(): 
            return render(request, 'create.html')
        else:
            return render(request, 'create.html')

def update(request):
    if request.method == "POST": 
        post_id = request.POST['post_id']
        post = Post.objects.get(id = post_id)
        post.title = request.POST['title']
        post.content = request.POST['content']
        post.priority = request.POST['priority'] 
        try:
            post.end_at = request.POST['end_at']
        except:
            post.end_at = None
        post.save()
        return redirect('main')
    else:
        if request.is_ajax(): 
            post_id = request.GET['post_id']
            post = Post.objects.get(id = post_id)
            context={
                "post":post,
            }
            return render(request, 'update.html',context)

def delete(request): 
    if request.method == "POST":
        post_id = request.POST['post_id']
        post = Post.objects.get(id = post_id) 
        post.delete() 
        return redirect('main')

def confirm(request):
    if request.method == "POST":
        post_id = request.POST['post_id']
        post = Post.objects.get(id = post_id) 
        confirm_stat = post.confirm
        post.confirm = not(confirm_stat)
        post.save()  
        return redirect('main')

def calendar(request):
    
    return render(request,'calendar.html')
