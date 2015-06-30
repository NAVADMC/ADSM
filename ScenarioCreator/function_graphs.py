# import Results.graphing  #matplotlib instantiation
import matplotlib
from Results.graphing import HttpFigure, rstyle
import matplotlib.pyplot as plt


def probability_graph(request, primary_key):
    pass

def relational_graph_update(request, primary_key):
    import ScenarioCreator.views

    print("Received a graph POST")
    context = ScenarioCreator.views.initialize_relational_form({}, primary_key, request)
    formset = ScenarioCreator.views.PointFormSet(request.POST or None, instance=context['model'])
    if formset.is_valid():
        return line_graph('Days', [a['x'] for a in formset], [a['y'] for a in formset])
    else:
        return existing_relational_graph(primary_key)


def relational_graph(request, primary_key):
    if request.method == 'POST':
        return relational_graph_update(request, primary_key)
    return existing_relational_graph(primary_key)


def existing_relational_graph(primary_key):
    import ScenarioCreator.models

    model_instance = ScenarioCreator.models.RelationalFunction.objects.get(id=primary_key)
    x_series = list(ScenarioCreator.models.RelationalPoint.objects.filter(relational_function=model_instance).order_by('x').values_list('x', flat=True))
    y_series = list(ScenarioCreator.models.RelationalPoint.objects.filter(relational_function=model_instance).order_by('x').values_list('y', flat=True))
    x_label = model_instance.x_axis_units
    return line_graph(x_label, x_series, y_series)


def line_graph(x_label, x_series, y_series):
    fig = plt.figure(figsize=(3.5, 2), dpi=100, tight_layout=True, facecolor='w')
    matplotlib.rcParams.update({'font.size': 10})
    time_graph = plt.subplot(111)  # title=model_instance.name)
    time_graph.set_xlabel(x_label)
    time_graph.grid(False)

    # plt.plot(old_x, old_y, color='lightgrey')  # for comparison
    plt.plot(x_series, y_series, color='black')
    rstyle(time_graph)

    return HttpFigure(fig)