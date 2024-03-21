from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseForbidden
from django.template import loader
from django.urls import reverse
from .models import Annoucement, Suggestion, Comment
from .forms import PostForm, CommentForm, AnnounceForm
# Create your views here.

def forum(request):
    # Gets all posts and gives them when renderinh
    suggestions = Suggestion.objects.order_by("post_date")
    annoucements = Annoucement.objects.filter(active=True).order_by("post_date")
    return render(request, "forum.html", {"suggestions": suggestions,
                                          'announcements': annoucements,
                                          "is_staff": request.user.is_staff})

def post(request):
    posted = False
    if request.method == "POST":
        # Takes the post form and turns it into an objext
        form = PostForm(request.POST)
        if form.is_valid():
            obj = Suggestion(post_name=form.cleaned_data['title'], post_text=form.cleaned_data['text'], poster=request.user)
            obj.save()
            return HttpResponseRedirect(f'/forum/post?posted=True')
    else:
        #Gives blank post form
        form = PostForm()
        if 'posted' in request.GET:
            posted = True

    return render(request, 'post.html', {"form": form, 
                                         'posted': posted,
                                         "is_staff": request.user.is_staff})

def announce(request):
    posted = False
    if not request.user.is_staff:
        return HttpResponseForbidden()
    
    if request.method == "POST":
        # Takes the announce form and turns it into an objext
        form = AnnounceForm(request.POST)
        if form.is_valid():
            obj = Annoucement(post_name=form.cleaned_data['title'], post_text=form.cleaned_data['text'], poster=request.user)
            obj.save()
            return HttpResponseRedirect(f'/forum/announce?posted=True')
    else:
        #Gives blank announce form
        form = AnnounceForm()
        if 'posted' in request.GET:
            posted = True

    return render(request, 'announce.html', {"form": form, 
                                         'posted': posted,
                                         "is_staff": request.user.is_staff})

def suggestion(request, suggestion_id):
    # Gets suggestion and the comments on it
    _suggestion = get_object_or_404(Suggestion, pk=suggestion_id)
    comments = Comment.objects.filter(linked_post=_suggestion).order_by("post_date")
    if request.method == 'POST':
        #Creates a comment with form given
        form = CommentForm(request.POST)
        if form.is_valid():
            obj = Comment(comment_text=form.cleaned_data['text'], linked_post=_suggestion, poster=request.user)
            obj.save()
            return HttpResponseRedirect(f'/forum/forum/suggestion/{_suggestion.id}')
    else:
        # Gives blank comment form
        form = CommentForm
    return render(request, 'suggestion.html', {'title': _suggestion.post_name,
                                                     'post_text': _suggestion.post_text,
                                                     'object_id': _suggestion.id,
                                                     'date':_suggestion.post_date,
                                                     'poster': _suggestion.poster,
                                                     'comments': comments,
                                                     'form': form,
                                                     "is_staff": request.user.is_staff,
                                                     "requester_id": request.user.id})

def announcement(request, announcement_id):
    # Gets announcement and the comments on it
    _announcement = get_object_or_404(Annoucement, pk=announcement_id)
    comments = Comment.objects.filter(linked_announcement=_announcement).order_by("post_date")
    if request.method == 'POST':
        #Creates a commrnt with form given
        form = CommentForm(request.POST)
        if form.is_valid():
            obj = Comment(comment_text=form.cleaned_data['text'], linked_announcement=_announcement, poster=request.user)
            obj.save()
            return HttpResponseRedirect(f'/forum/announcement/{_announcement.id}')
    else:
        # Gives blank comment form
        form = CommentForm
    return render(request, 'announcement.html', {'title': _announcement.post_name,
                                                     'post_text': _announcement.post_text,
                                                     'id': _announcement.id,
                                                     'date':_announcement.post_date,
                                                     'comments': comments,
                                                     'form': form,
                                                     "is_staff": request.user.is_staff})

def delete_post_function(request, id):
    ob = Suggestion.objects.get(id=id)
    ob.delete()
    return redirect(reverse('forum:forum'))

def endorse(request, id):
    ob = Suggestion.objects.get(id=id)
    if request.user.id in ob.endorsements:
        return redirect(reverse('forum:forum:suggestion:{id}'))
    else:
        ob.endorsements.append(id)
        return redirect(reverse('forum:forum:suggestion:{id}'))
