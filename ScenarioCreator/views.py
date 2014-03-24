import json
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
import re

from ScenarioCreator.forms import *  # This is absolutely necessary for dynamic form loading


def basic_context():  # TODO: This might not be performant... but it's nice to have a live status
    return {'Scenario': Scenario.objects.all(),
            'OutputSetting': OutputSettings.objects.all(),
            'ProductionTypes': ProductionType.objects.all(),
            'Farms': Unit.objects.all(),
            'Disease': Disease.objects.all(),
            'Reactions': DiseaseReaction.objects.all(),
            'DirectSpreads': DirectSpreadModel.objects.all(),
            'IndirectSpreads': IndirectSpreadModel.objects.all(),
            'AirborneSpreads': AirborneSpreadModel.objects.all(),
            'Transmissions': ProductionTypePairTransmission.objects.all(),
            'ControlMasterPlan': ControlMasterPlan.objects.all(),
            'Protocols': ControlProtocol.objects.all(),
            'Zones': Zone.objects.all(),
            'ZoneEffects': ZoneEffectOnProductionType.objects.all()}


def disease_spread(request):
    return render(request, 'ScenarioCreator/DiseaseSpread.html', basic_context())


def assign_protocols(request):
    context = basic_context()
    forms = []
    for pt in ProductionType.objects.all():
        initialized_form = ProtocolAssignmentForm(request.POST or None)
        initialized_form.fields['production_type'].initial = pt.id
        forms.append(initialized_form)
    context['forms'] = forms
    context['title'] = 'Assign a Control Protocol to each Production Type'
    return render(request, 'ScenarioCreator/ProtocolAssignment.html', context)


def assign_reactions(request):
    context = basic_context()
    forms = []
    for pt in ProductionType.objects.all():
        initialized_form = DiseaseReactionAssignmentForm(request.POST or None)
        initialized_form.fields['production_type'].initial = pt.id
        forms.append(initialized_form)
    context['forms'] = forms
    context['title'] = 'Set what Reaction each Production Type has to the Disease'
    return render(request, 'ScenarioCreator/ProtocolAssignment.html', context)


def save_new_instance(initialized_form, request):
    model_instance = initialized_form.save()  # write to database
    model_name = model_instance.__class__.__name__
    if request.is_ajax():
        msg = {'pk': model_instance.pk, 'title': str(model_instance), 'model': model_name, 'status': 'success'}
        return HttpResponse(json.dumps(msg), content_type="application/json")
    return redirect('/setup/%s/%i/' % (model_name, model_instance.pk))  # redirect to edit URL


def new_form(request, initialized_form, context):
    if initialized_form.is_valid():
        return save_new_instance(initialized_form, request)
    return render(request, 'ScenarioCreator/crispy-model-form.html', context)  # render in validation error messages


def get_model_name_and_form(request):
    model_name = re.split('\W+', request.path)[2]  # Second word in the URL
    form = globals()[model_name + 'Form']  # IMPORTANT: depends on naming convention
    return model_name, form


def initialize_from_existing_model(primary_key, request):
    """Raises an ObjectDoesNotExist exception when the primary_key is invalid"""
    model_name, form_class = get_model_name_and_form(request)
    model = form_class.Meta.model.objects.get(id=primary_key)  # may raise an exception
    initialized_form = form_class(request.POST or None, instance=model)
    return initialized_form, model_name


'''New / Edit / Copy trio that are called from URLs'''
def new_entry(request):
    model_name, form = get_model_name_and_form(request)
    initialized_form = form(request.POST or None)
    context = basic_context()
    context.update({'form': initialized_form,
                    'title': "Create a new " + model_name})
    return new_form(request, initialized_form, context)


def edit_entry(request, primary_key):
    model_name, form = get_model_name_and_form(request)
    try:
        initialized_form, model_name = initialize_from_existing_model(primary_key, request)
    except ObjectDoesNotExist:
        return redirect('/setup/%s/new/' % model_name)
    if initialized_form.is_valid() and request.method == 'POST':
        initialized_form.save()  # write instance updates to database
    context = basic_context()
    context.update({'form': initialized_form,
                    'title': "Edit a " + model_name}.items())
    return render(request, 'ScenarioCreator/crispy-model-form.html', context)


def copy_entry(request, primary_key):
    model_name, form = get_model_name_and_form(request)
    try:
        initialized_form, model_name = initialize_from_existing_model(primary_key, request)
    except ObjectDoesNotExist:
        return redirect('/setup/%s/new/' % model_name)
    if initialized_form.is_valid() and request.method == 'POST':
        initialized_form.instance.pk = None  # This will cause a new instance to be created
        return save_new_instance(initialized_form, request)
    context = basic_context()
    context.update({'form': initialized_form,
                    'title': "Copy a " + model_name}.items())
    return render(request, 'ScenarioCreator/crispy-model-form.html', context)
