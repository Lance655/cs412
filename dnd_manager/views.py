from django.shortcuts import render

from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import (
    Campaign, Session, Character, NPC, Item, Quest, AdventureLog, CalendarEvent
)
from .forms import (
    CampaignForm, SessionForm, CharacterForm, NPCForm, 
    ItemForm, QuestForm, AdventureLogForm, CalendarEventForm
)


# Create your views here.

# -----------------
# Campaign Views
# -----------------

class CampaignListView(ListView):
    model = Campaign
    template_name = 'dnd_manager/campaign_list.html'
    context_object_name = 'campaigns'


class CampaignDetailView(DetailView):
    model = Campaign
    template_name = 'dnd_manager/campaign_detail.html'
    context_object_name = 'campaign'

    def get_context_data(self, **kwargs):
        
        # Add related data to the context
        context = super().get_context_data(**kwargs)
        campaign = self.get_object()
        context['sessions'] = campaign.sessions.all()
        context['characters'] = campaign.characters.all()
        context['items'] = campaign.items.all()
        context['npcs'] = campaign.npcs.all()
        context['quests'] = campaign.quests.all()
        context['events'] = campaign.events.all()
        return context


class CampaignCreateView(CreateView):
    model = Campaign
    form_class = CampaignForm
    template_name = 'dnd_manager/create_campaign_form.html'
    success_url = reverse_lazy('campaign_list')


class CampaignUpdateView(UpdateView):
    model = Campaign
    form_class = CampaignForm
    template_name = 'dnd_manager/create_campaign_form.html'
    success_url = reverse_lazy('campaign_list')


class CampaignDeleteView(DeleteView):
    model = Campaign
    template_name = 'dnd_manager/delete_campaign_confirm.html'
    success_url = reverse_lazy('campaign_list')


# -----------------
# Session Views
# -----------------

class SessionListView(ListView):
    model = Session
    template_name = 'dnd_manager/session_list.html'
    context_object_name = 'sessions'


class SessionDetailView(DetailView):
    model = Session
    template_name = 'dnd_manager/session_detail.html'
    context_object_name = 'session'


