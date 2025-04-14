from django.contrib import admin

# Register your models here.
from .models import Campaign, Session, Character, NPC, Item, Quest, AdventureLog, CalendarEvent

admin.site.register(Campaign)
admin.site.register(Session)
admin.site.register(Character)
admin.site.register(NPC)
admin.site.register(Item)
admin.site.register(Quest)
admin.site.register(AdventureLog)
admin.site.register(CalendarEvent)