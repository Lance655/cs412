import requests

from django.shortcuts import render, redirect

from django.db.models import Sum
from django.db.models.functions import Coalesce

from collections import defaultdict

from django.urls import reverse_lazy, reverse

from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import (
    Campaign, Session, Character, NPC, Item, Quest, AdventureLog, CalendarEvent,
)
from .forms import (
    CampaignForm, SessionForm, CharacterForm, NPCForm, 
    CreateItemForm, UpdateItemForm, QuestForm, AdventureLogForm, CalendarEventForm,
    CreateGeneralItemForm, GeneralCharacterForm,
)

from django.contrib.auth.mixins import LoginRequiredMixin ## NEW
from django.contrib.auth.models import User ## NEW
from django.contrib.auth.forms import UserCreationForm ## NEW
from django.contrib.auth import login
from django.http import JsonResponse




class MyLoginRequiredMixin(LoginRequiredMixin):
    '''Class to create a custom mixin for logins'''
    def get_login_url(self):
        '''Redirect to the login page'''
        return reverse('login')

class DMOnlyMixin:
    """
    Restrict access to DM only.
    Requires the object has a campaign field with a .dm user.
    """
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user.is_staff or request.user == obj.campaign.dm:
            return super().dispatch(request, *args, **kwargs)

        return redirect('campaign_list')

class DMCreateOnlyMixin:
    """
    Mixin for create views that only staff or DM can create a new object.
    """
    def dispatch(self, request, *args, **kwargs):
        """Method to check if the user has permissions to create certain views"""
        # Attempt to fetch campaign_id from URL kwargs
        campaign_id = kwargs.get('campaign_id')
        if campaign_id is None:
            # If there's no campaign, fall back to staff check or deny
            if not request.user.is_staff:
                return redirect('campaign_list')
            return super().dispatch(request, *args, **kwargs)

        # Retrieve the Campaign using the ID
        campaign = Campaign.objects.get(pk=campaign_id)

        # Check if user is staff or campaign DM
        if request.user.is_staff or request.user == campaign.dm:
            # Allowed
            return super().dispatch(request, *args, **kwargs)

        # Otherwise, deny
        return redirect('campaign_list')


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

        # base queryset with totals
        # use coalesce so that if a character does not have any logs, it will default the fields to 0
        # use annotate to add calculated fields to each object in the queryset.
        chars = (Character.objects
                .filter(campaign=campaign)
                .annotate(
                    total_kills = Coalesce(Sum('adventure_logs__enemies_killed'), 0),
                    total_downs = Coalesce(Sum('adventure_logs__number_of_downs'), 0)
                ))

        # three leaderboards, each already sorted desc
        context["lb_gold"]   = chars.order_by("-gold",          "name")
        context["lb_kills"]  = chars.order_by("-total_kills",   "name")
        context["lb_downs"]  = chars.order_by("-total_downs",   "name")


        context['sessions'] = campaign.sessions.all()
        context['characters'] = campaign.characters.all()
        context['items'] = campaign.items.all()
        context['npcs'] = campaign.npcs.all()
        context['quests'] = campaign.quests.all()
        context['events'] = campaign.events.all()


        # context["user_characters_alive"] = campaign.characters.filter(
        #     user=self.request.user,
        #     status='alive'
        # )

        return context


class CampaignCreateView(MyLoginRequiredMixin, CreateView):
    model = Campaign
    form_class = CampaignForm
    template_name = 'dnd_manager/create_campaign_form.html'

    def form_valid(self, form):
        """Make the user creating a new campaign the DM for that campaign"""
        # find the logged in user
        user = self.request.user
        form.instance.dm = user

        return super().form_valid(form)

    def get_success_url(self):
        """Redirect back to the campaign list."""
        return reverse('campaign_list')
        


class CampaignUpdateView(MyLoginRequiredMixin, UpdateView):
    model = Campaign
    form_class = CampaignForm
    template_name = 'dnd_manager/create_campaign_form.html'

    def dispatch(self, request, *args, **kwargs):
        """Method to check whether user is the DM or a player"""
        campaign = self.get_object()

        # Only the DM or staff can update the campaign:
        if request.user.is_staff or request.user == campaign.dm:
            return super().dispatch(request, *args, **kwargs)

        # Block the user otherwise
        return redirect('campaign_list')


    def get_success_url(self):
        """Redirect back to the campaign list."""
        return reverse('campaign_list')


