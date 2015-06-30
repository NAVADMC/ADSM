# import Results.graphing  #matplotlib instantiation
import matplotlib
from Results.graphing import HttpFigure, rstyle
import matplotlib.pyplot as plt


def probability_graph(request, primary_key):
    pass

def relational_graph(request, primary_key):
    import ScenarioCreator.models

    model_instance = ScenarioCreator.models.RelationalFunction.objects.get(id=primary_key)

    fig = plt.figure(figsize=(7, 4), dpi=100, tight_layout=True, facecolor='w')
    matplotlib.rcParams.update({'font.size': 10})
    time_graph = plt.subplot(211)#title=model_instance.name)
    time_graph.set_xlabel(model_instance.x_axis_units)
    rstyle(time_graph)
    time_graph.grid(False)

    x_series = list(ScenarioCreator.models.RelationalPoint.objects.filter(relational_function=model_instance).order_by('x').values_list('x', flat=True))
    y_series = list(ScenarioCreator.models.RelationalPoint.objects.filter(relational_function=model_instance).order_by('x').values_list('y', flat=True))

    plt.plot(x_series, y_series)


    return HttpFigure(fig)