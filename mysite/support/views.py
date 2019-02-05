from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views import generic, View

from .forms import RegisterForm
from .models import Ticket

class IndexView(generic.ListView):
    """
    CBV for generating simple index view of our support app.
    User can either chose to
    1. list all the tickets in the database
    2. Register a new ticket in the database
    """

    template_name = 'support/index.html'

    def get_queryset(self):
        return None

class RegisterView(View):
    """
    Our form class that uses class based views to render a register form.
    """
    form_class = RegisterForm
    template_name = 'support/form.html'

    def get(self, request, *args, **kwargs):
        """
        Our inbuilt GET method to render a new blank form
        """
        form = self.form_class()
        return render(request, self.template_name, {'form': form})


    def post(self, request, *args, **kwargs):
        """
        Our inbuilt POST method to read a saved form or populate it with
        previously filled fields.
        """
        form = self.form_class(request.POST)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            vendor = form.cleaned_data['vendor']
            category = form.cleaned_data['category']
            severity = form.cleaned_data['severity']
            description = form.cleaned_data['description']

            # create a ticket in our database
            Ticket.objects.create(vendor=vendor, category=category,
                severity=severity, description=description)

            # redirect to a the list all tickets url
            return HttpResponseRedirect(reverse('support:list'))

        return render(request, self.template_name, {'form': form})

class ListView(generic.ListView):
    """
    Our List view class that used django's CBV and renders out a list of all the
    tickets in the database.
    """
    model = Ticket
    template_name = 'support/list.html'
    context_object_name = 'tickets'

    def get_queryset(self):
        """Return all the tickets registered in the database."""
        return Ticket.objects.all()



class DetailView(generic.DetailView):
    """
    Our Detail view class that used django's CBV and shows the detail
    of any particular ticket in the database.
    """
    model = Ticket
    template_name = 'support/detail.html'