class CampaignDeleteView(MyLoginRequiredMixin, DeleteView):
    model = Campaign
    template_name = 'dnd_manager/delete_campaign_confirm.html'

    def dispatch(self, request, *args, **kwargs):
        """Method to check whether user is the DM or a player"""
        campaign = self.get_object()

        # Only the DM or staff can delete a campaign:
        if request.user.is_staff or request.user == campaign.dm:
            return super().dispatch(request, *args, **kwargs)

        # Block the user otherwise
        return redirect('campaign_list')


    def get_success_url(self):
        """Redirect back to the campaign list."""
        return reverse('campaign_list')


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

        campaign_id = self.kwargs['campaign_id']
        campaign = Campaign.objects.get(pk=campaign_id)
        context['campaign'] = campaign

        return context


class SessionCreateView(MyLoginRequiredMixin, DMCreateOnlyMixin, CreateView):
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


class SessionUpdateView(MyLoginRequiredMixin, DMOnlyMixin, UpdateView):
    model = Session
    form_class = SessionForm
    template_name = 'dnd_manager/create_session_form.html'

    def get_context_data(self, **kwargs):
        """Make sure we include the campaign in the context for the template."""
        context = super().get_context_data(**kwargs)
        campaign_id = self.kwargs['campaign_id']
        campaign = Campaign.objects.get(pk=campaign_id)

        session_id = self.kwargs['pk']
        session = Session.objects.get(pk=session_id)

        context['campaign'] = campaign
        context['session'] = session

        return context

    def get_success_url(self):
        """Redirect back to the session list (or campaign detail)."""
        return reverse('session_detail', kwargs={'campaign_id': self.kwargs['campaign_id'], 
                                                'pk': self.kwargs['pk']})


class SessionDeleteView(MyLoginRequiredMixin, DMOnlyMixin, DeleteView):
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


class CharacterCreateView(MyLoginRequiredMixin, CreateView):
    model = Character
    form_class = CharacterForm
    template_name = 'dnd_manager/create_character_form.html'

    def form_valid(self, form):
        """Assign the correct Campaign via the URL param before saving. 
        Also add corresponding user
        """
        campaign_id = self.kwargs['campaign_id']
        campaign = Campaign.objects.get(pk=campaign_id)
        form.instance.campaign = campaign

        # find the logged in user
        user = self.request.user
        form.instance.user = user

        return super().form_valid(form)

    def get_success_url(self):
        """After creating a Character, go back to the Campaign detail page."""
        return reverse('my_characters', kwargs={'campaign_id': self.kwargs['campaign_id']})

    def get_context_data(self, **kwargs):
        """Pass the Campaign into the template context."""
        context = super().get_context_data(**kwargs)
        campaign_id = self.kwargs['campaign_id']
        campaign = Campaign.objects.get(pk=campaign_id)
        context['campaign'] = campaign

        return context


class CharacterUpdateView(MyLoginRequiredMixin, UpdateView):
    model = Character
    form_class = CharacterForm
    template_name = 'dnd_manager/create_character_form.html'

    def dispatch(self, request, *args, **kwargs):
        """Method to check whether user is the DM or a player"""
        character = self.get_object()

        # Only the DM or staff can update the character:
        if request.user.is_staff or request.user == character.campaign.dm:
            return super().dispatch(request, *args, **kwargs)
        if character.user == request.user:
            return super().dispatch(request, *args, **kwargs)
        
        # Block the user otherwise
        return redirect('campaign_list')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campaign_id = self.kwargs['campaign_id']
        campaign = Campaign.objects.get(pk=campaign_id)
        context['campaign'] = campaign

        character_id = self.kwargs['pk']
        character = Character.objects.get(pk=character_id)
        context['character'] = character
        return context

    def get_success_url(self):
        return reverse('character_detail', kwargs={'campaign_id': self.kwargs['campaign_id'], 
                                                            'pk': self.kwargs['pk'] })


