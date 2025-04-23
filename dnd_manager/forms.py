from django import forms
from .models import (
    Campaign, Session, Character, NPC, Item, Quest, AdventureLog, CalendarEvent
)

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        # fields = ['name', 'description', 'start_date', 'status', 'dm']
        fields = ['name', 'description', 'start_date', 'status']



class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        # fields = ['name', 'campaign', 'session_date', 'summary', 'location']
        fields = ['name', 'session_date', 'summary', 'location']



class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = [
            'name', 'player_name', 'class_type', 'level', 'race', 'backstory', 'strength', 
            'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma', 'max_hit_points', 
            'current_hit_points', 'armor_class', 'character_image', 'gold'
        ]


class NPCForm(forms.ModelForm):
    class Meta:
        model = NPC
        # fields = ['name', 'description', 'location', 'campaign', 'npc_image']
        fields = ['name', 'description', 'location', 'npc_image']



class CreateItemForm(forms.ModelForm):
    class Meta:
        model = Item
        # fields = [
        #     'name', 'description', 'item_type', 'rarity', 'owner_character', 'owner_npc', 
        #     'campaign', 'item_image', 'price'
        # ]
        fields = ['name', 'description', 'item_type', 'rarity', 'item_image', 'price']


        
class UpdateItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'name', 'description', 'item_type', 'rarity', 'owner_character', 'item_image', 'price'
        ]
        # fields = ['name', 'description', 'item_type', 'rarity', 'item_image', 'price']



class CreateGeneralItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'name', 'description', 'item_type', 'rarity', 'owner_character', 'owner_npc', 'item_image', 'price'
        ]
        # fields = ['name', 'description', 'item_type', 'rarity', 'item_image', 'price']



class QuestForm(forms.ModelForm):
    class Meta:
        model = Quest
        # fields = ['title', 'quest_type', 'description', 'assigned_to', 'rewards', 'status', 'related_npc', 'campaign']
        fields = ['title', 'quest_type', 'description', 'assigned_to', 'rewards', 'status', 'related_npc', 'quest_date']



class AdventureLogForm(forms.ModelForm):
    class Meta:
        model = AdventureLog
        # fields = ['session', 'character', 'details', 'xp_earned']
        fields = ['session', 'details', 'xp_earned', 'enemies_killed', 'number_of_downs']



class CalendarEventForm(forms.ModelForm):
    class Meta:
        model = CalendarEvent
        fields = ['campaign', 'event_name', 'event_date', 'notes']
