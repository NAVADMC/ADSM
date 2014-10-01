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

from django.http import HttpResponse
from matplotlib.colors import ListedColormap
from matplotlib.patches import Circle
from matplotlib import pyplot, colors
import numpy as np
import mpld3
from Results.models import Unit
from Results.summary import list_of_iterations
from math import ceil


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
    kilometers_in_one_latitude_degree = 111.13  # https://au.answers.yahoo.com/question/index?qid=20100815170802AAZe1AZ
    for i, freq in [(index, n_times) for index, n_times in enumerate(zone_focus) if n_times > 0]:
        ax.add_patch(Circle(xy=(latitude[i], longitude[i]),
                            color=zone_blues(freq / total_iterations),
                            radius=15.0 / kilometers_in_one_latitude_degree,
                            linewidth=0,
                            zorder=freq,
        ))



def population_d3_map(request):
    fig, ax = pyplot.subplots(subplot_kw=dict(axisbg='#DDDDDD'), figsize=(12,12))
    ax.grid(color='white', linestyle='solid')
    ax.set_title("Population Locations and IDs", size=20)

    pop_size = Unit.objects.count()
    total_iterations = float(len(list_of_iterations()))  # This is slower but more accurate than OutputSettings[0].iterations
    queryset = Unit.objects.all().order_by('unitstats__cumulative_infected')  # sort by N infected
    # It might be faster to request a flat value list and then construct new tuples based on that
    latlong = [(u.latitude, u.longitude, u.unitstats.cumulative_infected, u.unitstats.cumulative_zone_focus, u.unitstats.cumulative_destroyed,
                "%s %s %i" % (u.production_type.name, u.user_notes, u.unitstats.cumulative_destroyed) 
                ) for u in queryset]
    latitude, longitude, number_infected, zone_focus, destroyed, names = zip(*latlong)
    zone_blues, red_infected, green_vaccinated = define_color_mappings()

    graph_zones(ax, latitude, longitude, total_iterations, zone_blues, zone_focus)
    
    #the relation between sizes and black_rings was calculated to preserve the size of the inner colored dot,
    #the ratio compensates for size being squared and half the radius being eaten by the line width,
    #this ratio would probably be thrown off if you change the starting square pixels from 30.  Don't do that.
    sizes = [30 + ((d/total_iterations)/.0866)**2 for d in destroyed]  # Size in square pixels
    black_rings = [ceil((d/total_iterations)/.15) for d in destroyed]
    
    # to ensure zero occurrences has a different color
    non_zero_values = colors.Normalize(vmin=.001, vmax=1.0, clip=False)
    red_infected.set_under((0.6, 0.6, 0.6, 1.0))  # dark grey
    infected = ax.scatter(latitude,
                         longitude,
                         c=[x / total_iterations for x in number_infected],
                         s=sizes,
                         alpha=1.0,
                         cmap=red_infected,
                         norm=non_zero_values,
                         edgecolor='k',
                         linewidths=black_rings,
                         zorder=2000)
    # Begin mpld3 specific code
    tooltip = mpld3.plugins.PointLabelTooltip(infected, labels=names)
    mpld3.plugins.connect(fig, tooltip)


    # destroyed = ax.scatter(latitude,
    #                        longitude,
    #                        c='black',
    #                        s=[30] * pop_size,  # Size in square pixels
    #                        alpha=1.0,
    #                        linewidths=0,
    #                        zorder=1000)
   
    
    html = mpld3.fig_to_html(fig, d3_url=None, mpld3_url=None, no_extras=False,
                template_type="general", figid=None, use_http=False)
    return HttpResponse(html)



from mpld3 import plugins, utils


class HighlightLines(plugins.PluginBase):
    """A plugin to highlight lines on hover
    http://mpld3.github.io/examples/random_walk.html"""

    JAVASCRIPT = """
    mpld3.register_plugin("linehighlight", LineHighlightPlugin);
    LineHighlightPlugin.prototype = Object.create(mpld3.Plugin.prototype);
    LineHighlightPlugin.prototype.constructor = LineHighlightPlugin;
    LineHighlightPlugin.prototype.requiredProps = ["line_ids"];
    LineHighlightPlugin.prototype.defaultProps = {alpha_bg:0.3, alpha_fg:1.0}
    function LineHighlightPlugin(fig, props){
        mpld3.Plugin.call(this, fig, props);
    };

    LineHighlightPlugin.prototype.draw = function(){
      for(var i=0; i<this.props.line_ids.length; i++){
         var obj = mpld3.get_element(this.props.line_ids[i], this.fig),
             alpha_fg = this.props.alpha_fg;
             alpha_bg = this.props.alpha_bg;
         obj.elements()
             .on("mouseover", function(d, i){
                            d3.select(this).transition().duration(50)
                              .style("stroke-opacity", alpha_fg); })
             .on("mouseout", function(d, i){
                            d3.select(this).transition().duration(200)
                              .style("stroke-opacity", alpha_bg); });
      }
    };
    """

    def __init__(self, lines):
        self.lines = lines
        self.dict_ = {"type": "linehighlight",
                      "line_ids": [utils.get_id(line) for line in lines],
                      "alpha_bg": lines[0].get_alpha(),
                      "alpha_fg": 1.0}


def random_walk(request, n_paths, n_steps):
    n_paths = int(n_paths)
    n_steps = int(n_steps)
    
    x = np.linspace(0, 50, n_steps)
    y = 0.1 * (np.random.random((n_paths, n_steps)) - 0.5)
    y = y.cumsum(1)
    
    fig, ax = pyplot.subplots(subplot_kw={'xticks': [], 'yticks': []})
    lines = ax.plot(x, y.T, color='blue', lw=4, alpha=0.1)
    plugins.connect(fig, HighlightLines(lines))
    
    html = mpld3.fig_to_html(fig, d3_url=None, mpld3_url=None, no_extras=False,
                             template_type="general", figid=None, use_http=False)
    return HttpResponse(html)