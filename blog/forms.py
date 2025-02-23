# blog/forms.py
# define the forms that we use for create/update/delete operations

from django import forms
from .models import Article, Comment

class CreateArticleForm(forms.ModelForm):
    '''A form to add an Article to the database.'''

    class Meta:
        '''Associate this form with a model from our database.'''
        model = Article
        # specify the fields you want to be able to create with this form
        fields = ['author', 'title', 'text', 'image_url']

class CreateCommentForm(forms.ModelForm):
    '''A form to add a Comment about an Article.'''

    class Meta:
        '''associate this form with a model from our database.'''
        model = Comment
        # fields = ['article', 'author', 'text']
        fields = ['author', 'text'] # (my comment) remove article ---> we don't want the drop-down list

        
