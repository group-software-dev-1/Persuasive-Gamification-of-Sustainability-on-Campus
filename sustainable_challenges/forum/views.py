from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from .models import Annoucement, Suggestion, Comment
from .forms import PostForm, CommentForm, AnnounceForm
# Create your views here.

def forum(request):
    suggestions = Suggestion.objects.order_by("post_date")
    annoucements = Annoucement.objects.filter(active=True).order_by("post_date")
    if request.method == "POST":
        obj = request.POST.get('delete')
        obj.delete()
    return render(request, "forum.html", {"suggestions": suggestions,
                                          'announcements': annoucements,
                                          "is_staff": request.user.is_staff})

def post(request):
    posted = False
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            obj = Suggestion(post_name=form.cleaned_data['title'], post_text=form.cleaned_data['text'], poster=request.user)
            obj.save()
            return HttpResponseRedirect(f'/forum/post?posted=True')
    else:
        form = PostForm()
        if 'posted' in request.GET:
            posted = True

    return render(request, 'post.html', {"form": form, 
                                         'posted': posted})

def announce(request):
    posted = False
    if request.method == "POST":
        form = AnnounceForm(request.POST)
        if form.is_valid():
            obj = Annoucement(post_name=form.cleaned_data['title'], post_text=form.cleaned_data['text'], poster=request.user)
            obj.save()
            return HttpResponseRedirect(f'/forum/announce?posted=True')
    else:
        form = AnnounceForm()
        if 'posted' in request.GET:
            posted = True

    return render(request, 'announce.html', {"form": form, 
                                         'posted': posted})

def suggestion(request, suggestion_id):
    _suggestion = get_object_or_404(Suggestion, pk=suggestion_id)
    comments = Comment.objects.filter(linked_post=_suggestion).order_by("post_date")
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            obj = Comment(comment_text=form.cleaned_data['text'], linked_post=_suggestion, poster=request.user)
            obj.save()
            return HttpResponseRedirect(f'/forum/forum/{_suggestion.id}')
    else:
        form = CommentForm
    return render(request, 'suggestion.html', {'title': _suggestion.post_name,
                                                     'post_text': _suggestion.post_text,
                                                     'id': _suggestion.id,
                                                     'date':_suggestion.post_date,
                                                     'poster': _suggestion.poster.username,
                                                     'comments': comments,
                                                     'form': form})

def announcement(request, announcement_id):
    _announcement = get_object_or_404(Annoucement, pk=announcement_id)
    comments = Comment.objects.filter(linked_announcement=_announcement).order_by("post_date")
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            obj = Comment(comment_text=form.cleaned_data['text'], linked_announcement=_announcement, poster=request.user)
            obj.save()
            return HttpResponseRedirect(f'/forum/announcement/{_announcement.id}')
    else:
        form = CommentForm
    return render(request, 'announcement.html', {'title': _announcement.post_name,
                                                     'post_text': _announcement.post_text,
                                                     'id': _announcement.id,
                                                     'date':_announcement.post_date,
                                                     'comments': comments,
                                                     'form': form})