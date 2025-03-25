# blog/views.py
# views for the blog application
from xml.etree.ElementTree import Comment
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Article, Comment
from .forms import CreateArticleForm, CreateCommentForm, UpdateArticleForm 
from django.urls import reverse # (my comment) allows us to create a url from a url pattern name
from django.contrib.auth.mixins import LoginRequiredMixin ## NEW
from django.contrib.auth.forms import UserCreationForm ## NEW
from django.contrib.auth.models import User ## NEW
from django.contrib.auth import login # NEW


import random

# Create your views here.
class ShowAllView(ListView):
    '''Define a view class o show all blog Articles.'''

    model = Article
    template_name = "blog/show_all.html"
    context_object_name = "articles" # note plural variable name

    def dispatch(self, request, *args, **kwargs):
        '''Override the dispatch method to add debugging information.'''

        if request.user.is_authenticated:
            print(f'ShowAllView.dispatch(): request.user={request.user}')
        else:
            print(f'ShowAllView.dispatch(): not logged in.')

        return super().dispatch(request, *args, **kwargs)



class ArticleView(DetailView):
    '''Display a single article.'''

    model = Article
    template_name = 'blog/article.html'
    context_object_name = "article" # note singular variable name

class RandomArticleView(DetailView):
    '''Display a single article selected at random.'''
      
    model = Article
    template_name = 'blog/article.html'
    context_object_name = "article" # note singular variable name

    # methods
    def get_object(self):
        '''return one instance of the Article object 
        selected at random.'''

        all_articles = Article.objects.all()
        article = random.choice(all_articles)
        return article

# define a subclass of CreateView to handle creation of Article objects
class CreateArticleView(LoginRequiredMixin, CreateView):
    '''A view to handle creation of a new Article.
    (1) display the HTML form to user (GET)
    (2) process the form submission and store the new Article object (POST)
    '''

    form_class = CreateArticleForm
    template_name = "blog/create_article_form.html"

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 

    def form_valid(self, form):
        '''
        Handle the form submission to create a new Article object.
        '''
        print(f'CreateArticleView: form.cleaned_data={form.cleaned_data}')

        # find the logged in user
        user = self.request.user
        print(f"CreateArticleView user={user} article.user={user}")

        # attach user to form instance (Article object):
        form.instance.user = user

        return super().form_valid(form)
        

class CreateCommentView(CreateView):
    '''A view to handle creation of a new Comment on an Article.'''

    # specify the form class
    form_class = CreateCommentForm
    template_name = "blog/create_comment_form.html"

    # (my comment) this is what sends you to 
    # (my comment) show_all after after you've submitted the comment form
    def get_success_url(self):
        '''Provide a URL to redirect to after creating a new Comment.'''

        # create and return a URL:
        # (my comment) reverse allows us to create a url from a url pattern name
        # (my comment) originally --> the code below redirected you to show all after you submitted a comment
        #               now       --> he's getting the fk from the url link
        # return reverse('show_all') # not ideal; we will return to this


        pk = self.kwargs['pk']
        # call reverse to generate the URL for this Article
        return reverse('article', kwargs={'pk':pk})

    # (my comment) --> he made this method because he wanted the title for each create comment page
    # (my comment) --> to include the title of what page they were commenting on
    def get_context_data(self):
        '''Return the dictionary of context variables for use in the template.'''

        # calling the superclass method
        context = super().get_context_data()

        # find/add the article to the context data
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        article = Article.objects.get(pk=pk)

        # add this article into the context dictionary:
        context['article'] = article
        return context

    def form_valid(self, form): 
        '''This method handles the form submission and saves the 
        new object to the Django database.
        We need to add the foreign key (of the Article) to the Comment
        object before saving it to the database.
        '''
        # (my comment) ---> basically, this method is called after the form is submitted
        # (my comment) ---> this is what fixes the error message after making a comment? 

        print(form.cleaned_data)
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        article = Article.objects.get(pk=pk) # (my comment) we need to create an article object that we can attach to the new comment
        form.instance.article = article # set the Foreign Key

        # delegate the work to the superclass method form_valid):
        return super().form_valid(form)


class UpdateArticleView(UpdateView):
    '''View class to handle update of an article based on its PK.'''

    model = Article
    form_class = UpdateArticleForm
    template_name = "blog/update_article_form.html"


class DeleteCommentView(DeleteView):
    '''View class to delete a comment on an Article.'''

    model = Comment
    template_name = "blog/delete_comment_form.html"


    def get_success_url(self):
        '''Return the URL to redirect to after a successful delete.'''

        # find the PK for this Comment:
        pk = self.kwargs['pk']

        # find the Comment object:
        comment = Comment.objects.get(pk=pk)

        # find the PK of the Article to which this comment is associated:
        article = comment.article

        # return the URL to redirect to:
        return reverse('article', kwargs={'pk':article.pk})


class RegistrationView(CreateView):
    '''
    show/process form for account registration
    '''

    template_name = 'blog/register.html'
    form_class = UserCreationForm
    model = User
    
    def get_success_url(self):
        '''The URL to redirect to after creating a new User.'''
        return reverse('login')
  	       