# import Results.graphing  #matplotlib instantiation
from django.http import HttpResponse
import matplotlib

matplotlib.use('Agg')  # Force matplotlib to not use any Xwindows backend.
from matplotlib import rc
rc("figure", facecolor="white")

from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt


def probability_graph(request, primary_key):
    pass

def relational_graph_update(request, primary_key):
    import ScenarioCreator.views

    print("Received a graph POST")
    context = ScenarioCreator.views.initialize_relational_form({}, primary_key, request)
    formset = ScenarioCreator.views.PointFormSet(request.POST or None, instance=context['model'])
    if formset.is_valid():
        x, y = [], []
        for a in formset:
            if a['x'].data and a['y'].data:
                x.append(float(a['x'].data))
                y.append(float(a['y'].data))

        #         http://stackoverflow.com/questions/8483348/django-return-image-data-from-a-view
        # https://en.wikipedia.org/wiki/Data_URI_scheme
        # http://stackoverflow.com/questions/10802312/display-png-image-as-response-to-jquery-ajax-request
        return line_graph('Days', x, y)
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


def HttpFigure(fig):
    response = HttpResponse(content_type='image/png')
    FigureCanvas(fig).print_png(response, bbox_inches='tight')
    plt.close(fig)
    return response


def rstyle(axis):
    """Styles x,y axes to appear like ggplot2
    Must be called after all plot and axis manipulation operations have been
    carried out (needs to know final tick spacing) """
    #Set the style of the major and minor grid lines, filled blocks
    axis.grid(True, 'major', color='w', linestyle='-', linewidth=1.4)
    axis.grid(True, 'minor', color='0.99', linestyle='-', linewidth=0.7)
    # axis.patch.set_facecolor('0.90')  # uncomment to add a subtle grid
    axis.set_axisbelow(True)

    """This code is currently disabled because I don't want to add a pylab dependency"""
    #Set minor tick spacing to 1/2 of the major ticks
    # axis.yaxis.set_major_locator((plticker.MultipleLocator(base=3000.0)))

    #Remove axis border
    for child in axis.get_children():
        if isinstance(child, matplotlib.spines.Spine):
            child.set_alpha(0)

    #Restyle the tick lines
    for line in axis.get_xticklines() + axis.get_yticklines():
        line.set_markersize(5)
        line.set_color("gray")
        line.set_markeredgewidth(1.4)

    #Remove the minor tick lines
    for line in (axis.xaxis.get_ticklines(minor=True) +
                 axis.yaxis.get_ticklines(minor=True)):
        line.set_markersize(0)

    #Only show bottom left ticks, pointing out of axis
    plt.rcParams['xtick.direction'] = 'out'
    plt.rcParams['ytick.direction'] = 'out'
    axis.xaxis.set_ticks_position('bottom')
    axis.yaxis.set_ticks_position('left')