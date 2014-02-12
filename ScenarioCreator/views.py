from django.shortcuts import render
from ScenarioCreator.forms import ScenarioForm


def start_window(request):
    context = {'motd':'Remember your quotes!'}
    return render(request, 'ScenarioCreator/index.html', context)

def new_scenario(request):
    initialized_form = ScenarioForm(request.POST or None)
    if initialized_form.is_valid():
        initialized_form.save(); #write to database
    context = {'form': initialized_form}
    return render(request, 'ScenarioCreator/new.html', context)
