import math
import matplotlib
import numpy

matplotlib.use('Agg')  # Force matplotlib to not use any Xwindows backend.
from matplotlib import rc
rc("figure", facecolor="white")

from time import time
from matplotlib import gridspec
from itertools import chain
from django.http import HttpResponse
from django.db.models import Max, Min
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.colors import LogNorm, ListedColormap
from matplotlib.colorbar import ColorbarBase
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib import cm

from ScenarioCreator.models import Zone, ProductionType, Unit
from Results.summary import list_of_iterations
from Results.models import DailyControls, DailyByProductionType, DailyByZone, DailyByZoneAndProductionType


def HttpFigure(fig):
    response = HttpResponse(content_type='image/png')
    FigureCanvas(fig).print_png(response, bbox_inches='tight')
    plt.close(fig)
    return response


# def matplotd3(request):
#     fig, ax = plt.subplots()
#     points = ax.plot([3, 1, 4, 1, 5], 'ks-', mec='w', mew=5, ms=20)
#     return HttpResponse(mpld3.fig_to_html(fig))


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


def construct_title(field_name, iteration, model, zone=''):
    pt_mention = ' for all Production Types' if model in [DailyByProductionType, DailyByZoneAndProductionType] and not iteration else ''
    explanation = model._meta.get_field_by_name(field_name)[0].verbose_name
    iter_str = " iteration " + str(iteration) if iteration else ' for all iterations'
    if zone:
        title = "%s %s\n%s%s" % (zone, explanation, pt_mention, iter_str)
    else:
        title = "%s\n%s%s" % (explanation, pt_mention, iter_str)
    return explanation, title




def population_png(request, width_inches=8, height_inches=8):
    start_time = time()
    qualitative_colors = ['#1f78b4', '#33a02c','#e31a1c', '#ff7f00','#6a3d9a', '#b15928']
    #dark_and_light = ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c', '#fdbf6f', '#ff7f00', '#cab2d6', '#6a3d9a', '#ffff99', '#b15928', ]
    fig = Figure(figsize=(width_inches, height_inches), frameon=True, tight_layout=True)  # Issue #168 aspect ratio doesn't adjust currently
    ax = fig.add_subplot(1, 1, 1, axisbg='#FFFFFF')
    size = 3000 / math.sqrt(Unit.objects.count())
    for index, production_type in enumerate(ProductionType.objects.all()):
        latlong = [(u.latitude, u.longitude) for u in Unit.objects.filter(production_type=production_type)]
        longitude, latitude = zip(*latlong)
        ax.scatter(latitude,
                   longitude,
                   marker='s',
                   linewidths=0.005,  # for some reason won't draw if linewidths = 0
                   s=size,
                   color=qualitative_colors[index % len(qualitative_colors)],
                   label=production_type.name)
    ax.legend(scatterpoints=3,
              loc='lower left',
              ncol=4,
              fontsize=10)
        
    # Math for aspect ratio and range of axes
    ymin, ymax = Unit.objects.all().aggregate(Min('latitude'))['latitude__min'], Unit.objects.all().aggregate(Max('latitude'))['latitude__max']
    xmin, xmax = Unit.objects.all().aggregate(Min('longitude'))['longitude__min'], Unit.objects.all().aggregate(Max('longitude'))['longitude__max']
    x_center, y_center = (xmin + xmax)/2,  (ymin + ymax)/2
    largest_range = max(abs(ymax-ymin), abs(xmax-xmin)) / 2 
    ax.set_ylim(y_center - largest_range, y_center + largest_range)
    ax.set_xlim(x_center - largest_range, x_center + largest_range)
    print("Population Map took %i seconds" % int(time() - start_time))
    return HttpFigure(fig)


def breakdown_dictionary(iterate_pt, iterate_zone):
    production_types, zones = {}, {}
    if iterate_pt:
        production_types = dict(ProductionType.objects.all().values_list('name', 'id'))  # Tuples need to be turned into dict
        production_types['All'] = None  # this has been vetted for Issue #223 as a user label
    if iterate_zone:
        zones = dict(Zone.objects.all().values_list('name', 'id'))  # Tuples need to be turned into dict
        if iterate_pt:  # Background is only included in DailyByZoneAndProductionType.  See Issue #198
            zones['Background'] = None
    return production_types, zones


