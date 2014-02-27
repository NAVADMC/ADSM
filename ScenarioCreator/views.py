from django.shortcuts import render, get_object_or_404

from ScenarioCreator.forms import *


def start_window(request):
    context = {'motd':'Remember your quotes!'}
    return render(request, 'ScenarioCreator/index.html', context)

def new_form(request, formClass, title):
    initialized_form = formClass(request.POST or None)
    if initialized_form.is_valid():
        initialized_form.save()  # write to database
    context = {'form': initialized_form,
               'title': title}
    return render(request, 'ScenarioCreator/new.html', context)

def new_scenario(request):
    return new_form(request, InGeneralForm, "Create a new scenario")

def new_herd(request):
    return new_form(request, DynamicHerdForm, "Create a new Herd")

def edit_scenario(request, primary_key):
    scenario = get_object_or_404(InGeneral, pk=primary_key)
    form = InGeneralForm(request.POST or None, instance=scenario)
    if request.method == 'POST' and form.is_valid():
        form.save(); #write to database
    context = {'form': form,
               'title': "Edit a new scenario"}
    return render(request, 'ScenarioCreator/new.html', context)
