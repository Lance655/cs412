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
        '''Method to add the years for the drop down menu into the context variables'''
        context = super().get_context_data(**kwargs)
        current_year = datetime.now().year
        context['years'] = list(range(1900, current_year + 1)) 
        return context

    def get_queryset(self):
        '''Method to query the database based on the inputeted parameters of the user'''
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


class ShowGraphsView(ListView):
    '''View to show graph information about the data'''
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'graph_voters'
    
    def get_queryset(self):
        '''Method to add the years for the drop down menu into the context variables'''

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


    def get_context_data(self, **kwargs):
        """
        Build the Plotly charts using the filtered queryset,
        and add them (as safe HTML <div> elements) to the context.
        """
        context = super().get_context_data(**kwargs)
        graph_voters = context['graph_voters']  # The filtered queryset

        # 1) Distribution of Voters by Year of Birth (Histogram)
        chart_birth = self._histogram_by_birth_year(graph_voters)

        # 2) Pie Chart: Distribution by Party Affiliation
        chart_party = self._pie_by_party(graph_voters)

        # 3) Histogram: Participation in each of the 5 elections
        chart_elections = self._histogram_by_elections(graph_voters)

        # Add them to the template context:
        context['chart_birth'] = chart_birth
        context['chart_party'] = chart_party
        context['chart_elections'] = chart_elections

        # add the years for the drop down menu
        current_year = datetime.now().year
        context['years'] = list(range(1900, current_year + 1)) 

        # add the length of voters in the queryset
        context['graph_voter_count'] = len(graph_voters)

        return context

    def _histogram_by_birth_year(self, qs):
        """
        Build a Plotly histogram counting how many voters
        fall into each year_of_birth.
        """
        years = []
        for v in qs:
            if v.date_of_birth and len(v.date_of_birth) >= 4:
                year_str = (v.date_of_birth[:4])  # e.g. '1979'
            try:
                years.append(int(year_str))  # convert to int for sorting
            except ValueError:
                pass

        years.sort()  # sort the years numerically

        fig = go.Histogram(x=years)
        title_text = "Distribution of Voters by Year of Birth"

        graph_div_birth = plotly.offline.plot(
            {
                "data": [fig],
                "layout": {"title": title_text}
            },
            auto_open=False,
            output_type="div"
        )
        return graph_div_birth
    
    def _pie_by_party(self, qs):
        """
        Build a pie chart to show distribution by party affiliation.
        """
        party_count = {}
        for v in qs:
            party = v.party_affiliation.strip()
            party_count[party] = party_count.get(party, 0) + 1

        labels = list(party_count.keys())
        values = list(party_count.values())

        fig = go.Pie(labels=labels, values=values)
        title_text = "Distribution by Party"

        graph_div_party = plotly.offline.plot(
            {
                "data": [fig],
                "layout": {"title": title_text}
            },
            auto_open=False,
            output_type="div"
        )

        return graph_div_party

    def _histogram_by_elections(self, qs):
        """
        Bar chart: how many voted in v20state, v21town, v21primary, v22general, v23town
        """
        labels = ['2020 State', '2021 Town', '2021 Primary', '2022 General', '2023 Town']
        values = [
            qs.filter(v20state=True).count(),
            qs.filter(v21town=True).count(),
            qs.filter(v21primary=True).count(),
            qs.filter(v22general=True).count(),
            qs.filter(v23town=True).count(),
        ]

        fig = go.Bar(x=labels, y=values)
        title_text = "Participation in Each Election"

        graph_div_elections = plotly.offline.plot(
            {
                "data": [fig],
                "layout": {"title": title_text}
            },
            auto_open=False,
            output_type="div"
        )

        return graph_div_elections
