from django import forms


class PostForm(forms.Form):
    #Basic Suggestion form
    title = forms.CharField(label="Post Title", max_length=100)
    text = forms.CharField(label="Post Text", max_length=400)

class CommentForm(forms.Form):
    #Basic comment form
    text = forms.CharField(label="Comment:", max_length=400)

class AnnounceForm(forms.Form):
    #Basic announcement form
    title = forms.CharField(label="Post Title", max_length=100)
    text = forms.CharField(label="Post Text", max_length=400)