def construct_iterating_combination_filter_dictionary(iteration, model, zone=''):
    """Truth table of iterate_pt and iterate_zone gives you four values.  One for each Daily Model.
    Whether or not iteration is specified raises it to 8 combinations of possible filters used."""
    iterate_pt, iterate_zone = {DailyByProductionType: (True, False),
                                DailyByZoneAndProductionType: (True, True),
                                DailyByZone: (False, True),
                                DailyControls: (False, False)}[model]
    production_types, zones = breakdown_dictionary(iterate_pt, iterate_zone)
    active_zone = Zone.objects.all().order_by('-radius').first()  # the only "summary" zone stats to be displayed
    if zone:
        active_zone = Zone.objects.filter(name=zone).first()
    filter_sequence = []
    columns = ['Day']
    if iteration:  # 1__ Break down lines by production type for only one iteration
        if production_types:  # 11_
            columns += list(production_types.keys())
            if iterate_zone:  # 111
                # This is the one case where we use the 'zone' parameter because there's too much information otherwise
                for name in production_types.keys():  # add one for each Production Type and "All"
                    filter_sequence.append({'iteration': iteration,
                                            'production_type_id': production_types[name],
                                            'zone': active_zone})
            else:  # 110
                for name in production_types.keys():  # add one for each Production Type and "All"
                    filter_sequence.append({'iteration': iteration, 'production_type_id': production_types[name]})
                
        else:  # 10_
            if iterate_zone:  # 101 specific iteration of DailyByZone
                columns += list(zones.keys())
                for zone_pk in zones.values():  # add one for each Zone and "Background"
                    filter_sequence.append({'iteration': iteration, 'zone_id': zone_pk})
            else:  # 100 specific iteration of DailyControl field
                columns.append("Field")
                filter_sequence.append({'iteration': iteration},)
            
    else:  # 0__ This is a summary time plot of all iterations.
        columns += ["Iteration " + str(it) for it in list_of_iterations()]  # columns names are always the same,
        # Different graph settings still only get to inject one time line graph per iteration
        if production_types:  # 01_ "All Production Type"
            if iterate_zone:  # 011 "All Production Type" and active_zone
                filter_sequence.append({'production_type': None, 'zone': active_zone})
            else:  # 010
                filter_sequence.append({'production_type': None})
            
        else:  # 00_
            if iterate_zone:  # 001 DailyByZone
                filter_sequence.append({'zone': active_zone})
            else:  # 000 DailyControls
                filter_sequence.append({})  

    return filter_sequence, columns


def create_time_series_lines(field_name, model, iteration=None, zone=''):
    filter_sequence, columns = construct_iterating_combination_filter_dictionary(iteration, model, zone=zone)
    lines = [] 
    if iteration:  # Manually step through each query for a single iteration
        for filter_dict in filter_sequence:
            lines.append(list(model.objects.filter(**filter_dict).order_by('day').values_list(field_name, flat=True)))
    else:  # summary of all iterations is a single query for performance reasons
        max_size = model.objects.all().aggregate(Max('day'))['day__max']
        for row in range(len(list_of_iterations())):  # iteration = index
            lines.append([None] * max_size)
        objs = model.objects.filter(**filter_sequence[0]).values_list('iteration', 'day', field_name)
        for entry in objs:
            lines[int(entry[0])-1][entry[1]-1] = entry[2]  # sorting done in python, iteration and day are both 1 indexed

    return lines, columns


def field_is_cumulative(explanation):
    return 'new' not in explanation.lower()


def extend_last_day_lines(lines, model, field_name):
    """Turns the ragged edge caused by different iterations ending on different days into
    a series of flat lines at their ending value.  Implemented for Issue #159"""
    time_series = []
    max_size = max([len(x) for x in lines])
    cumulative_field = field_is_cumulative(model._meta.get_field_by_name(field_name)[0].verbose_name.lower())
    ends = [line.index(None) if None in line else max_size for line in lines]
    
    for line, end in [(lines[i], ends[i]) for i in range(len(lines))]:
        if cumulative_field:
            last_value = line[end-1]
        else:  # This field is non-cumulative, default to zero
            last_value = 0
        time_series.append(line)
        for x in range(end, max_size):
            time_series[-1][x] = last_value  # editing the line we just appended
    return time_series


