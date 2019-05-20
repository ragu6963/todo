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
        if sort_filter == "all": # 모든 항목
            posts = Post.objects.all()
        elif sort_filter =="confirm": # 완료된 항목
            posts = Post.objects.filter(confirm=True)
        elif sort_filter =="un_confirm": # 미완료 항목
            posts = Post.objects.filter(confirm=False)
        elif sort_filter =="end_post": # 마감날짜 지난 항목들 filter
            post = Post.objects.all()
            posts = [] 
            for p in post:
                if p.end_at != None: # 마감날짜 성정 학목들 중에서
                    time = p.end_at+timedelta(days=1) - datetime.now()
                    if time.days < 0: # 마감날짜가 지난 항목들 list에 append
                        posts.append(p)  

            context={'posts':posts} 
            return render(request, 'index.html', context) 
        else: # 우선순위 혹은 마감날짜, 내림차순 오름차순
            posts = Post.objects.order_by(sort_filter) 

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
        post = Post()
        post.title = request.POST['title']
        post.content = request.POST['content']
        post.priority = request.POST['priority'] 
        try:
            post.end_at = request.POST['end_at'] # 마감날짜 설정시
        except:
            post.end_at = None # 마감날짜 미설정시
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
            post = Post.objects.get(id = post_id) # 읽고있는 post table 불러오기
            context={
                "post":post,
            }
            return render(request, 'update.html',context)

def delete(request): 
    if request.method == "POST":
        post_id = request.POST['post_id'] # 읽고있는 post table 불러오기
        post = Post.objects.get(id = post_id) 
        post.delete() # table delete
        return redirect('main')

def confirm(request):
    if request.method == "POST":
        post_id = request.POST['post_id']
        post = Post.objects.get(id = post_id) 
        confirm_stat = post.confirm # 현재 post confirm 상태 저장
        post.confirm = not(confirm_stat) # 현재 post confirm 반대 값 저장
        post.save()  
        return redirect('main')

def calendar(request):
    
    return render(request,'calendar.html')
