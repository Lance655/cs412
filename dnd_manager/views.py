from django.shortcuts import render, redirect

from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import (
    Campaign, Session, Character, NPC, Item, Quest, AdventureLog, CalendarEvent
)
from .forms import (
    CampaignForm, SessionForm, CharacterForm, NPCForm, 
    CreateItemForm, UpdateItemForm, QuestForm, AdventureLogForm, CalendarEventForm
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        session = self.get_object()
        # Pull all logs for this Session, as well as the related Character for each log
        context['adventure_logs'] = session.adventure_logs.select_related('character')
        return context


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
        return reverse('session_detail', kwargs={'campaign_id': self.kwargs['campaign_id'], 
                                                'pk': self.kwargs['pk']})


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

        # Add the character's items
        character = self.get_object()
        context['items_owned'] = character.items_owned.all()

        # Pull all logs for this Character, as well as the related Session of each log
        context['adventure_logs'] = character.adventure_logs.select_related('session')
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
        return reverse('character_list', kwargs={'campaign_id': self.kwargs['campaign_id']})

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
        return reverse('character_detail', kwargs={'campaign_id': self.kwargs['campaign_id'], 
                                                            'pk': self.kwargs['pk'] })


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


# -----------------
# NPC Views
# -----------------

class NPCListView(ListView):
    model = NPC
    template_name = 'dnd_manager/npc_list.html'
    context_object_name = 'npcs'

    def get_queryset(self):
        """Return only NPCs belonging to the given campaign_id."""
        campaign_id = self.kwargs['campaign_id']
        return NPC.objects.filter(campaign__id=campaign_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campaign_id = self.kwargs['campaign_id']
        campaign = Campaign.objects.get(pk=campaign_id)
        context['campaign'] = campaign
        return context

class NPCDetailView(DetailView):
    model = NPC
    template_name = 'dnd_manager/npc_detail.html'
    context_object_name = 'npc'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the Campaign to the template
        campaign_id = self.kwargs['campaign_id']
        campaign = Campaign.objects.get(pk=campaign_id)
        context['campaign'] = campaign
        return context


class NPCCreateView(CreateView):
    model = NPC
    form_class = NPCForm
    template_name = 'dnd_manager/create_npc_form.html'

    def form_valid(self, form):
        """Attach the correct Campaign before saving."""
        campaign_id = self.kwargs['campaign_id']
        campaign = Campaign.objects.get(pk=campaign_id)
        form.instance.campaign = campaign
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect to the campaign detail page."""
        return reverse('npc_list', kwargs={'campaign_id': self.kwargs['campaign_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campaign_id = self.kwargs['campaign_id']
        campaign = Campaign.objects.get(pk=campaign_id)
        context['campaign'] = campaign
        return context


class NPCUpdateView(UpdateView):
    model = NPC
    form_class = NPCForm
    template_name = 'dnd_manager/create_npc_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campaign_id = self.kwargs['campaign_id']
        campaign = Campaign.objects.get(pk=campaign_id)
        context['campaign'] = campaign
        return context

    def get_success_url(self):
        return reverse('npc_list', kwargs={'campaign_id': self.kwargs['campaign_id']})


class NPCDeleteView(DeleteView):
    model = NPC
    template_name = 'dnd_manager/delete_npc_confirm.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campaign_id = self.kwargs['campaign_id']
        campaign = Campaign.objects.get(pk=campaign_id)
        context['campaign'] = campaign
        return context

    def get_success_url(self):
        return reverse('npc_list', kwargs={'campaign_id': self.kwargs['campaign_id']})

    
# -----------------
# Item Views
# -----------------

class ItemCreateView(CreateView):
    model = Item
    form_class = CreateItemForm
    template_name = 'dnd_manager/create_item_form.html' 

    def form_valid(self, form):
        campaign_id = self.kwargs['campaign_id']
        character_id = self.kwargs['character_id']
        campaign = Campaign.objects.get(pk=campaign_id)
        character = Character.objects.get(pk=character_id)

        # Attach the campaign & character to this item
        form.instance.campaign = campaign
        form.instance.owner_character = character

        # To ensure there's no conflict, clear out owner_npc:
        form.instance.owner_npc = None  

        return super().form_valid(form)

    def get_success_url(self):
        # After creation, go back to the Character’s detail page
        return reverse('character_detail', kwargs={
            'campaign_id': self.kwargs['campaign_id'],
            'pk': self.kwargs['character_id']
        })

    def get_context_data(self, **kwargs):
        """Pass the Campaign into the template context."""
        context = super().get_context_data(**kwargs)
        campaign_id = self.kwargs['campaign_id']
        campaign = Campaign.objects.get(pk=campaign_id)
        context['campaign'] = campaign

        character_id = self.kwargs['character_id']
        character = Character.objects.get(pk=character_id)
        context['character'] = character

        return context


class ItemUpdateView(UpdateView):
    model = Item
    form_class = UpdateItemForm
    template_name = 'dnd_manager/create_item_form.html'

    def get_context_data(self, **kwargs):
        """Pass the Campaign into the template context."""
        context = super().get_context_data(**kwargs)
        campaign_id = self.kwargs['campaign_id']
        campaign = Campaign.objects.get(pk=campaign_id)
        context['campaign'] = campaign

        character_id = self.kwargs['character_id']
        character = Character.objects.get(pk=character_id)
        context['character'] = character

        return context

    def get_success_url(self):
        return reverse('character_detail', kwargs={
            'campaign_id': self.kwargs['campaign_id'],
            'pk': self.kwargs['character_id']
        })


class ItemDeleteView(DeleteView):
    model = Item
    template_name = 'dnd_manager/delete_item_confirm.html'

    def get_success_url(self):
        return reverse('character_detail', kwargs={
            'campaign_id': self.kwargs['campaign_id'],
            'pk': self.kwargs['character_id']
        })
    
    def get_context_data(self, **kwargs):
        """Pass the Campaign into the template context."""
        context = super().get_context_data(**kwargs)
        campaign_id = self.kwargs['campaign_id']
        campaign = Campaign.objects.get(pk=campaign_id)
        context['campaign'] = campaign

        character_id = self.kwargs['character_id']
        character = Character.objects.get(pk=character_id)
        context['character'] = character

        return context

def item_sell_view(request, campaign_id, character_id, pk):
    item = Item.objects.get(pk=pk)
    character = Character.objects.get(pk=character_id)
    campaign = Campaign.objects.get(pk=campaign_id)
    # verify the item.owner_character == this character?

    if request.method == 'POST':
        # user confirmed selling
        character.gold += item.price
        character.save()

        item.owner_character = None
        item.save()
        # item.delete()?

        return redirect('character_detail', campaign_id=campaign_id, pk=character_id)
    else:
        # Show confirmation page
        return render(request, 'dnd_manager/item_sell_confirm.html', {
            'campaign': campaign,
            'character': character,
            'item': item
        })



# -----------------
# Adventure Log Views
# -----------------



class AdventureLogCreateView(CreateView):
    model = AdventureLog
    form_class = AdventureLogForm
    template_name = 'dnd_manager/adventure_log_form.html'

    def form_valid(self, form):
        """Assign the correct character to this log."""

        character_id = self.kwargs['character_id']
        character = Character.objects.get(pk=character_id)

        # Set the character on the form instance
        form.instance.character = character

        return super().form_valid(form)

    def get_success_url(self):
        """Redirect back to the Character Detail page."""
        return reverse('character_detail', kwargs={
            'campaign_id': self.kwargs['campaign_id'],
            'pk': self.kwargs['character_id']
        })

    def get_context_data(self, **kwargs):
        """Provide the campaign & character for the template."""
        context = super().get_context_data(**kwargs)
        context['campaign_id'] = self.kwargs['campaign_id']
        context['character_id'] = self.kwargs['character_id']
        return context




# class CharacterDetailView(DetailView):
#     model = Character
#     template_name = 'dnd_manager/character_detail.html'
#     context_object_name = 'character'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # Pass the Campaign to the template
#         campaign_id = self.kwargs['campaign_id']
#         campaign = Campaign.objects.get(pk=campaign_id)
#         context['campaign'] = campaign
#         return context

# class CharacterListView(ListView):
#     model = Character
#     template_name = 'dnd_manager/character_list.html'
#     context_object_name = 'characters'

#     def get_queryset(self):
#         """Return only Characters belonging to the given campaign_id."""
#         campaign_id = self.kwargs['campaign_id']
#         return Character.objects.filter(campaign__id=campaign_id)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         campaign_id = self.kwargs['campaign_id']
#         campaign = Campaign.objects.get(pk=campaign_id)
#         context['campaign'] = campaign
#         return context



# class CharacterCreateView(CreateView):
#     model = Character
#     form_class = CharacterForm
#     template_name = 'dnd_manager/create_character_form.html'

#     def form_valid(self, form):
#         """Assign the correct Campaign via the URL param before saving."""
#         campaign_id = self.kwargs['campaign_id']
#         campaign = Campaign.objects.get(pk=campaign_id)
#         form.instance.campaign = campaign
#         return super().form_valid(form)

#     def get_success_url(self):
#         """After creating a Character, go back to the Campaign detail page."""
#         return reverse('campaign_detail', kwargs={'pk': self.kwargs['campaign_id']})

#     def get_context_data(self, **kwargs):
#         """Pass the Campaign into the template context."""
#         context = super().get_context_data(**kwargs)
#         campaign_id = self.kwargs['campaign_id']
#         campaign = Campaign.objects.get(pk=campaign_id)
#         context['campaign'] = campaign
#         return context