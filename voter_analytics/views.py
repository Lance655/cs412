# File: views.py
# Author: Lance Sinson (ssinson@bu.edu), 4/4/25
# Description: The views file for the voter_analytics website. 

# voter_analytics/views.py
#
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView ## NEW
from . models import Voter
from datetime import datetime

## new imports: for the plotly library
import plotly
import plotly.graph_objs as go

# Create your views here.
class ShowAllVoters(ListView):
    '''View to display all voters'''
    model = Voter
    template_name = 'voter_analytics/voters.html'
    context_object_name = 'voters'
    paginate_by = 100


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_year = datetime.now().year
        context['years'] = list(range(1900, current_year + 1)) 
        return context

    def get_queryset(self):
        
        voters = super().get_queryset()

        # look for URL parameters to filter by:

        # general filters
        if 'party' in self.request.GET:
            party = self.request.GET['party']

            if party: # Only filter if user actually selected something
                voters = voters.filter(party_affiliation = party)
        if 'min_dob' in self.request.GET:
            min_dob = self.request.GET['min_dob']

            voters = voters.filter(date_of_birth__gt = min_dob)
        if 'max_dob' in self.request.GET:
            max_dob = self.request.GET['max_dob']

            voters = voters.filter(date_of_birth__lt = max_dob)
        if 'voter_score' in self.request.GET:
            voter_score = self.request.GET['voter_score']

            voters = voters.filter(voter_score=voter_score)


        # whether they voted in the past 5 elections
        if 'v20state' in self.request.GET:   
            did_vote = self.request.GET['v20state']

            voters = voters.filter(v20state=(did_vote=="true"))
        if 'v21town' in self.request.GET:
            did_vote = self.request.GET['v21town']

            voters = voters.filter(v21town=(did_vote=="true"))
        if 'v21primary' in self.request.GET:
            did_vote = self.request.GET['v21primary']

            voters = voters.filter(v21primary=(did_vote=="true"))
        if 'v22general' in self.request.GET:
            did_vote = self.request.GET['v22general']

            voters = voters.filter(v22general=(did_vote=="true"))
        if 'v23town' in self.request.GET:
            did_vote = self.request.GET['v23town']

            voters = voters.filter(v23town=(did_vote=="true"))


        return voters

class ShowVoter(DetailView):
    '''View to show detail page for one result.'''
    model = Voter
    template_name = 'voter_analytics/voter.html'
    context_object_name = 'voter' # primary key pk value starts at 176308