class SessionCreateView(CreateView):
    model = Session
    form_class = SessionForm
    template_name = 'dnd_manager/create_session_form.html'

    def form_valid(self, form):
        """Set the campaign based on URL campaign_id before saving."""
        campaign_id = self.kwargs['campaign_id']
        campaign = Campaign.objects.get(pk=campaign_id)
        form.instance.campaign = campaign
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect back to the session list (or campaign detail)."""
        return reverse('campaign_detail', kwargs={'pk': self.kwargs['campaign_id']})
        
    def get_context_data(self, **kwargs):
        """Make sure we include the campaign in the context for the template."""
        context = super().get_context_data(**kwargs)
        campaign_id = self.kwargs['campaign_id']
        campaign = Campaign.objects.get(pk=campaign_id)
        context['campaign'] = campaign
        return context


class SessionUpdateView(UpdateView):
    model = Session
    form_class = SessionForm
    template_name = 'dnd_manager/create_session_form.html'

    def get_context_data(self, **kwargs):
        """Make sure we include the campaign in the context for the template."""
        context = super().get_context_data(**kwargs)
        campaign_id = self.kwargs['campaign_id']
        campaign = Campaign.objects.get(pk=campaign_id)
        context['campaign'] = campaign
        return context

    def get_success_url(self):
        """Redirect back to the session list (or campaign detail)."""
        return reverse('campaign_detail', kwargs={'pk': self.kwargs['campaign_id']})


class SessionDeleteView(DeleteView):
    model = Session
    template_name = 'dnd_manager/delete_session_confirm.html'

    def get_success_url(self):
        """Redirect back to the session list (or campaign detail)."""
        return reverse('campaign_detail', kwargs={'pk': self.kwargs['campaign_id']})


# -----------------
# Character Views
# -----------------

class CharacterListView(ListView):
    model = Character
    template_name = 'dnd_manager/character_list.html'
    context_object_name = 'characters'

    def get_queryset(self):
        """Return only Characters belonging to the given campaign_id."""
        campaign_id = self.kwargs['campaign_id']
        return Character.objects.filter(campaign__id=campaign_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campaign_id = self.kwargs['campaign_id']
        campaign = Campaign.objects.get(pk=campaign_id)
        context['campaign'] = campaign
        return context


class CharacterDetailView(DetailView):
    model = Character
    template_name = 'dnd_manager/character_detail.html'
    context_object_name = 'character'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the Campaign to the template
        campaign_id = self.kwargs['campaign_id']
        campaign = Campaign.objects.get(pk=campaign_id)
        context['campaign'] = campaign
        return context


class CharacterCreateView(CreateView):
    model = Character
    form_class = CharacterForm
    template_name = 'dnd_manager/create_character_form.html'

    def form_valid(self, form):
        """Assign the correct Campaign via the URL param before saving."""
        campaign_id = self.kwargs['campaign_id']
        campaign = Campaign.objects.get(pk=campaign_id)
        form.instance.campaign = campaign
        return super().form_valid(form)

    def get_success_url(self):
        """After creating a Character, go back to the Campaign detail page."""
        return reverse('campaign_detail', kwargs={'pk': self.kwargs['campaign_id']})

    def get_context_data(self, **kwargs):
        """Pass the Campaign into the template context."""
        context = super().get_context_data(**kwargs)
        campaign_id = self.kwargs['campaign_id']
        campaign = Campaign.objects.get(pk=campaign_id)
        context['campaign'] = campaign
        return context


class CharacterUpdateView(UpdateView):
    model = Character
    form_class = CharacterForm
    template_name = 'dnd_manager/create_character_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campaign_id = self.kwargs['campaign_id']
        campaign = Campaign.objects.get(pk=campaign_id)
        context['campaign'] = campaign
        return context

    def get_success_url(self):
        return reverse('campaign_detail', kwargs={'pk': self.kwargs['campaign_id']})


class CharacterDeleteView(DeleteView):
    model = Character
    template_name = 'dnd_manager/delete_character_confirm.html'

    def get_context_data(self, **kwargs):
        """We also want the campaign in the context for a link 
        back to the campaign detail if needed. """
        context = super().get_context_data(**kwargs)
        campaign_id = self.kwargs['campaign_id']
        campaign = Campaign.objects.get(pk=campaign_id)
        context['campaign'] = campaign
        return context

    def get_success_url(self):
        """Redirect to the Campaign detail page after deletion."""
        return reverse('campaign_detail', kwargs={'pk': self.kwargs['campaign_id']})
        

# # -----------------
# # NPC Views
# # -----------------
# class NPCListView(ListView):
#     model = NPC
#     template_name = 'campaign/npc_list.html'
#     context_object_name = 'npcs'


# class NPCDetailView(DetailView):
#     model = NPC
#     template_name = 'campaign/npc_detail.html'
#     context_object_name = 'npc'


# class NPCCreateView(CreateView):
#     model = NPC
#     form_class = NPCForm
#     template_name = 'campaign/npc_form.html'
#     success_url = reverse_lazy('npc_list')


# class NPCUpdateView(UpdateView):
#     model = NPC
#     form_class = NPCForm
#     template_name = 'campaign/npc_form.html'
#     success_url = reverse_lazy('npc_list')


# class NPCDeleteView(DeleteView):
#     model = NPC
#     template_name = 'campaign/npc_confirm_delete.html'
#     success_url = reverse_lazy('npc_list')


# # -----------------
# # Item Views
# # -----------------
# class ItemListView(ListView):
#     model = Item
#     template_name = 'campaign/item_list.html'
#     context_object_name = 'items'


# class ItemDetailView(DetailView):
#     model = Item
#     template_name = 'campaign/item_detail.html'
#     context_object_name = 'item'


# class ItemCreateView(CreateView):
#     model = Item
#     form_class = ItemForm
#     template_name = 'campaign/item_form.html'
#     success_url = reverse_lazy('item_list')


# class ItemUpdateView(UpdateView):
#     model = Item
#     form_class = ItemForm
#     template_name = 'campaign/item_form.html'
#     success_url = reverse_lazy('item_list')


# class ItemDeleteView(DeleteView):
#     model = Item
#     template_name = 'campaign/item_confirm_delete.html'
#     success_url = reverse_lazy('item_list')


# # -----------------
# # Quest Views
# # -----------------
# class QuestListView(ListView):
#     model = Quest
#     template_name = 'campaign/quest_list.html'
#     context_object_name = 'quests'


# class QuestDetailView(DetailView):
#     model = Quest
#     template_name = 'campaign/quest_detail.html'
#     context_object_name = 'quest'


# class QuestCreateView(CreateView):
#     model = Quest
#     form_class = QuestForm
#     template_name = 'campaign/quest_form.html'
#     success_url = reverse_lazy('quest_list')


# class QuestUpdateView(UpdateView):
#     model = Quest
#     form_class = QuestForm
#     template_name = 'campaign/quest_form.html'
#     success_url = reverse_lazy('quest_list')


# class QuestDeleteView(DeleteView):
#     model = Quest
#     template_name = 'campaign/quest_confirm_delete.html'
#     success_url = reverse_lazy('quest_list')


# # -----------------
# # AdventureLog Views
# # -----------------
# class AdventureLogListView(ListView):
#     model = AdventureLog
#     template_name = 'campaign/adventurelog_list.html'
#     context_object_name = 'adventurelogs'


# class AdventureLogDetailView(DetailView):
#     model = AdventureLog
#     template_name = 'campaign/adventurelog_detail.html'
#     context_object_name = 'adventurelog'


# class AdventureLogCreateView(CreateView):
#     model = AdventureLog
#     form_class = AdventureLogForm
#     template_name = 'campaign/adventurelog_form.html'
#     success_url = reverse_lazy('adventurelog_list')


# class AdventureLogUpdateView(UpdateView):
#     model = AdventureLog
#     form_class = AdventureLogForm
#     template_name = 'campaign/adventurelog_form.html'
#     success_url = reverse_lazy('adventurelog_list')


# class AdventureLogDeleteView(DeleteView):
#     model = AdventureLog
#     template_name = 'campaign/adventurelog_confirm_delete.html'
#     success_url = reverse_lazy('adventurelog_list')


# # -----------------
# # CalendarEvent Views
# # -----------------
# class CalendarEventListView(ListView):
#     model = CalendarEvent
#     template_name = 'campaign/event_list.html'
#     context_object_name = 'events'


# class CalendarEventDetailView(DetailView):
#     model = CalendarEvent
#     template_name = 'campaign/event_detail.html'
#     context_object_name = 'event'


# class CalendarEventCreateView(CreateView):
#     model = CalendarEvent
#     form_class = CalendarEventForm
#     template_name = 'campaign/event_form.html'
#     success_url = reverse_lazy('event_list')


# class CalendarEventUpdateView(UpdateView):
#     model = CalendarEvent
#     form_class = CalendarEventForm
#     template_name = 'campaign/event_form.html'
#     success_url = reverse_lazy('event_list')


# class CalendarEventDeleteView(DeleteView):
#     model = CalendarEvent
#     template_name = 'campaign/event_confirm_delete.html'
#     success_url = reverse_lazy('event_list')
