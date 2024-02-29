from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from .models import Annoucement, Suggestion, Comment
from .forms import PostForm, CommentForm
# Create your views here.

def forum(request):
    suggestions = Suggestion.objects.order_by("post_date")
    annoucements = Annoucement.objects.filter(priority=True).order_by("post_date")
    return render(request, "forum.html", {"suggestions": suggestions,
                                          'announcements': annoucements})

def post(request):
    posted = False
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            obj = Suggestion(post_name=form.cleaned_data['title'], post_text=form.cleaned_data['text'])
            obj.save()
            return HttpResponseRedirect(f'/forum/post?posted=True')
    else:
        form = PostForm()
        if 'posted' in request.GET:
            posted = True

    return render(request, 'post.html', {"form": form, 
                                         'posted': posted})

def suggestion(request, suggestion_id):
    _suggestion = get_object_or_404(Suggestion, pk=suggestion_id)
    comments = Comment.objects.filter(linked_post=_suggestion).order_by("post_date")
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            obj = Comment(comment_text=form.cleaned_data['text'], linked_post=_suggestion)
            obj.save()
            return HttpResponseRedirect(f'/forum/forum/{_suggestion.id}')
    else:
        form = CommentForm
    return render(request, 'suggestion.html', {'title': _suggestion.post_name,
                                                     'post_text': _suggestion.post_text,
                                                     'id': _suggestion.id,
                                                     'date':_suggestion.post_date,
                                                     'comments': comments,
                                                     'form': form})

def announcement(request, announcement_id):
    _announcement = get_object_or_404(Annoucement, pk=announcement_id)
    comments = Comment.objects.filter(linked_post=_announcement).order_by("post_date")
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            obj = Comment(comment_text=form.cleaned_data['text'], linked_post=_announcement)
            obj.save()
            return HttpResponseRedirect(f'/forum/forum/{_announcement.id}')
    else:
        form = CommentForm
    return render(request, 'suggestion.html', {'title': _announcement.post_name,
                                                     'post_text': _announcement.post_text,
                                                     'id': _announcement.id,
                                                     'date':_announcement.post_date,
                                                     'comments': comments,
                                                     'form': form})