class CharacterDeleteView(MyLoginRequiredMixin, DeleteView):
    model = Character
    template_name = 'dnd_manager/delete_character_confirm.html'

    def dispatch(self, request, *args, **kwargs):
        """Method to check whether user is the DM or a player"""
        character = self.get_object()

        # Only the DM or staff can delete a character:
        if request.user.is_staff or request.user == character.campaign.dm:
            return super().dispatch(request, *args, **kwargs)
        if character.user == request.user:
            return super().dispatch(request, *args, **kwargs)
        
        # Block the user otherwise
        return redirect('campaign_list')
    

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

        campaign_id = self.kwargs['campaign_id']
        campaign = Campaign.objects.get(pk=campaign_id)
        if self.request.user == campaign.dm:
            return reverse('character_list', kwargs={'campaign_id': self.kwargs['campaign_id']})

        return reverse('my_characters', kwargs={'campaign_id': self.kwargs['campaign_id']})


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


class NPCCreateView(MyLoginRequiredMixin, DMCreateOnlyMixin, CreateView):
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


class NPCUpdateView(MyLoginRequiredMixin, DMOnlyMixin, UpdateView):
    model = NPC
    form_class = NPCForm
    template_name = 'dnd_manager/create_npc_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campaign_id = self.kwargs['campaign_id']
        campaign = Campaign.objects.get(pk=campaign_id)

        npc_id = self.kwargs['pk']
        npc = NPC.objects.get(pk=npc_id)


        context['campaign'] = campaign
        context['npc'] = npc

        return context

    def get_success_url(self):
        return reverse('npc_list', kwargs={'campaign_id': self.kwargs['campaign_id']})


class NPCDeleteView(MyLoginRequiredMixin, DMOnlyMixin, DeleteView):
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


class ItemListView(ListView):
    model = Item
    template_name = 'dnd_manager/item_list.html'
    context_object_name = 'items'

    # ---------- filtering ----------
    def get_queryset(self):
        qs = (Item.objects
                    .filter(campaign_id=self.kwargs['campaign_id'])
                    .select_related('owner_character', 'owner_npc'))

        # type
        item_type = self.request.GET.get('type')
        if item_type:
            qs = qs.filter(item_type=item_type)

        # rarity
        rarity = self.request.GET.get('rarity')
        if rarity:
            qs = qs.filter(rarity=rarity)

        # owner
        owner_id = self.request.GET.get('owner')
        if owner_id:
            qs = qs.filter(owner_character_id=owner_id) | qs.filter(owner_npc_id=owner_id)
            

        # default ordering
        return qs.order_by('item_type', 'name')

    def get_available_owners(self):
        """Helper function to get only item owners from this campaign"""
        campaign_id = self.kwargs['campaign_id']
        chars = Character.objects.filter(campaign_id=campaign_id).values('id', 'name')
        npcs  = NPC.objects.filter(campaign_id=campaign_id).values('id', 'name')
        # tag them to know which is which 
        return [('C'+str(c['id']), c['name']) for c in chars] + \
            [('N'+str(n['id']), n['name']) for n in npcs]

    # ---------- grouping ----------
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campaign = Campaign.objects.get(pk=self.kwargs['campaign_id'])
        context['campaign'] = campaign

        char_groups = defaultdict(list)
        npc_groups  = defaultdict(list)
        unowned     = []

        for item in self.object_list:
            if item.owner_character:
                char_groups[item.owner_character].append(item)
            elif item.owner_npc:
                npc_groups[item.owner_npc].append(item)
            else:
                unowned.append(item)

        # convert to something template‑friendly
        context['char_items'] = list(char_groups.items())   # [(Character, [items])]
        context['npc_items']  = list(npc_groups.items())    # [(NPC, [items])]
        context['unowned']    = unowned

        context['owner_choices'] = self.get_available_owners()

        # make choices available to the template
        context["item_type_choices"] = Item.ITEM_TYPE_CHOICES
        context["rarity_choices"]     = Item.RARITY_CHOICES


        return context


class ItemDetailView(DetailView):
    model = Item
    template_name = "dnd_manager/item_detail.html"
    context_object_name = "item"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campaign = Campaign.objects.get(pk=self.kwargs["campaign_id"])
        context["campaign"] = campaign
        return context