def collect_boxplot_data(padded_lines, explanation):
    """Returns a long tuple with all the data necessary to make a boxplot distribution.  For 'cumulative' fields,
    this is the last day.  For non-cumulative, it is the range of non-blank values.  Issue #159:
    https://github.com/NAVADMC/ADSM/issues/159#issuecomment-53058264"""
    if not field_is_cumulative(explanation):  # This field is non-cumulative, default to zero
        boxplot_data = tuple(chain([x for line in padded_lines for x in line if x != 0]))  # pile together all the data, but don't include trailing zeroes
    else:  # this field is cumulative
        boxplot_data = (line[-1] for line in padded_lines)  # only last day is relevant
    return boxplot_data


def single_iteration_line_graph(iteration, field_name, model_name, model, time_series, columns, time_graph, boxplot_graph, fig):
    days = list(range(1, len(time_series[0]) + 1))  # Start with day index
    time_data = pd.DataFrame.from_records( list(zip(days, *time_series)), columns=columns)  # keys should be same ordering as the for loop above
    time_data = time_data.set_index('Day')

    time_data.plot(ax=time_graph)

    if iteration is None:
        time_graph.legend().remove()
    
    # Manually scale zone graphs based on the Max for any zone (universal value)
    if "Zone" in model_name:
        # It's important to filter out Background stats from this Max
        if iteration is not None:
            ymax = model.objects.filter(zone__isnull=False, iteration=iteration).aggregate(Max(field_name))[field_name + '__max'] * 1.05
        else:
            ymax = model.objects.filter(zone__isnull=False).aggregate(Max(field_name))[field_name + '__max'] * 1.05
        time_graph.set_ylim(0.0, ymax)
        boxplot_graph.set_ylim(0.0, ymax)

    return HttpFigure(fig)


def TwoD_histogram(fig, gs, time_graph, time_series):
    days = list(range(1, len(time_series[0]) + 1))  # Start with day index
    x = days * len(time_series)  # repeat day series for each set of data (1 per iteration)
    y = list(chain(*time_series))
    hot = plt.get_cmap('hot')
    norm = LogNorm()
    time_graph.hist2d(x, y,
                      bins=[len(days), max(5, min(max(*y), 300))],
                      # 300 should really be the number of pixels in the draw area (I don't know how to fetch that)
                      norm=norm,
                      cmap=hot)
    color_bar = fig.add_subplot(gs[0], )
    ColorbarBase(cmap=hot, ax=color_bar, norm=norm)
    return HttpFigure(fig)


def graph_field_png(request, model_name, field_name, iteration='', zone=''):
    model = globals()[model_name]
    iteration = int(iteration) if iteration else None
    lines, columns = create_time_series_lines(field_name, model, iteration=iteration, zone=zone)

    time_series = extend_last_day_lines(lines, model, field_name)
    
    explanation, title = construct_title(field_name, iteration, model, zone)

    fig = plt.figure(figsize=(7, 4), dpi=100, tight_layout=True, facecolor='w')
    matplotlib.rcParams.update({'font.size': 10})
    gs = gridspec.GridSpec(1, 3, width_ratios=[.2, 6, 1])
    time_graph = fig.add_subplot(gs[1], title=title)
    time_graph.set_xlabel('Days')
    boxplot_graph = fig.add_subplot(gs[2], sharey=time_graph, )  # http://stackoverflow.com/questions/4209467/matplotlib-share-x-axis-but-dont-show-x-axis-tick-labels-for-both-just-one
    # boxplot_graph.locator_params(nbins=4)  # limiting the number of y-axis ticks was causing an intermittent crash.  try/except this if you want it
    plt.setp(boxplot_graph.get_yticklabels(), visible=False)
    for axis in [time_graph, boxplot_graph]:
        rstyle(axis)
    time_graph.grid(False)

    boxplot_raw = collect_boxplot_data(time_series, explanation)  # This has already been padded
    boxplot_data = pd.DataFrame(pd.Series(boxplot_raw), columns=['Last Day'] if field_is_cumulative(explanation) else ['Distribution'])
    boxplot_data.boxplot(ax=boxplot_graph, return_type='axes')

    if iteration:  # for a single iteration, we don't need all the hist2d prep
        return single_iteration_line_graph(iteration, field_name, model_name, model, time_series, columns, time_graph, boxplot_graph, fig)
    if len(list_of_iterations()) < 50:
        # do a stacked line graph instead of a histogram    
        return single_iteration_line_graph(iteration, field_name, model_name, model, time_series, columns, time_graph, boxplot_graph, fig)

    return TwoD_histogram(fig, gs, time_graph, time_series)

