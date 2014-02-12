from django.shortcuts import render
from ScenarioCreator.forms import ScenarioForm


def start_window(request):
    context = {'motd':'Remember your quotes!'}
    return render(request, 'ScenarioCreator/index.html', context)

def new_scenario(request):
    context = {'form': ScenarioForm()}
    return render(request, 'ScenarioCreator/new.html', context)