class ItemCreateView(MyLoginRequiredMixin, CreateView):
    model = Item
    form_class = CreateItemForm
    template_name = 'dnd_manager/create_item_form.html' 

    def dispatch(self, request, *args, **kwargs):
        """
        Only allow the DM or the specified Character’s user to create an item
        for their character.
        """
        # Fetch the campaign & character from URL params
        campaign_id = self.kwargs['campaign_id']
        character_id = self.kwargs['character_id']

        campaign = Campaign.objects.get(pk=campaign_id)
        character = Character.objects.get(pk=character_id, campaign=campaign)

        # Check if user is the DM or the character's owner
        if request.user == campaign.dm or request.user == character.user:
            return super().dispatch(request, *args, **kwargs)

        # If neither, block access
        return redirect("campaign_list")


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


class ItemUpdateView(MyLoginRequiredMixin, UpdateView):
    model = Item
    form_class = UpdateItemForm
    template_name = 'dnd_manager/create_item_form.html'

    def dispatch(self, request, *args, **kwargs):
        """Method to find whether user is DM or player"""
        item = self.get_object()  
        
        # DM can edit any item in the campaign, or the item’s owner (if owned by a character).
        if request.user == item.campaign.dm:
            return super().dispatch(request, *args, **kwargs)
        if item.owner_character and request.user == item.owner_character.user:
            return super().dispatch(request, *args, **kwargs)
        
        # If neither condition is true, block them
        return redirect('campaign_list')

    def get_form(self, form_class=None):
        """
        Override get_form() to filter the Item field's queryset
        so that it only shows Characters for the correct campaign.
        """
        form = super().get_form(form_class)
        
        # Fetch the relevant Campaign from the URL
        campaign_id = self.kwargs['campaign_id']
        campaign = Campaign.objects.get(pk=campaign_id)

        # Restrict the Character dropdown to only characters from this campaign
        form.fields['owner_character'].queryset = Character.objects.filter(campaign=campaign)

        return form

    def get_context_data(self, **kwargs):
        """Pass the Campaign into the template context."""
        context = super().get_context_data(**kwargs)
        campaign_id = self.kwargs['campaign_id']
        campaign = Campaign.objects.get(pk=campaign_id)
        context['campaign'] = campaign

        character_id = self.kwargs['character_id']
        character = Character.objects.get(pk=character_id)
        context['character'] = character
        
        item_id = self.kwargs['pk']
        item = Item.objects.get(pk=item_id)
        context['item'] = item

        return context

    def get_success_url(self):
        return reverse('character_detail', kwargs={
            'campaign_id': self.kwargs['campaign_id'],
            'pk': self.kwargs['character_id']
        })


class ItemDeleteView(MyLoginRequiredMixin, DeleteView):
    model = Item
    template_name = 'dnd_manager/delete_item_confirm.html'

    def dispatch(self, request, *args, **kwargs):
        """Method to find whether user is DM or player"""
        item = self.get_object()  
        
        # DM can edit any item in the campaign, or the item’s owner (if owned by a character).
        if request.user == item.campaign.dm:
            return super().dispatch(request, *args, **kwargs)
        if item.owner_character and request.user == item.owner_character.user:
            return super().dispatch(request, *args, **kwargs)
        
        # If neither condition is true, block them
        return redirect('campaign_list')

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

    # Check if item is actually owned by this character
    if item.owner_character != character:
        # block otherwise
        return redirect ("campaign_list")

    # Check if the current user is either DM or the character owner
    if request.user != campaign.dm and request.user != character.user:
        return redirect ("campaign_list")


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
# General Item Views
# -----------------



class ItemCreateGeneralView(MyLoginRequiredMixin, DMCreateOnlyMixin, CreateView):
    model = Item
    form_class = CreateGeneralItemForm
    template_name = 'dnd_manager/create_item_general_form.html' 

    def form_valid(self, form):
        campaign_id = self.kwargs['campaign_id']
        campaign = Campaign.objects.get(pk=campaign_id)

        # Attach the campaign to this item
        form.instance.campaign = campaign 

        return super().form_valid(form)

    def get_success_url(self):
        # After creation, go back to the Item's detail page -->
        # NOT THE CHARACTER's PAGE: 
        return reverse('item_list', kwargs={
            'campaign_id': self.kwargs['campaign_id'],
        })

    def get_context_data(self, **kwargs):
        """Pass the Campaign into the template context."""
        context = super().get_context_data(**kwargs)
        campaign_id = self.kwargs['campaign_id']
        campaign = Campaign.objects.get(pk=campaign_id)
        context['campaign'] = campaign

        # DOESN'T HAVE CHARACTER ID: 
        # character_id = self.kwargs['character_id']
        # character = Character.objects.get(pk=character_id)
        # context['character'] = character

        return context


