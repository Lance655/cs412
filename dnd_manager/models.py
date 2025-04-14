from django.db import models
from django.utils import timezone

# Create your models here.

class Campaign(models.Model):
    STATUS_CHOICES = [
        ('ongoing', 'Ongoing'),
        ('hiatus', 'On Hiatus'),
        ('completed', 'Completed'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ongoing')

    def __str__(self):
        return self.name


class Session(models.Model):
    name = models.CharField(max_length=200)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='sessions')
    session_date = models.DateTimeField(default=timezone.now)
    summary = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Session {self.id} for {self.campaign.name} on {self.session_date}"


class Character(models.Model):
    name = models.CharField(max_length=100)
    player_name = models.CharField(max_length=100)
    class_type = models.CharField(max_length=100)
    level = models.PositiveIntegerField(default=1)
    race = models.CharField(max_length=100)
    backstory = models.TextField(blank=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='characters')

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

    def __str__(self):
        return f"{self.name} (Lvl {self.level} {self.class_type})"


class NPC(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='npcs')
    npc_image = models.ImageField(blank=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    RARITY_CHOICES = [
        ('Common', 'Common'),
        ('Uncommon', 'Uncommon'),
        ('Rare', 'Rare'),
        ('Legendary', 'Legendary'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    item_type = models.CharField(max_length=100)
    rarity = models.CharField(max_length=20, choices=RARITY_CHOICES, default='Common')
    # allow EITHER Character or NPC to own it:
    owner_character = models.ForeignKey(Character, on_delete=models.SET_NULL, null=True, blank=True, related_name='items_owned')
    owner_npc = models.ForeignKey(NPC, on_delete=models.SET_NULL, null=True, blank=True, related_name='items_held_by')
    
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='items')
    item_image = models.ImageField(blank=True)
    price = models.PositiveIntegerField(default=0)


    def __str__(self):
        return self.name


class Quest(models.Model):
    STATUS_CHOICES = [
        ('Not Started', 'Not Started'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    assigned_to = models.ManyToManyField(Character, blank=True, related_name='quests')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Not Started')
    related_npc = models.ForeignKey(NPC, on_delete=models.SET_NULL, null=True, blank=True, related_name='quests_given')
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='quests')

    def __str__(self):
        return f"{self.title} ({self.status})"


class AdventureLog(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='adventure_logs')
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='adventure_logs')
    details = models.TextField(blank=True)
    xp_earned = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"AdventureLog for {self.character.name} in session {self.session.id}"


class CalendarEvent(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='events')
    event_name = models.CharField(max_length=200)
    event_date = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.event_name} - {self.event_date}"
