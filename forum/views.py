from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils import timezone

from .models import Threads, Comments
from .forms import ThreadForm, CommentForm
# Create your views here.


def threads(request):
    all_thread = Threads.objects.all()
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            new_thread = Threads(
                subject=form.cleaned_data['subject'],
                creator=request.user,
                creation_date=timezone.now()
                )
            new_thread.save()
            messages.success(request, f'New Thread created')
            return redirect('threads')
    else:
        form =ThreadForm()
    return render(request, 'forum_threads.html', {'threads': all_thread, 'form':form})


def thread(request, id):
    comments = Comments.objects.filter(thread_id=id)
    thr=Threads.objects.get(id=id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_com = Comments(
                comment=form.cleaned_data['comment'],
                user = request.user,
                thread=thr,
                pub_date = timezone.now()
                )
            new_com.save()
            messages.success(request, f'Comment added')
            return redirect('thread', id)
        else:
            messages.warning(request, f'Sorry we cannot add your your comment')
    else:
        form = CommentForm()
    return render(request, 'forum_comment.html', {'comments': comments, 'form':form,
                                             'thread':thr})


def delete_com(request, id):
    old_com = Comments.objects.get(id=id)
    old_com.delete()
    messages.warning(request, f'Comment deleted')
    return redirect('threads')


def delete_thread(request, id):
    old_thr = Threads.objects.get(id=id)
    old_thr.delete()
    messages.warning(request, f'Thread deleted')
    return redirect('threads')