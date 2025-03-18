# mini_fb/models.py
# define data models for the mini_fb application

from django.db import models
from django.urls import reverse


# Create your models here.
class Profile(models.Model):
    '''Encapsulate the data profile for each user'''
    first_name = models.TextField(blank=True)
    last_name = models.TextField(blank=True)
    city = models.TextField(blank=True)
    email_address = models.TextField(blank=True)
    image_url = models.URLField(blank=True)

    def __str__(self): 
        '''return a string representation of this model instance.'''
        return f'{self.first_name}'

    def get_status_messages(self):
        '''Return a QuerySet of status messages about this profile.'''
        status_messages = StatusMessage.objects.filter(profile=self)
        return status_messages 

    def get_absolute_url(self):
        '''Return a URL to display one instance of this object.'''
        return reverse('show_profile', kwargs={'pk': self.pk})

    def get_friends(self):
        '''Return a list of a profile's friends'''
        friends1 = Friend.objects.filter(profile1=self)
        friends2 = Friend.objects.filter(profile2=self)

        # Extract the actual Profile objects
        friend_profiles = [friend.profile2 for friend in friends1] + [friend.profile1 for friend in friends2]

        return friend_profiles

    def add_friend(self, other):
        '''Takes a parameter other, which refers to another Profile instance, 
        and the effect of the method should be add a Friend relation for the 
        two Profiles: self and other.'''
 
        if self != other:
            # Check if a friend object already exists between the two profiles
            check_friends = Friend.objects.filter(profile1=self, profile2=other) | Friend.objects.filter(profile1=other, profile2=self)
            if len(check_friends) == 0:
                Friend.objects.create(profile1=self, profile2=other)

    def get_friend_suggestions(self):
        '''Return a list (or QuerySet) of possible friends for a Profile.'''

        friends = self.get_friends()
        suggestions = []
        for friend in friends:
            for potential_friend in friend.get_friends():
                if (potential_friend not in friends) and (potential_friend != self):
                    suggestions += [potential_friend]
        return suggestions
        

       
    


class StatusMessage(models.Model):
    '''Encapsulate the idea of a status message for a individual profile'''

    # data attributes for Status Messages:
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    message = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''return a string representation of this model instance.'''
        return f'{self.message} - {self.profile.first_name}'

    def get_images(self):
        '''method to find all images associated to this status message'''
        # status_images is a list of StatusImage objects
        status_images = StatusImage.objects.filter(status_message_fk=self)

        # Extract the Image objects from the StatusImage queryset
        images = [status_image.image_fk for status_image in status_images]


        return images


class Image(models.Model):
    '''Encapsulates the idea of an image file that is stored in the Django
    media directory'''

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image_file = models.ImageField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    caption = models.TextField(blank=True)

    def __str__(self):
        '''return a string representation of this model instance'''
        return f'Image "{self.image_file}" associated with {self.profile}'

class StatusImage(models.Model):
    '''Links together images and status messages'''
    image_fk = models.ForeignKey(Image, on_delete=models.CASCADE)
    status_message_fk = models.ForeignKey(StatusMessage, on_delete=models.CASCADE)

    def __str__(self):
        '''return a string representation of this model instance'''
        return f'Linking image ("{self.image_fk}") and status message ("{self.status_message_fk}")'

class Friend(models.Model):
    '''Encapsulates the idea of an edge connecting two nodes within the social network (e.g., 
    two Profiles that are friends with each other).
    '''
    profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile1")
    profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile2")
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''return a string representation of this model instance'''
        return f'{self.profile1.first_name} {self.profile1.last_name} & {self.profile2.first_name} {self.profile2.last_name}'