class ItemUpdateGeneralView(MyLoginRequiredMixin, DMOnlyMixin, UpdateView):
    model = Item
    form_class = CreateGeneralItemForm
    template_name = 'dnd_manager/create_item_general_form.html' 

    def get_form(self, form_class=None):
        """
        Override get_form() to filter the Item field's queryset
        so that it only shows Characters for the correct campaign.
        """
        form = super().get_form(form_class)
        
        # Fetch the relevant Campaign from the URL
        campaign_id = self.kwargs['campaign_id']
        campaign = Campaign.objects.get(pk=campaign_id)

        # Restrict the Character dropdown to only characters from this campaign
        form.fields['owner_character'].queryset = Character.objects.filter(campaign=campaign)
        form.fields['owner_npc'].queryset = NPC.objects.filter(campaign=campaign)

        return form

    def get_context_data(self, **kwargs):
        """Pass the Campaign into the template context."""
        context = super().get_context_data(**kwargs)
        campaign_id = self.kwargs['campaign_id']
        campaign = Campaign.objects.get(pk=campaign_id)
        context['campaign'] = campaign

        item_id = self.kwargs['pk']
        item = Item.objects.get(pk=item_id)
        context['item'] = item

        return context

    def get_success_url(self):
        return reverse('item_detail', kwargs={
            'campaign_id': self.kwargs['campaign_id'],
            'pk': self.kwargs['pk']
        })


class ItemDeleteGeneralView(MyLoginRequiredMixin, DMOnlyMixin, DeleteView):
    model = Item
    template_name = 'dnd_manager/delete_item_general_confirm.html'

    def get_success_url(self):
        return reverse('item_list', kwargs={
            'campaign_id': self.kwargs['campaign_id'],
        })
    
    def get_context_data(self, **kwargs):
        """Pass the Campaign into the template context."""
        context = super().get_context_data(**kwargs)
        campaign_id = self.kwargs['campaign_id']
        campaign = Campaign.objects.get(pk=campaign_id)
        context['campaign'] = campaign

        return context



# -----------------
# Adventure Log Views
# -----------------


class AdventureLogCreateView(MyLoginRequiredMixin, CreateView):
    model = AdventureLog
    form_class = AdventureLogForm
    template_name = 'dnd_manager/create_adventure_log_form.html'


    def dispatch(self, request, *args, **kwargs):
        """Method to check whether user id DM or a player"""

        # Fetch campaign & character from the URL
        campaign_id = self.kwargs['campaign_id']
        character_id = self.kwargs['character_id']

        campaign = Campaign.objects.get(pk=campaign_id)
        character = Character.objects.get(pk=character_id, campaign=campaign)

        # Check if user is DM or the character’s owner
        if request.user != campaign.dm and request.user != character.user:
            return redirect("campaign_list")

        return super().dispatch(request, *args, **kwargs)


    def get_form(self, form_class=None):
        """
        Override get_form() to filter the Session field's queryset
        so that it only shows Sessions for the correct campaign.
        """

        form = super().get_form(form_class)
        
        # Fetch the relevant Campaign from the URL
        campaign_id = self.kwargs['campaign_id']
        campaign = Campaign.objects.get(pk=campaign_id)

        # Restrict the Session dropdown to only sessions from this campaign
        form.fields['session'].queryset = Session.objects.filter(campaign=campaign)

        return form

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
        character_id  = self.kwargs['character_id']
        campaign_id = self.kwargs['campaign_id']

        campaign = Campaign.objects.get(pk=campaign_id)
        character = Character.objects.get(pk=character_id)

        context['campaign'] = campaign
        context['character'] = character

        return context

