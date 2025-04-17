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
    path('campaigns/<int:campaign_id>/characters/<int:pk>/', CharacterDetailView.as_view(), name='character_detail'),
    path('campaigns/<int:campaign_id>/characters/create/', CharacterCreateView.as_view(), name='character_create'),
    path('campaigns/<int:campaign_id>/characters/<int:pk>/update/', CharacterUpdateView.as_view(), name='character_update'),
    path('campaigns/<int:campaign_id>/characters/<int:pk>/delete/', CharacterDeleteView.as_view(), name='character_delete'),

    # NPC
    path('campaigns/<int:campaign_id>/npcs/', NPCListView.as_view(), name='npc_list'),
    path('campaigns/<int:campaign_id>/npcs/create/', NPCCreateView.as_view(), name='npc_create'),
    path('campaigns/<int:campaign_id>/npcs/<int:pk>/', NPCDetailView.as_view(), name='npc_detail'),
    path('campaigns/<int:campaign_id>/npcs/<int:pk>/update/', NPCUpdateView.as_view(), name='npc_update'),
    path('campaigns/<int:campaign_id>/npcs/<int:pk>/delete/', NPCDeleteView.as_view(), name='npc_delete'),

    # Items
    path('campaigns/<int:campaign_id>/characters/<int:character_id>/items/create/', ItemCreateView.as_view(), name='item_create'),
    path('campaigns/<int:campaign_id>/characters/<int:character_id>/items/<int:pk>/update/', ItemUpdateView.as_view(), name='item_update'),
    path('campaigns/<int:campaign_id>/characters/<int:character_id>/items/<int:pk>/delete/', ItemDeleteView.as_view(), name='item_delete'),

]


