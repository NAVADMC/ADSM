from django.http import HttpResponse
from django.db.models import Max
from itertools import chain
from Results.summary import list_of_iterations
from Results.models import *  # necessary for globals()
import matplotlib
from ScenarioCreator.views import spaces_for_camel_case

matplotlib.use('Agg')  # Force matplotlib to not use any Xwindows backend.
from matplotlib import gridspec
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import pandas as pd
import matplotlib.pyplot as plt, mpld3


def matplotd3(request):
    fig, ax = plt.subplots()
    points = ax.plot([3, 1, 4, 1, 5], 'ks-', mec='w', mew=5, ms=20)
    return HttpResponse(mpld3.fig_to_html(fig))


def HttpFigure(fig):
    response = HttpResponse(content_type='image/png')
    FigureCanvas(fig).print_png(response)
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


def population_png(request):
    latlong = [(u.latitude, u.longitude) for u in Unit.objects.all()]
    df = pd.DataFrame.from_records(latlong, columns=['Latitude', 'Longitude'])
    axis = df.plot('Longitude', 'Latitude', kind='scatter', color='black', figsize=(4.5, 4))
    return HttpFigure(axis.figure)


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


def construct_iterating_combination_filter_dictionary(iteration, iterate_pt, iterate_zone, zone=''):
    """Truth table of iterate_pt and iterate_zone gives you four values.  One for each Daily Model.
    Whether or not iteration is specified raises it to 8 combinations of possible filters used."""
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
        for nth_iteration in list_of_iterations():
            if production_types:  # 01_ "All Production Type"
                if iterate_zone:  # 011 "All Production Type" and active_zone
                    filter_sequence.append({'iteration': nth_iteration, 'production_type': None, 'zone': active_zone})
                else:  # 010
                    filter_sequence.append({'iteration': nth_iteration, 'production_type': None})
                
            else:  # 00_
                if iterate_zone:  # 001 DailyByZone
                    filter_sequence.append({'iteration': nth_iteration, 'zone': active_zone})
                else:  # 000 DailyControls
                    filter_sequence.append({'iteration': nth_iteration})  

    return filter_sequence, columns


def create_time_series_lines(field_name, model, iteration='', zone=''):  # Django assigns iteration='' when there's nothing
    iterate_pt, iterate_zone = {DailyByProductionType: (True, False),
                                DailyByZoneAndProductionType: (True, True),
                                DailyByZone: (False, True),
                                DailyControls: (False, False)}[model]
    filter_sequence, columns = construct_iterating_combination_filter_dictionary(iteration, iterate_pt, iterate_zone, zone=zone)
    lines = []
    for filter_dict in filter_sequence:
        lines.append(list(model.objects.filter(**filter_dict).order_by('day').values_list(field_name, flat=True)))

    return lines, columns


def extend_last_day_lines(lines, model, field_name):
    """Turns the ragged edge caused by different iterations ending on different days into
    a series of flat lines at their ending value.  Implemented for Issue #159"""
    time_series = []
    max_size = max([len(x) for x in lines])
    time_series.append(range(1, max_size + 1))  # Start with day index
    cumulative_field = 'new' not in model._meta.get_field_by_name(field_name)[0].verbose_name.lower()
        
    for line in lines:
        if cumulative_field:
            last_value = line[-1]
        else:  # This field is non-cumulative, default to zero
            last_value = 0
        missing_values = max_size - len(line)
        time_series.append(line + [last_value] * missing_values)
    return list(zip(*time_series))


def field_is_cumulative(explanation):
    return 'new' not in explanation.lower()


def collect_boxplot_data(ragged_lines, explanation):
    """Returns a tuple with all the data necessary to make a boxplot distribution.  For 'cumulative' fields,
    this is the last day.  For non-cumulative, it is the range of non-blank values.  Issue #159:
    https://github.com/NAVADMC/SpreadModel/issues/159#issuecomment-53058264"""
    if not field_is_cumulative(explanation):  # This field is non-cumulative, default to zero
        boxplot_data = tuple(chain(*ragged_lines))  # pile together all the data, but don't include trailing zeroes
    else:  # this field is cumulative
        boxplot_data = (line[-1] for line in ragged_lines)  # only last day is relevant
    return boxplot_data


def graph_field_png(request, model_name, field_name, iteration='', zone=''):
    model = globals()[model_name]
    lines, columns = create_time_series_lines(field_name, model, iteration=iteration, zone=zone)
    
    time_series = extend_last_day_lines(lines, model, field_name)
    time_data = pd.DataFrame.from_records(time_series, columns=columns)  # keys should be same ordering as the for loop above
    time_data = time_data.set_index('Day')

    explanation = model._meta.get_field_by_name(field_name)[0].verbose_name
    iter_str = ", iteration " + str(iteration) if iteration else 'for all iterations'
    title = "%s in \n%s %s" % (explanation, spaces_for_camel_case(model_name), iter_str)
    
    # plt.xkcd(scale=.5, randomness=1)
    fig = plt.figure(figsize=(6, 4), dpi=100, tight_layout=True, facecolor='w')
    matplotlib.rcParams.update({'font.size': 10})
    gs = gridspec.GridSpec(1, 2, width_ratios=[6, 1])
    time_graph = fig.add_subplot(gs[0], title=title)
    boxplot_graph = fig.add_subplot(gs[1], sharey=time_graph, )
    plt.locator_params(nbins=4)
    # http://stackoverflow.com/questions/4209467/matplotlib-share-x-axis-but-dont-show-x-axis-tick-labels-for-both-just-one
    plt.setp(boxplot_graph.get_yticklabels(), visible=False)
    for axis in [time_graph, boxplot_graph]:
        rstyle(axis)


    # Manually scale zone graphs based on the Max for any zone (universal value)
    if "Zone" in model_name:
        ymax = model.objects.filter(zone__isnull=False).aggregate(  # It's important to filter out Background stats from this Max
            Max(field_name))[field_name + '__max'] * 1.05
        time_graph.set_ylim(0.0, ymax)
        boxplot_graph.set_ylim(0.0, ymax)
    time_data.plot(ax=time_graph)

    
    boxplot_raw = collect_boxplot_data(lines, explanation)  # This uses the original lines because the ragged shape is important
    boxplot_data = pd.DataFrame(pd.Series(boxplot_raw), columns=['Last Day'] if field_is_cumulative(explanation) else ['Distribution'])
    boxplot_data.boxplot(ax=boxplot_graph, return_type='axes')
    #if there are more than 11 iterations, hide or truncate the legend
    if len(columns) > 11:
        time_graph.legend().set_visible(False)

    return HttpFigure(fig)
