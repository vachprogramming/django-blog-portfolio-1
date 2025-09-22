from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    """
    Form for users to add comments.
    """
    class Meta:
        model = Comment
        fields = ('body',) # We only want the user to edit the body