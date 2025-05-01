# File: forms.py
# Author: Lance Sinson (ssinson@bu.edu), 5/1/25
# Description: The forms file for the dnd campaign manager website. 

# dnd_manager/forms.py
# forms for the dnd campaign manager application

from django import forms
from .models import (
    Campaign, Session, Character, NPC, Item, Quest, AdventureLog, CalendarEvent
)

class CampaignForm(forms.ModelForm):
    '''A form to add or update a campaign to the database'''
    class Meta:
        '''Associate this form with a model from our database'''
        model = Campaign
        # fields = ['name', 'description', 'start_date', 'status', 'dm']
        fields = ['name', 'description', 'start_date', 'status', 'map_image', 'main_image']



class SessionForm(forms.ModelForm):
    '''A form to add or update a session to the database'''
    class Meta:
        '''Associate this form with a model from our database'''
        model = Session
        # fields = ['name', 'campaign', 'session_date', 'summary', 'location']
        fields = ['name', 'session_date', 'summary', 'location']



class CharacterForm(forms.ModelForm):
    '''A form to add or update a Character to the database'''
    class Meta:
        '''Associate this form with a model from our database'''
        model = Character
        fields = [
            'name', 'player_name', 'class_type', 'level', 'race', 'backstory', 'strength', 
            'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma', 'max_hit_points', 
            'current_hit_points', 'armor_class', 'character_image', 'gold', 'status'
        ]

class GeneralCharacterForm(forms.ModelForm):
    '''A form to add or update a Character to the database from the general character list page'''
    class Meta:
        '''Associate this form with a model from our database'''
        model = Character
        fields = [
            'name', 'player_name', 'class_type', 'level', 'race', 'backstory', 'strength', 
            'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma', 'max_hit_points', 
            'current_hit_points', 'armor_class', 'character_image', 'gold', 'status', 'user'
        ]


class NPCForm(forms.ModelForm):
    '''A form to add or update an NPC to the database'''
    class Meta:
        '''Associate this form with a model from our database'''
        model = NPC
        # fields = ['name', 'description', 'location', 'campaign', 'npc_image']
        fields = ['name', 'description', 'location', 'npc_image']



class CreateItemForm(forms.ModelForm):
    '''A form to add an item (specifically by a player, to their own inventory) to the database'''
    class Meta:
        '''Associate this form with a model from our database'''
        model = Item
        # fields = [
        #     'name', 'description', 'item_type', 'rarity', 'owner_character', 'owner_npc', 
        #     'campaign', 'item_image', 'price'
        # ]
        fields = ['name', 'description', 'item_type', 'rarity', 'item_image', 'price']


        
class UpdateItemForm(forms.ModelForm):
    '''A form to update an item (specifically by a player modifying their inventory) to the database'''
    class Meta:
        '''Associate this form with a model from our database'''
        model = Item
        fields = [
            'name', 'description', 'item_type', 'rarity', 'owner_character', 'item_image', 'price'
        ]
        # fields = ['name', 'description', 'item_type', 'rarity', 'item_image', 'price']



class CreateGeneralItemForm(forms.ModelForm):
    '''A form to add an item (specifically by a DM from the general item list page) to the database'''
    class Meta:
        '''Associate this form with a model from our database'''
        model = Item
        fields = [
            'name', 'description', 'item_type', 'rarity', 'owner_character', 'owner_npc', 'item_image', 'price'
        ]
        # fields = ['name', 'description', 'item_type', 'rarity', 'item_image', 'price']



class QuestForm(forms.ModelForm):
    '''A form to add or update a quest to the database'''
    class Meta:
        '''Associate this form with a model from our database'''
        model = Quest
        # fields = ['title', 'quest_type', 'description', 'assigned_to', 'rewards', 'status', 'related_npc', 'campaign']
        fields = ['title', 'quest_type', 'description', 'assigned_to', 'rewards', 'status', 'related_npc', 'quest_date']



class AdventureLogForm(forms.ModelForm):
    '''A form to add or update an adventure log to the database'''
    class Meta:
        '''Associate this form with a model from our database'''
        model = AdventureLog
        # fields = ['session', 'character', 'details', 'xp_earned']
        fields = ['session', 'details', 'xp_earned', 'enemies_killed', 'number_of_downs']



class CalendarEventForm(forms.ModelForm):
    '''A form to add or update a calendar event to the database'''
    class Meta:
        '''Associate this form with a model from our database'''
        model = CalendarEvent
        fields = ['campaign', 'event_name', 'event_date', 'notes']



