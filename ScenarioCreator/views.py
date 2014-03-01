from django.shortcuts import render, get_object_or_404
import re

from ScenarioCreator.forms import *


def new_form(request, formClass, title):
    initialized_form = formClass(request.POST or None)
    if initialized_form.is_valid():
        initialized_form.save()  # write to database
    context = {'form': initialized_form,
               'title': title}
    return render(request, 'ScenarioCreator/new.html', context)


def new_entry(request):
    model_name = re.split('\W+', request.path)[2]  # Second word
    form = globals()[model_name+'Form']
    return new_form(request, form, "Create a new " + model_name)


def edit_entry(request, primary_key, model):
    scenario = get_object_or_404(model, pk=primary_key)
    form = InGeneralForm(request.POST or None, instance=scenario)
    if request.method == 'POST' and form.is_valid():
        form.save();  #write to database
    context = {'form': form,
               'title': "Edit a " + model.__class__.__name__}
    return render(request, 'ScenarioCreator/new.html', context)
