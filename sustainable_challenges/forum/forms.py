from django import forms


class PostForm(forms.Form):
    title = forms.CharField(label="Post Title", max_length=100)
    text = forms.CharField(label="Post Text", max_length=400)

class CommentForm(forms.Form):
    text = forms.CharField(label="Comment:", max_length=400)