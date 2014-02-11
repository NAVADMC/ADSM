from django.shortcuts import render

# Create your views here.
def start_window(request):
    context = {'motd':'Remember your quotes!'}
    return render(request, 'ScenarioCreator/index.html', context)