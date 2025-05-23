# File: models.py
# Author: Lance Sinson (ssinson@bu.edu), 5/1/25
# Description: The models file for the dnd campaign manager website. 

# dnd_manager/models.py
# models for the dnd campaign manager application

from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import User  # new


# Create your models here.

class Campaign(models.Model):
    '''Encapsulate the data for each campaign'''

    STATUS_CHOICES = [
        ('ongoing', 'Ongoing'),
        ('hiatus', 'On Hiatus'),
        ('completed', 'Completed'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ongoing')
    dm = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, 
                           related_name='campaigns_as_dm')
    map_image = models.ImageField(blank=True, null=True)
    main_image = models.ImageField(blank=True, null=True)



    def __str__(self):
        return self.name


class Session(models.Model):

    '''Encapsulate the data for each session within a campaign'''
    name = models.CharField(max_length=200)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='sessions')
    session_date = models.DateTimeField(default=timezone.now)
    summary = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.campaign.name} | {self.name }on {self.session_date}"


class Character(models.Model):
    '''Encapsulate the data for each character'''

    STATUS_CHOICES = [
        ('Alive', 'Alive'),
        ('Dead', 'Dead'),
        ('Retired', 'Retired'),
    ]

    # general information
    name = models.CharField(max_length=100)
    player_name = models.CharField(max_length=100)
    class_type = models.CharField(max_length=100)
    level = models.PositiveIntegerField(default=1)
    race = models.CharField(max_length=100)
    backstory = models.TextField(blank=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='characters')


    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Alive'
    )

    # D&D core ability scores
    strength = models.PositiveSmallIntegerField(default=10)
    dexterity = models.PositiveSmallIntegerField(default=10)
    constitution = models.PositiveSmallIntegerField(default=10)
    intelligence = models.PositiveSmallIntegerField(default=10)
    wisdom = models.PositiveSmallIntegerField(default=10)
    charisma = models.PositiveSmallIntegerField(default=10)

    # Hit points & Armor Class
    max_hit_points = models.PositiveIntegerField(default=10)
    current_hit_points = models.PositiveIntegerField(default=10)
    armor_class = models.PositiveIntegerField(default=10)


    character_image = models.ImageField(blank=True)
    gold = models.PositiveIntegerField(default=0)

    # User FK
    user = models.ForeignKey(User, on_delete=models.CASCADE) 

    def __str__(self):
        return f"{self.name} (Lvl {self.level} {self.class_type})"


class NPC(models.Model):
    '''Encapsulate the data for each non-player character (NPC)'''

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='npcs')
    npc_image = models.ImageField(blank=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    '''Encapsulate the data for each item'''

    ITEM_TYPE_CHOICES = [
        ('Weapon', 'Weapon'),
        ('Armor', 'Armor'),
        ('Potion', 'Potion'),
        ('Ring', 'Ring'),
        ('Rod', 'Rod'),
        ('Scroll', 'Scroll'),
        ('Staff', 'Staff'),
        ('Wand', 'Wand'),
        ('Wondrous Item', 'Wondrous Item'),
        ('Artifact', 'Artifact'),
        ('Adventuring Gear', 'Adventuring Gear'),
        ('Tool', 'Tool'),
        ('Material', 'Material'),
        ('Food/Drink', 'Food/Drink'),
        ('Miscellaneous', 'Miscellaneous'),
    ]

    RARITY_CHOICES = [
        ('Common', 'Common'),
        ('Uncommon', 'Uncommon'),
        ('Rare', 'Rare'),
        ('Legendary', 'Legendary'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    item_type = models.CharField(max_length=30, choices=ITEM_TYPE_CHOICES, default='Weapon')
    rarity = models.CharField(max_length=20, choices=RARITY_CHOICES, default='Common')
    # allow either Character or NPC to own it
    owner_character = models.ForeignKey(Character, on_delete=models.SET_NULL, null=True, blank=True, related_name='items_owned')
    owner_npc = models.ForeignKey(NPC, on_delete=models.SET_NULL, null=True, blank=True, related_name='items_held_by')
    
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='items')
    item_image = models.ImageField(blank=True)
    price = models.PositiveIntegerField(default=0)


    def __str__(self):
        return self.name


class Quest(models.Model):
    '''Encapsulate the data for each quest'''

    STATUS_CHOICES = [
        ('Not Started', 'Not Started'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    QUEST_TYPE_CHOICES = [
        ('Main Quest', 'Main Quest'),
        ('Personal Quest', 'Personal Quest'),
    ]

    title = models.CharField(max_length=200)
    quest_type = models.CharField(max_length=20, choices=QUEST_TYPE_CHOICES, default='Main')
    description = models.TextField()
    assigned_to = models.ManyToManyField(Character, blank=True, related_name='quests')
    rewards = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Not Started')
    related_npc = models.ForeignKey(NPC, on_delete=models.SET_NULL, null=True, blank=True, related_name='quests_given')
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='quests')
    quest_date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f"{self.title} ({self.status})"


class AdventureLog(models.Model):
    '''Encapsulate the data to keep track of each character's adventure log per session'''

    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='adventure_logs')
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='adventure_logs')
    details = models.TextField(blank=True)
    xp_earned = models.PositiveIntegerField(default=0)
    enemies_killed = models.PositiveIntegerField(default=0)
    number_of_downs = models.PositiveIntegerField(default=0)


    def __str__(self):
        return f"AdventureLog for {self.character.name} in session {self.session.id}"


class CalendarEvent(models.Model):
    '''Encapsulate the data to schedule future meetings'''

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='events')
    event_name = models.CharField(max_length=200)
    event_date = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.event_name} - {self.event_date}"
