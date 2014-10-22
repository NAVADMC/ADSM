"""
Example taken from: http://mpld3.github.io/examples/scatter_tooltip.html

Scatter Plot With Tooltips
==========================
A scatter-plot with tooltip labels on hover.  Hover over the points to see
the point labels.
Use the toolbar buttons at the bottom-right of the plot to enable zooming
and panning, and to reset the view.
"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_hooks()
from future.builtins import *

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.colors import ListedColormap
from matplotlib.patches import Circle, Rectangle
from matplotlib import pyplot
import os
from django.http import HttpResponse
from django.db.models import Max

from Results.models import Unit
from Results.summary import list_of_iterations, iteration_progress
from Results.graphing import rstyle, population_png
from Settings.views import workspace_path
from Settings.models import scenario_filename
from ScenarioCreator.models import Zone


kilometers_in_one_latitude_degree = 111.13  # https://au.answers.yahoo.com/question/index?qid=20100815170802AAZe1AZ


def define_color_mappings():
    zone_blues = [(0.9686, 0.9843, 1.0),
                  (0.8706, 0.9216, 0.9686),
                  (0.7765, 0.8588, 0.9373),
                  (0.6196, 0.7922, 0.8824),
                  (0.4196, 0.6824, 0.8392),
                  (0.2588, 0.5725, 0.7765),
                  (0.1294, 0.4431, 0.7098),
                  (0.0314, 0.3176, 0.6118),
                  (0.0314, 0.1882, 0.4196)]
    red_infected = [# (1.0, 0.929, 0.627),
                    (0.996, 0.851, 0.463),  # this spectrum has a bit of orange in it
                    (0.996, 0.698, 0.298), 
                    (0.992, 0.553, 0.235),    
                    (0.988, 0.306, 0.165), 
                    (0.89, 0.102, 0.11), 
                    (0.741, 0.0, 0.149), 
                    (0.502, 0.0, 0.149)]
    green_vaccinated = [(0.9686, 0.9882, 0.9608),
                        (0.898, 0.9608, 0.8784),
                        (0.7804, 0.9137, 0.7529),
                        (0.6314, 0.851, 0.6078),
                        (0.4549, 0.7686, 0.4627),
                        (0.2549, 0.6706, 0.3647),
                        (0.1373, 0.5451, 0.2706),
                        (0.0, 0.4275, 0.1725),
                        (0.0, 0.2667, 0.1059)]

    return [ListedColormap(x) for x in [zone_blues, red_infected, green_vaccinated]]


def graph_zones(ax, latitude, longitude, total_iterations, zone_blues, zone_focus):
    largest_zone_radius = Zone.objects.aggregate(Max('radius'))['radius__max']
    for i, freq in [(index, n_times) for index, n_times in enumerate(zone_focus) if n_times > 0]:
        ax.add_patch(Circle(xy=(longitude[i], latitude[i]),
                            color=zone_blues(freq / total_iterations),
                            radius= largest_zone_radius / kilometers_in_one_latitude_degree,
                            linewidth=0,
                            zorder=freq,
        ))


def graph_states(ax, latitude, longitude, total_iterations, infected, vaccinated, destroyed):
    marker_size = 3.0
    width = marker_size / kilometers_in_one_latitude_degree / 3
    half = width * 1.5
    for i in range(len(infected)):
        if infected[i] > 0:
            ax.add_patch(Rectangle(xy=(longitude[i] - half, latitude[i] - half),
                                   color = (0.89, 0.102, 0.11),
                                   width = width,
                                   height= marker_size / kilometers_in_one_latitude_degree * (infected[i] / total_iterations),
                                   zorder=2000))
        if vaccinated[i] > 0:
            ax.add_patch(Rectangle(xy=(longitude[i] - width *.5, latitude[i] - half),
                                   color=(0.2549, 0.6706, 0.3647),
                                   width= width,
                                   height= marker_size / kilometers_in_one_latitude_degree * (vaccinated[i] / total_iterations),
                                   zorder=2000))
        if destroyed[i] > 0:
            ax.add_patch(Rectangle(xy=(longitude[i] + width * .5, latitude[i] - half),
                                   color=(0.3, 0.27, 0.27),
                                   width=width,
                                   height= marker_size / kilometers_in_one_latitude_degree * (destroyed[i] / total_iterations),
                                   zorder=2000))
        if infected[i] > 0 or vaccinated[i] > 0 or destroyed[i] > 0:
            ax.add_patch(Rectangle(xy=(longitude[i] - half, latitude[i] - half),
                                   fill=None,
                                   alpha=0.1,
                                   edgecolor='k',
                                   linestyle='solid',
                                   width=width*3,
                                   height=width*3,
                                   zorder=1500))


def population_results_map(request):
    fig, ax = pyplot.subplots(subplot_kw=dict(axisbg='#DDDDDD'), figsize=(58.5,52), frameon=True)
    pyplot.tight_layout()
    ax.autoscale_view('tight')
    ax.grid(color='white', linestyle='solid')
    rstyle(ax)
    ax.set_title("Population Locations and IDs", size=20)

    queryset = Unit.objects.all()
    # It might be faster to request a flat value list and then construct new tuples based on that
    latlong = [(u.latitude, u.longitude, 
                u.unitstats.cumulative_infected, 
                u.unitstats.cumulative_vaccinated,
                u.unitstats.cumulative_destroyed,
                u.unitstats.cumulative_zone_focus, 
                "%s %s %i" % (u.production_type.name, u.user_notes, u.unitstats.cumulative_destroyed) 
                ) for u in queryset]
    total_iterations = float(len(list_of_iterations()))  # This is slower but more accurate than OutputSettings[0].iterations
    latitude, longitude, infected, vaccinated, destroyed, zone_focus, names = zip(*latlong)
    zone_blues, red_infected, green_vaccinated = define_color_mappings()
    
    graph_zones(ax, latitude, longitude, total_iterations, zone_blues, zone_focus)
    graph_states(ax, latitude, longitude, total_iterations, infected, vaccinated, destroyed)  
    
    longitude = [entry[1] for entry in latlong if not any(x > 0 for x in (entry[2], entry[3], entry[4]))]
    latitude =  [entry[0] for entry in latlong if not any(x > 0 for x in (entry[2], entry[3], entry[4]))]
    # to ensure zero occurrences has a different color
    uninvolved = ax.scatter(longitude,
                            latitude,
                            marker='s',
                            s=70,
                            color=(0.6, 0.6, 0.6, 1.0),
                            linewidths=0,
                            zorder=1000)
    return fig


def population_d3_map(request):
    fig = population_results_map(request)
    # Begin mpld3 specific code
    # tooltip = mpld3.plugins.PointLabelTooltip(infected, labels=names)
    # mpld3.plugins.connect(fig, tooltip)

    
    # html = mpld3.fig_to_html(fig, d3_url=None, mpld3_url=None, no_extras=False,
    #             template_type="general", figid=None, use_http=False)
    return HttpResponse()#html)


def population_zoom_png(request):
    path = workspace_path(scenario_filename() + '/population_map.png')
    try:
        with open(path, "rb") as img_file:  #TODO: remove "rb"
            return HttpResponse(img_file.read(), mimetype="image/png")
    except IOError:
        print("Calculating a new Population Map")
        save_image = iteration_progress() == 1.0  # we want to check this before reading the stats, this is in motion
        if not save_image:  # in order to avoid database locked Issue #150
            return population_png(request, 58.5, 52)
        else:
            fig = population_results_map(request)
            response = HttpResponse(content_type='image/png')
            FigureCanvas(fig).print_png(response)
            if save_image:
                if not os.path.exists(workspace_path(scenario_filename())):
                    os.makedirs(workspace_path(scenario_filename()))
                FigureCanvas(fig).print_png(path)
            print("Finished Population Map")
            return response
