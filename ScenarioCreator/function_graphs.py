# import Results.graphing  #matplotlib instantiation
from django.http import HttpResponse
import matplotlib

matplotlib.use('Agg')  # Force matplotlib to not use any Xwindows backend.
from matplotlib import rc
rc("figure", facecolor="white")

from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import scipy.stats
from math import sqrt, log, exp
from django.db.models import IntegerField, FloatField

def probability_graph(request, primary_key):
    if request.method == 'POST':
        return empty_graph(request)  # TODO: update on the fly
    return existing_probability_graph(primary_key)
    # return empty_graph()


def existing_probability_graph(primary_key):
    import ScenarioCreator.models
    m = ScenarioCreator.models.ProbabilityFunction.objects.get(id=primary_key)
    #TODO: filler to avoid NaNs
    for field in m._meta.fields:
        if field is None and isinstance(field, (IntegerField, FloatField)):
            field = 1  # don't save this

    kind = m.equation_type
    d = (m.min + 4 * m.mode + m.max) / 6
    # log defaults to ln
    eq = {  # Compiled from:  https://github.com/NAVADMC/ADSM/wiki/Probability-density-functions  Thanks Neil Harvey!
            "Bernoulli": [scipy.stats.bernoulli, {'p': m.p}],
            "Beta": [scipy.stats.beta, {'a': m.alpha, 'b': m.alpha2, 'loc': m.min, 'scale': m.max - m.min}],
            "BetaPERT": [scipy.stats.beta,
                         {'a': 6 * ((d - m.min) / (m.max - m.min)), 'b': 6 * ((m.max - d) / (m.max - m.min)), 'loc': m.min, 'scale': m.max - m.min}],
            "Binomial": [scipy.stats.binom, {'s': m.s, 'loc': m.p}],
            "Discrete Uniform": [scipy.stats.randint, {'a': m.min, 'b': m.max}],
            "Exponential": [scipy.stats.expon, {'scale': m.mean}],
            "Fixed Value": [],  # TODO: Not offered in SciPy? Use a narrow uniform instead
            "Gamma": [scipy.stats.gamma, {'a': m.alpha, 'scale': m.beta, 'loc': 0}],
            "Gaussian": [scipy.stats.norm, {'loc': m.mean, 'scale': m.std_dev}],
            "Histogram": [],  # TODO: Not offered in SciPy? by hand
            "Hypergeometric": [scipy.stats.hypergeom, {'M': m.m, 'n': m.d, 'N': m.n}],
            # I don't know, but these seem to be the order of args in scipy/stats/_discrete_distns.py:306
            "Inverse Gaussian": [],  # TODO: Shape/lambda parameter not supported in SciPy?
            "Logistic": [scipy.stats.logistic, {'loc': m.location, 'scale': m.scale}],
            "LogLogistic": [scipy.stats.fisk, {'c':m.shape, 'loc': m.location, 'scale': m.scale}],  # scipy/stats/_continuous_distns.py:683 http://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.fisk.html
            "Lognormal": [scipy.stats.lognorm, {'sigma': (sqrt(log((std_dev**2 + mean**2) / mean**2))), 
                                                'scale': exp(log(mean**2 / sqrt(std_dev**2 + mean**2)))}],  # I think exp(log()) is redundant
                                                # Double check this, there's a lot of math
            "Negative Binomial": [scipy.stats.nbinom, {'n': m.s, 'p': m.p}],
            "Pareto": [scipy.stats.pareto, {'theta': m.theta, 'scale': m.a}],
            "Pearson 5": [],  # TODO: Not offered in SciPy
            "Piecewise": [],
            "Poisson": [scipy.stats.poisson, {'k': m.mean}],
            "Triangular": [scipy.stats.triang, {'loc':m.min, 'c':(m.mode-m.min)/(m.max-m.min), 'scale': m.max-m.min}],
            "Uniform": [scipy.stats.uniform, {'loc': m.min, 'scale':m.max-m.min}],
            "Weibull": [scipy.stats.weibull_min, {'x':m.alpha, 'scale': m.beta}],
            }
    function = eq[kind][0]
    kwargs_dict = eq[kind][1]

    return pdf_graph(m.x_axis_units, function, kwargs_dict)


def pdf_graph(x_label, function, kwargs_dict):
    x_axis = (0, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5)
    dist = function(**kwargs_dict)
    y_axis = [dist.pdf(x) for x in x_axis]

    return line_graph(x_label, x_axis, y_axis)


def empty_graph(request):
    return line_graph('Days', [],[])  # empty graph


def relational_graph_update(request, primary_key):
    import ScenarioCreator.views

    x, y = [], []

    print("Received a graph POST")
    context = ScenarioCreator.views.initialize_relational_form({}, primary_key, request)
    formset = ScenarioCreator.views.PointFormSet(request.POST or None, instance=context['model'])
    if formset.is_valid():
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