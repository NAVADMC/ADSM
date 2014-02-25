from django.shortcuts import render, get_object_or_404

from ScenarioCreator.forms import *
from ScenarioCreator.models import Ingeneral


def start_window(request):
    context = {'motd':'Remember your quotes!'}
    return render(request, 'ScenarioCreator/index.html', context)


def new_scenario(request):
    initialized_form = DynaherdForm(request.POST or None)
    if initialized_form.is_valid():
        initialized_form.save();  # write to database
    context = {'form': initialized_form}
    context['title'] = "Create a new scenario"
    return render(request, 'ScenarioCreator/new.html', context)


def edit_scenario(request, primary_key):
    scenario = get_object_or_404(Ingeneral, pk=primary_key)
    form = DynaherdForm(request.POST or None, instance=scenario)
    if request.method == 'POST' and form.is_valid():
        form.save(); #write to database
    context = {'form': form}
    context['title'] = "Edit a new scenario"
    return render(request, 'ScenarioCreator/new.html', context)
