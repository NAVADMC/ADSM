# import Results.graphing  #matplotlib instantiation
from django.http import HttpResponse
import matplotlib

matplotlib.use('Agg')  # Force matplotlib to not use any Xwindows backend.
from matplotlib import rc
rc("figure", facecolor="white")

from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import scipy.stats
import numpy as np
from math import sqrt, log, exp, pi
from django.db.models import IntegerField, FloatField

class Empty:
    pass

class inverse_gaussian:
    """Example of how to make a Scipy imposter class for pdf.
    Scipy does not offer inverse gaussian functions with 'shape' parameters, so this is brought in from the C Engine."""
    dist = Empty()
    dist.pdf = 1 # to pass the check in pdf_graph()

    def __init__(self, mean, shape):
        self.mean = mean
        self.shape = shape

    def pdf(self, x_array):
        y = []
        for x in x_array:
            if x > 0:
                y.append( sqrt(self.shape / (2.0 * pi * x**3)) * exp(-1 * ((self.shape * (x - self.mean)**2) /
                                                                                      (2.0 * ((self.mean)**2) * x))) )
            else:
                y.append(0.0)
        return y


def histogram_pdf(rel_primary_key):
    """Example of bare pdf function that returns a graph without the need for an X range array."""
    import ScenarioCreator.models

    model_instance = ScenarioCreator.models.RelationalFunction.objects.get(id=rel_primary_key)
    x_series = list(ScenarioCreator.models.RelationalPoint.objects.filter(relational_function=model_instance).order_by('x').values_list('x', flat=True))
    y_series = list(ScenarioCreator.models.RelationalPoint.objects.filter(relational_function=model_instance).order_by('x').values_list('y', flat=True))
    x_label = "Histogram"
    # x_series = [0, 1, 3, 6, 7, 8, 11]
    # y_series = [0, 2, 0, 5, 2, 1, 0]
    x_hist = [0]
    y_hist = [0]
    points = list(zip(x_series, y_series))
    for index in range(len(points) - 1):
        x_hist += [points[index][0], points[index + 1][0]]
        y_hist += [points[index][1], points[index + 0][1]]
    x_hist += [x_series[-1], x_series[-1]+1, x_series[-1]+1]
    y_hist += [y_series[-1], y_series[-1], 0]

    return line_graph(x_label, x_hist, y_hist)



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
        if getattr(m, field.name) is None and isinstance(field, (IntegerField, FloatField)):
            setattr(m, field.name, 1)  # don't save this

    # log defaults to ln
    d = (m.min + 4 * m.mode + m.max) / 6

    #The following could cause a divide by zero error
    max_min_denominator = m.max - m.min if m.max != m.min else .000001
    a = 6 * ((d - m.min) / max_min_denominator)
    b = 6 * ((m.max - d) / max_min_denominator)
    c = (m.mode - m.min) / max_min_denominator
    mean_safe = m.mean if m.mean != 0 else .000001
    x_lognorm = sqrt(log((m.std_dev ** 2 + mean_safe ** 2) / mean_safe ** 2))
    s_lognorm = mean_safe ** 2 / sqrt(m.std_dev ** 2 + mean_safe ** 2)

    eq = {  # Compiled from:  https://github.com/NAVADMC/ADSM/wiki/Probability-density-functions  Thanks Neil Harvey!
            "Bernoulli": [scipy.stats.bernoulli, [m.p]],
            "Beta": [scipy.stats.beta, {'a': m.alpha, 'b': m.alpha2, 'loc': m.min, 'scale': m.max - m.min}],
            "BetaPERT": [scipy.stats.beta, {'a': a, 'b': b, 'loc': m.min, 'scale': m.max - m.min}],
            "Binomial": [scipy.stats.binom, [m.s, m.p]],
            "Discrete Uniform": [scipy.stats.randint, [m.min, m.max]],
            "Exponential": [scipy.stats.expon, {'scale': m.mean}],
            "Fixed Value": [scipy.stats.uniform, {'loc': m.mode, 'scale': 0.0001}],  # Use a narrow uniform instead
            "Gamma": [scipy.stats.gamma, {'a': m.alpha, 'scale': m.beta, 'loc': 0}],
            "Gaussian": [scipy.stats.norm, {'loc': m.mean, 'scale': m.std_dev}],
            "Histogram": [histogram_pdf, [m.graph_id]],
            "Hypergeometric": [scipy.stats.hypergeom, [m.m, m.d, m.n]],
            "Inverse Gaussian": [inverse_gaussian, [m.mean, m.shape]],
            "Logistic": [scipy.stats.logistic, {'loc': m.location, 'scale': m.scale}],
            "LogLogistic": [scipy.stats.fisk, {'c': m.shape, 'loc': m.location, 'scale': m.scale}],
            # scipy/stats/_continuous_distns.py:683 http://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.fisk.html
            "Lognormal": [scipy.stats.lognorm, [x_lognorm, 0, s_lognorm]],  # I think exp(log()) is redundant
            "Negative Binomial": [scipy.stats.nbinom, {'n': m.s, 'p': m.p}],
            "Pareto": [scipy.stats.pareto, [m.theta, 0, m.a]],
            "Pearson 5": [scipy.stats.invgamma, {'a':m.alpha, 'scale':m.beta}],
            "Piecewise": [existing_relational_graph, [m.graph_id]],
            "Poisson": [scipy.stats.poisson, [m.mean]],
            "Triangular": [scipy.stats.triang, {'loc': m.min, 'c': c, 'scale': m.max - m.min}],
            "Uniform": [scipy.stats.uniform, {'loc': m.min, 'scale': m.max - m.min}],
            "Weibull": [scipy.stats.weibull_min, [m.alpha, 0, m.beta]],
            }
    function = eq[m.equation_type][0]
    kwargs_dict = eq[m.equation_type][1]

    return pdf_graph(m.x_axis_units, function, kwargs_dict)


def pdf_graph(x_label, function, kwargs_dict):
    if isinstance(kwargs_dict, dict):
        dist = function(**kwargs_dict)
    else:
        dist = function(*kwargs_dict) # use positional arguments
    if isinstance(dist, HttpResponse):  #some shortcut scipy and just return a graph response
        return dist
    x_max = 5
    if hasattr(dist, 'ppf'):
        x_max = dist.ppf(0.95) * 1.1
    x = np.arange(0.0, x_max, x_max / 100)
    if hasattr(dist.dist, 'pdf'):  # Scipy continuous functions
        y_axis = dist.pdf(x)
    else:  # scipy discrete functions
        y_axis = dist.pmf(x)

    return line_graph(x_label, x, y_axis)


def empty_graph(request=None):
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
    if request is not None and request.method == 'POST':
        return relational_graph_update(request, primary_key)
    return existing_relational_graph(primary_key)


def existing_relational_graph(primary_key):
    import ScenarioCreator.models

    if primary_key is None:
        return empty_graph()

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