class AdventureLogUpdateView(MyLoginRequiredMixin, UpdateView):
    model = AdventureLog
    form_class = AdventureLogForm
    template_name = 'dnd_manager/create_adventure_log_form.html'

    def dispatch(self, request, *args, **kwargs):
        """Method to find whether user is DM or player"""

        log = self.get_object()  
        character = log.character
        campaign = character.campaign

        # Check if user is DM or the character owner
        if request.user != campaign.dm and request.user != character.user:
            return redirect("campaign_list")

        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        """
        Override get_form() to filter the Session field's queryset
        so that it only shows Sessions for the correct campaign.
        """

        form = super().get_form(form_class)
        
        # Fetch the relevant Campaign from the URL
        campaign_id = self.kwargs['campaign_id']
        campaign = Campaign.objects.get(pk=campaign_id)

        # Restrict the Session dropdown to only sessions from this campaign
        form.fields['session'].queryset = Session.objects.filter(campaign=campaign)

        return form

    def get_queryset(self):
        """Ensure we only get logs that match the campaign & character in the URL."""
        campaign_id = self.kwargs['campaign_id']
        character_id = self.kwargs['character_id']
        return AdventureLog.objects.filter(character__id=character_id, character__campaign__id=campaign_id)

    def get_success_url(self):
        """Redirect back to the Character Detail page."""
        return reverse('character_detail', kwargs={
            'campaign_id': self.kwargs['campaign_id'],
            'pk': self.kwargs['character_id']
        })

    def get_context_data(self, **kwargs):
        """Provide the campaign & character for the template."""
        context = super().get_context_data(**kwargs)
        character_id  = self.kwargs['character_id']
        campaign_id = self.kwargs['campaign_id']

        campaign = Campaign.objects.get(pk=campaign_id)
        character = Character.objects.get(pk=character_id)

        context['campaign'] = campaign
        context['character'] = character

        return context

