from django.shortcuts import render, get_object_or_404
import re

from ScenarioCreator.forms import *


def new_form(request, form_class, title):
    initialized_form = form_class(request.POST or None)
    if initialized_form.is_valid():
        initialized_form.save()  # write to database
    context = {'form': initialized_form,
               'title': title}
    return render(request, 'ScenarioCreator/new.html', context)


def new_scenario(request):
    return new_form(request, InGeneralForm, "Starting a new Scenario")


def get_model_name_and_form(request):
    model_name = re.split('\W+', request.path)[2]  # Second word in the URL
    form = globals()[model_name + 'Form']  # depends on naming convention
    return model_name, form


def new_entry(request):
    model_name, form = get_model_name_and_form(request)
    return new_form(request, form, "Create a new " + model_name)


def edit_entry(request, primary_key):
    model_name, form_class = get_model_name_and_form(request)
    model = get_object_or_404(form_class.Meta.model, pk=primary_key)
    form = form_class(request.POST or None, instance=model)
    if request.method == 'POST' and form.is_valid():
        form.save()  # write to database
    context = {'form': form,
               'title': "Edit a " + model_name}
    return render(request, 'ScenarioCreator/new.html', context)
