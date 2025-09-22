from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    """
    Represents a single blog post.
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True) # Automatically set when object is created
    updated_at = models.DateTimeField(auto_now=True)     # Automatically set every time object is saved

    def __str__(self):
        """
        A string representation of the model, used in the admin and elsewhere.
        """
        return self.title
    

class Comment(models.Model):
    """
    Represents a comment on a blog post.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post}'