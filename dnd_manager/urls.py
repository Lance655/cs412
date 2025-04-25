from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views # NEW


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
    path('campaigns/<int:campaign_id>/characters/create/', CharacterGeneralCreateView.as_view(), name='character_create_general'),
    path('campaigns/<int:campaign_id>/my_characters/create/', CharacterCreateView.as_view(), name='character_create'),
    path('campaigns/<int:campaign_id>/characters/<int:pk>/update/', CharacterUpdateView.as_view(), name='character_update'),
    path('campaigns/<int:campaign_id>/characters/<int:pk>/delete/', CharacterDeleteView.as_view(), name='character_delete'),

    # NPC
    path('campaigns/<int:campaign_id>/npcs/', NPCListView.as_view(), name='npc_list'),
    path('campaigns/<int:campaign_id>/npcs/create/', NPCCreateView.as_view(), name='npc_create'),
    path('campaigns/<int:campaign_id>/npcs/<int:pk>/', NPCDetailView.as_view(), name='npc_detail'),
    path('campaigns/<int:campaign_id>/npcs/<int:pk>/update/', NPCUpdateView.as_view(), name='npc_update'),
    path('campaigns/<int:campaign_id>/npcs/<int:pk>/delete/', NPCDeleteView.as_view(), name='npc_delete'),

    # Items
    path('campaigns/<int:campaign_id>/items/', ItemListView.as_view(), name='item_list'),
    path('campaigns/<int:campaign_id>/characters/<int:character_id>/items/create/', ItemCreateView.as_view(), name='item_create'),
    path('campaigns/<int:campaign_id>/items/<int:pk>/', ItemDetailView.as_view(), name='item_detail'),
    path('campaigns/<int:campaign_id>/characters/<int:character_id>/items/<int:pk>/update/', ItemUpdateView.as_view(), name='item_update'),
    path('campaigns/<int:campaign_id>/characters/<int:character_id>/items/<int:pk>/delete/', ItemDeleteView.as_view(), name='item_delete'),
    path('campaigns/<int:campaign_id>/characters/<int:character_id>/items/<int:pk>/sell/', item_sell_view, name='item_sell'),

    # General Item CRUD
    path('campaigns/<int:campaign_id>/items/create/', ItemCreateGeneralView.as_view(), name="item_create_general"),
    path('campaigns/<int:campaign_id>/items/<int:pk>/update/', ItemUpdateGeneralView.as_view(), name="item_update_general"),
    path('campaigns/<int:campaign_id>/items/<int:pk>/delete/', ItemDeleteGeneralView.as_view(), name="item_delete_general"),



    # Adventure Logs
    path('campaigns/<int:campaign_id>/characters/<int:character_id>/logs/create/', AdventureLogCreateView.as_view(), name='adventure_log_create'),
    path('campaigns/<int:campaign_id>/characters/<int:character_id>/logs/<int:pk>/update/', AdventureLogUpdateView.as_view(), name='adventure_log_update'),
    path('campaigns/<int:campaign_id>/characters/<int:character_id>/logs/<int:pk>/delete/', AdventureLogDeleteView.as_view(), name='adventure_log_delete'),

    # Quests
    path('campaigns/<int:campaign_id>/quests/', QuestListView.as_view(), name='quest_list'),
    path('campaigns/<int:campaign_id>/quests/create/', QuestCreateView.as_view(), name='quest_create'),
    path('campaigns/<int:campaign_id>/quests/<int:pk>/', QuestDetailView.as_view(), name='quest_detail'),
    path('campaigns/<int:campaign_id>/quests/<int:pk>/update/', QuestUpdateView.as_view(), name='quest_update'),
    path('campaigns/<int:campaign_id>/quests/<int:pk>/delete/', QuestDeleteView.as_view(), name='quest_delete'),


    # Login / Logout / Registration
    path('login/', auth_views.LoginView.as_view(template_name='dnd_manager/login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='dnd_manager/logged_out.html'), name="logout"),
    path('register/', UserRegistrationView.as_view(), name='register'),

    # multiple characters
    path('campaigns/<int:campaign_id>/my_characters/', MyCharactersListView.as_view(), name='my_characters'),

    # Map
    path('campaigns/<int:pk>/map/', CampaignMapView.as_view(), name='campaign_map'),

    # References (from API)
    path('campaigns/<int:campaign_id>/references/', references_search_view, name='references_search'),
    path('campaigns/<int:campaign_id>/references/<str:search_type>/<str:slug>/', references_detail_view, name='references_detail'),

]