class AdventureLogDeleteView(MyLoginRequiredMixin, DeleteView):
    model = AdventureLog
    template_name = 'dnd_manager/delete_adventure_log_confirm.html'

    def dispatch(self, request, *args, **kwargs):
        """Method to find whether user is DM or player"""
        
        log = self.get_object()  
        character = log.character
        campaign = character.campaign

        # Check if user is DM or the character owner
        if request.user != campaign.dm and request.user != character.user:
            return redirect("campaign_list")

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """Ensure we only fetch logs that belong to the correct character."""
        campaign_id = self.kwargs['campaign_id']
        character_id = self.kwargs['character_id']
        return AdventureLog.objects.filter(character__id=character_id, character__campaign__id=campaign_id)

    def get_success_url(self):
        """After deleting, go back to the character detail."""
        return reverse('character_detail', kwargs={
            'campaign_id': self.kwargs['campaign_id'],
            'pk': self.kwargs['character_id']
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['campaign_id'] = self.kwargs['campaign_id']
        context['character_id'] = self.kwargs['character_id']
        return context


# -----------------
# Quest Views
# -----------------

class QuestListView(ListView):
    model = Quest
    template_name = 'dnd_manager/quest_list.html'
    context_object_name = 'quests'

    def get_queryset(self):
        """Return quests only belonging to this campaign, with the proper filters"""
        qs = Quest.objects.filter(campaign_id=self.kwargs['campaign_id'])

        # ----- apply filters ----------
        status = self.request.GET.get('status')
        if status:
            qs = qs.filter(status=status)

        quest_type = self.request.GET.get('quest_type')
        if quest_type:
            qs = qs.filter(quest_type=quest_type)

        npc_id = self.request.GET.get('npc')
        if npc_id:
            qs = qs.filter(related_npc_id=npc_id)

        # ---- default ordering ----------
        qs = qs.order_by('quest_date')  
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        campaign_id = self.kwargs['campaign_id']
        campaign = Campaign.objects.get(pk=campaign_id)
        context['campaign'] = campaign

        qs = self.object_list 

        # Separate queries: main quests vs. personal quests
        main_quests = qs.filter(
            campaign=campaign,
            quest_type='Main Quest'
        ).order_by('quest_date')  # Oldest to earliest

        context['main_quests'] = main_quests

        # ───── PERSONAL quests grouped per character ─────
        #
        # 1) Fetch all personal quests in one query.
        personal_qs = (qs.filter(
            campaign=campaign, 
            quest_type='Personal Quest')
        .order_by('quest_date'))

        # 2) Build a dict  {character --> [quest, quest, ...]}
        personal_by_character = defaultdict(list)
        for quest in personal_qs:
            for char in quest.assigned_to.all():
                personal_by_character[char].append(quest)

        # 3) Add that to the template
        context['personal_by_character'] = list(personal_by_character.items())


        return context


class QuestDetailView(DetailView):
    model = Quest
    template_name = 'dnd_manager/quest_detail.html'
    context_object_name = 'quest'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # pass the Campaign to the template
        campaign_id = self.kwargs['campaign_id']
        campaign = Campaign.objects.get(pk=campaign_id)
        context['campaign'] = campaign
        return context

class QuestCreateView(MyLoginRequiredMixin, DMCreateOnlyMixin, CreateView):
    model = Quest
    form_class = QuestForm
    template_name = 'dnd_manager/create_quest_form.html'

    def get_form(self, form_class=None):
        """
        Override get_form() to filter the assigned to field's queryset
        so that it only shows characters for the correct campaign.
        """
        form = super().get_form(form_class)
        
        # Fetch the relevant Campaign from the URL
        campaign_id = self.kwargs['campaign_id']
        campaign = Campaign.objects.get(pk=campaign_id)

        # Restrict the Session dropdown to only sessions from this campaign
        form.fields['assigned_to'].queryset = Character.objects.filter(campaign=campaign)
        form.fields['related_npc'].queryset = NPC.objects.filter(campaign=campaign)


        return form

    def form_valid(self, form):
        """
        Attach the correct Campaign from the URL before saving.
        """
        campaign_id = self.kwargs['campaign_id']
        campaign = Campaign.objects.get(pk=campaign_id)
        form.instance.campaign = campaign
        return super().form_valid(form)

    def get_success_url(self):
        """
        Redirect to the quest list after creation.
        """
        return reverse('quest_list', kwargs={'campaign_id': self.kwargs['campaign_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campaign_id = self.kwargs['campaign_id']
        campaign = Campaign.objects.get(pk=campaign_id)
        context['campaign'] = campaign
        return context

class QuestUpdateView(MyLoginRequiredMixin, DMOnlyMixin, UpdateView):
    model = Quest
    form_class = QuestForm
    template_name = 'dnd_manager/create_quest_form.html'

    def get_form(self, form_class=None):
        """
        Override get_form() to filter the assigned to field's queryset
        so that it only shows characters for the correct campaign.
        """
        form = super().get_form(form_class)
        
        # Fetch the relevant Campaign from the URL
        campaign_id = self.kwargs['campaign_id']
        campaign = Campaign.objects.get(pk=campaign_id)

        # Restrict the Session dropdown to only sessions from this campaign
        form.fields['assigned_to'].queryset = Character.objects.filter(campaign=campaign)
        form.fields['related_npc'].queryset = NPC.objects.filter(campaign=campaign)


        return form

    def get_queryset(self):
        """
        Ensure we only fetch Quests that belong to the correct campaign.
        """
        campaign_id = self.kwargs['campaign_id']
        return Quest.objects.filter(campaign__id=campaign_id)

    def get_success_url(self):
        return reverse('quest_detail', kwargs={
            'campaign_id': self.kwargs['campaign_id'],
            'pk': self.kwargs['pk']
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campaign_id = self.kwargs['campaign_id']
        campaign = Campaign.objects.get(pk=campaign_id)
        context['campaign'] = campaign

        quest_id = self.kwargs['pk']
        quest = Quest.objects.get(pk=quest_id)
        context['quest'] = quest
        
        return context

class QuestDeleteView(MyLoginRequiredMixin, DMOnlyMixin, DeleteView):
    model = Quest
    template_name = 'dnd_manager/delete_quest_confirm.html'

    def get_queryset(self):
        """
        Ensure we only delete Quests that belong to the correct campaign.
        """
        campaign_id = self.kwargs['campaign_id']
        return Quest.objects.filter(campaign__id=campaign_id)

    def get_success_url(self):
        """
        After deleting, redirect to the quest list.
        """
        return reverse('quest_list', kwargs={'campaign_id': self.kwargs['campaign_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campaign_id = self.kwargs['campaign_id']
        campaign = Campaign.objects.get(pk=campaign_id)
        context['campaign'] = campaign
        return context


# -----------------
# Registration
# -----------------

class UserRegistrationView(CreateView):
    '''A view to show/process the registration form to create a new User.'''

    template_name = 'dnd_manager/register.html'
    form_class = UserCreationForm
    model = User

    def form_valid(self, form):
        user = form.save()
        # Automatically log the user in
        login(self.request, user)
        return redirect('campaign_list')

    # def get_success_url(self):
    #     '''The url to redirect to after creating a new User'''
    #     return reverse('campaign_list')


# -----------------
# Multiple Characters
# -----------------


class MyCharactersListView(MyLoginRequiredMixin, ListView):
    model = Character
    template_name = 'dnd_manager/my_characters_list.html'
    context_object_name = 'characters'

    def get_queryset(self):
        """Return only this user’s characters for the given campaign."""
        campaign_id = self.kwargs['campaign_id']
        return Character.objects.filter(
            campaign_id=campaign_id,
            user=self.request.user,
        )

    def get_context_data(self, **kwargs):
        """Pass along the campaign to the template as well."""
        context = super().get_context_data(**kwargs)
        campaign_id = self.kwargs['campaign_id']
        campaign = Campaign.objects.get(pk=campaign_id)
        context['campaign'] = campaign

        context["user_characters"] = campaign.characters.filter(
            user=self.request.user,
        )

        return context


# -----------------
# General Create Character / General Delete Character
# -----------------

class CharacterGeneralCreateView(MyLoginRequiredMixin, CreateView):
    model = Character
    form_class = GeneralCharacterForm
    template_name = 'dnd_manager/create_character_general_form.html'

    def dispatch(self, request, *args, **kwargs):
        """Method to check whether user is the DM or a player"""

        campaign_id = self.kwargs['campaign_id']
        campaign = Campaign.objects.get(pk=campaign_id)
        
        # Only the DM or staff can create a character through the general page:
        if request.user.is_staff or request.user == campaign.dm:
            return super().dispatch(request, *args, **kwargs)
        
        # Otherwise, block the user
        return redirect('campaign_list')
    

    def form_valid(self, form):
        """Assign the correct Campaign via the URL param before saving. 
        """
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


# -----------------
#  Map
# -----------------

class CampaignMapView(DetailView):
    model = Campaign
    template_name = 'dnd_manager/campaign_map.html'
    context_object_name = 'campaign'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 
        return context


# -----------------
#  References (API)
# -----------------

def references_search_view(request, campaign_id):
    """
    Show a search bar and a list of matching monsters/spells from the 5e-bits API.
    """
    search_type = request.GET.get('type', 'monster').lower()  # "monster" or "spell"
    search_query = request.GET.get('search', '').strip()

    list_results = None
    error = None

    # Base URL for the list endpoint:
    if search_type == 'monster':
        base_url = "https://www.dnd5eapi.co/api/2014/monsters"
    else:
        base_url = "https://www.dnd5eapi.co/api/2014/spells"

    if search_query:
        # call GET /monsters?name=dragon
        try:
            response = requests.get(base_url, params={'name': search_query}, headers={'Accept': 'application/json'})
            if response.status_code == 200:
                json_data = response.json()
                list_results = json_data.get('results', [])
                if not list_results:
                    error = f"No {search_type}s found matching '{search_query}'."
            else:
                error = f"Could not retrieve {search_type} list. (Status {response.status_code})"
        except requests.exceptions.RequestException as e:
            error = f"Error connecting to API: {str(e)}"

    campaign = Campaign.objects.get(pk=campaign_id)

    context = {
        'campaign': campaign,
        'search_type': search_type,
        'search_query': search_query,
        'list_results': list_results,
        'error': error
    }
    return render(request, 'dnd_manager/references_search.html', context)


def references_detail_view(request, campaign_id, search_type, slug):
    """
    Show detailed information for a single monster or spell from the 5e-bits API.
    """
    error = None
    data = None

    # Base URL
    if search_type == 'monster':
        base_url = "https://www.dnd5eapi.co/api/2014/monsters"
    else:
        base_url = "https://www.dnd5eapi.co/api/2014/spells"

    url = f"{base_url}/{slug}"

    try:
        response = requests.get(url, headers={'Accept': 'application/json'})
        if response.status_code == 200:
            data = response.json()
        else:
            error = f"Could not find {search_type} details for '{slug}'. (Status {response.status_code})"
    except requests.exceptions.RequestException as e:
        error = f"Error connecting to API: {str(e)}"

    campaign = Campaign.objects.get(pk=campaign_id)

    context = {
        'campaign': campaign,
        'search_type': search_type,
        'data': data,
        'error': error,
    }
    return render(request, 'dnd_manager/references_detail.html', context)

