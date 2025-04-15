from django.urls import path
from .views import *

urlpatterns = [

    path('', CampaignListView.as_view(), name='home'),

    # Campaign
    path('campaigns/', CampaignListView.as_view(), name='campaign_list'),
    path('campaigns/create/', CampaignCreateView.as_view(), name='campaign_create'),
    path('campaigns/<int:pk>/', CampaignDetailView.as_view(), name='campaign_detail'),
    path('campaigns/<int:pk>/update/', CampaignUpdateView.as_view(), name='campaign_update'),
    path('campaigns/<int:pk>/delete/', CampaignDeleteView.as_view(), name='campaign_delete'),

    # Session
    path('campaigns/<int:campaign_id>/sessions/create/', SessionCreateView.as_view(), name='session_create'),
    path('campaigns/<int:campaign_id>/sessions/<int:pk>/', SessionDetailView.as_view(), name='session_detail'),
    path('campaigns/<int:campaign_id>/sessions/<int:pk>/update/', SessionUpdateView.as_view(), name='session_update'),
    path('campaigns/<int:campaign_id>/sessions/<int:pk>/delete/', SessionDeleteView.as_view(), name='session_delete'),
    # path('campaigns/<int:campaign_id>/sessions/', SessionListView.as_view(), name='session_list'),

    # Character
    path('campaigns/<int:campaign_id>/characters/', CharacterListView.as_view(), name='character_list'),
    path('campaigns/<int:campaign_id>/characters/create/', CharacterCreateView.as_view(), name='character_create'),
    path('campaigns/<int:campaign_id>/characters/<int:pk>/', CharacterDetailView.as_view(), name='character_detail'),
    path('campaigns/<int:campaign_id>/characters/<int:pk>/update/', CharacterUpdateView.as_view(), name='character_update'),
    path('campaigns/<int:campaign_id>/characters/<int:pk>/delete/', CharacterDeleteView.as_view(), name='character_delete'),

    # Character
#     path('characters/', CharacterListView.as_view(), name='character_list'),
#     path('characters/create/', CharacterCreateView.as_view(), name='character_create'),
#     path('characters/<int:pk>/', CharacterDetailView.as_view(), name='character_detail'),
#     path('characters/<int:pk>/update/', CharacterUpdateView.as_view(), name='character_update'),
#     path('characters/<int:pk>/delete/', CharacterDeleteView.as_view(), name='character_delete'),

#     # NPC
#     path('npcs/',  NPCListView.as_view(), name='npc_list'),
#     path('npcs/create/',  NPCCreateView.as_view(), name='npc_create'),
#     path('npcs/<int:pk>/',  NPCDetailView.as_view(), name='npc_detail'),
#     path('npcs/<int:pk>/update/', NPCUpdateView.as_view(), name='npc_update'),
#     path('npcs/<int:pk>/delete/', NPCDeleteView.as_view(), name='npc_delete'),

#     # Item
#     path('items/', ItemListView.as_view(), name='item_list'),
#     path('items/create/', ItemCreateView.as_view(), name='item_create'),
#     path('items/<int:pk>/', ItemDetailView.as_view(), name='item_detail'),
#     path('items/<int:pk>/update/', ItemUpdateView.as_view(), name='item_update'),
#     path('items/<int:pk>/delete/', ItemDeleteView.as_view(), name='item_delete'),

#     # Quest
#     path('quests/', QuestListView.as_view(), name='quest_list'),
#     path('quests/create/', QuestCreateView.as_view(), name='quest_create'),
#     path('quests/<int:pk>/', QuestDetailView.as_view(), name='quest_detail'),
#     path('quests/<int:pk>/update/', QuestUpdateView.as_view(), name='quest_update'),
#     path('quests/<int:pk>/delete/', QuestDeleteView.as_view(), name='quest_delete'),

#     # AdventureLog
#     path('adventurelogs/', AdventureLogListView.as_view(), name='adventurelog_list'),
#     path('adventurelogs/create/', AdventureLogCreateView.as_view(), name='adventurelog_create'),
#     path('adventurelogs/<int:pk>/', AdventureLogDetailView.as_view(), name='adventurelog_detail'),
#     path('adventurelogs/<int:pk>/update/', AdventureLogUpdateView.as_view(), name='adventurelog_update'),
#     path('adventurelogs/<int:pk>/delete/', AdventureLogDeleteView.as_view(), name='adventurelog_delete'),

#     # CalendarEvent
#     path('events/', CalendarEventListView.as_view(), name='event_list'),
#     path('events/create/', CalendarEventCreateView.as_view(), name='event_create'),
#     path('events/<int:pk>/', CalendarEventDetailView.as_view(), name='event_detail'),
#     path('events/<int:pk>/update/', CalendarEventUpdateView.as_view(), name='event_update'),
#     path('events/<int:pk>/delete/', CalendarEventDeleteView.as_view(), name='event_delete'),
]
