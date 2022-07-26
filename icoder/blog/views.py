from re import template
from django.shortcuts import render, HttpResponse, redirect
from blog.models import Post, BlogComment
from django.contrib import messages
from .forms import PostCreate, UserPost
from django.contrib.auth import authenticate
from django.http import JsonResponse
# Create your views here.
def blogHome(request): 
    allPosts= Post.objects.all()
    context={'allPosts': allPosts,}
    return render(request, "blog/blogHome.html", context)

def blogPost(request, slug): 
    post=Post.objects.filter(slug=slug).first()
    comments= BlogComment.objects.filter(post=post, parent=None)
    replies= BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict={}
    for reply in replies:
        if reply.parent.id not in replyDict.keys():
            replyDict[reply.parent.id]=[reply]
        else:
            replyDict[reply.parent.id].append(reply)

    context={'post':post, 'comments': comments, 'user': request.user, 'replyDict': replyDict}
    return render(request, "blog/blogPost.html", context)

def postComment(request):
    if request.method == "POST":
        comment=request.POST.get('comment')
        user=request.user
        post_id =request.POST.get('postid')
        post= Post.objects.get(id=post_id)
        parentid= request.POST.get('parentid')
        if parentid=="":
            comment=BlogComment(comment= comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully")
        else:
            parent= BlogComment.objects.get(id=parentid)
            comment=BlogComment(comment= comment, user=user, post=post , parent=parent)
            comment.save()
            messages.success(request, "Your reply has been posted successfully")
        
    return redirect(f"/blog/{post.slug}")



def upload(request):
    if request.user.is_authenticated:
        form = UserPost()
        notes = Post.objects.filter(user = request.user ).order_by('-id')
        data ={
            'form':form,
            'notes':notes
        }
        if request.method=="POST":
            title = request.POST.get('title')
            slug = request.POST.get('slug')
            content = request.POST.get('content')
            img = request.POST.get('img')

            note = Post()
            note.title =  title
            note.slug = slug
            note.content = content
            note.img = img
            note.user = request.user
            note.save()
            notes = Post.objects.values().filter(user=request.user).order_by('-id')
            user_notes = list(notes)
            return JsonResponse({"status":"1","status_message":"Your Note Added Successfully","notes":user_notes})

        return render(request, template_name='blog/upload_form.html',context = data)
    else:
        return redirect('home')



"""
below code is for blogpost page
"""
def update_post(request, post_id):
    post_id = int(post_id)
    try:
        post_sel = Post.objects.get(id = post_id)
    except Post.DoesNotExist:
        return redirect('bloghome')
    post_form = UserPost(request.POST or None, instance = post_sel)
    if post_form.is_valid():
       post_form.save()
       return redirect('bloghome')
    return render(request, 'blog/upload_form.html', {'upload_form':post_form})

def delete_post(request, post_id):
    post_id = int(post_id)
    try:
        post_sel = Post.objects.get(id = post_id)
    except Post.DoesNotExist:
        return redirect('bloghome')
    post_sel.delete()
    return redirect('bloghome')

"""
below is for user upload page
"""
def edit_note (request):
    edit_id = request.POST.get('edit_id')
    title = request.POST.get('title')
    slug = request.POST.get('slug')
    content = request.POST.get('content')
    Post.objects.filter(id = edit_id ).update(title = title, slug = slug, content = content)
    notes = Post.objects.values().filter(user=request.user).order_by('-id')
    user_notes = list(notes)
    return JsonResponse({"status":"1","status_message":"Your Note Updated Successfully","notes":user_notes})

def delete_note(request):
    delete_id = request.GET.get('delete_id')
    Post.objects.filter(id=delete_id).first().delete()
    notes = Post.objects.values().filter(user=request.user).order_by('-id')
    user_notes = list(notes)
    return JsonResponse({"status":"1","status_message":"Your Note Deleted Successfully","notes":user_notes})
