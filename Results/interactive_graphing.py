"""
Example taken from: http://mpld3.github.io/examples/scatter_tooltip.html

Scatter Plot With Tooltips
==========================
A scatter-plot with tooltip labels on hover.  Hover over the points to see
the point labels.
Use the toolbar buttons at the bottom-right of the plot to enable zooming
and panning, and to reset the view.
"""
from django.http import HttpResponse

from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
import numpy as np
import mpld3
from Results.models import Unit
from Results.summary import list_of_iterations


def population_d3_map(request):
    fig, ax = plt.subplots(subplot_kw=dict(axisbg='#EEEEEE'), figsize=(9,9))
    pop_size = Unit.objects.count()

    latlong = [(u.latitude, u.longitude, "%s %s %i"%(u.production_type.name, u.user_notes, u.unitstats.cumulative_infected), u.unitstats.cumulative_infected) for u in Unit.objects.all()]
    latitude, longitude, names, number_infected = zip(*latlong)
    total_iterations = float(len(list_of_iterations()))  # This is slower but more accurate than OutputSettings[0].iterations
    
    red_spectrum = ListedColormap([(1.0, 1.0, 0.8), (1.0, 0.929, 0.627), (0.996, 0.851, 0.463), (0.996, 0.698, 0.298), (0.992, 0.553, 0.235), 
                                   (0.988, 0.306, 0.165), (0.89, 0.102, 0.11), (0.741, 0.0, 0.149), (0.502, 0.0, 0.149)], 
                                  name=u'from_list', N=None)
    scatter = ax.scatter(latitude,
                         longitude,
                         c=[x / total_iterations for x in number_infected],
                         s=[30] * pop_size,  # Size in square pixels
                         alpha=0.5,
                         cmap=red_spectrum,
                         linewidths=0)
    ax.grid(color='white', linestyle='solid')
    
    ax.set_title("Population Locations and IDs", size=20)
    
    tooltip = mpld3.plugins.PointLabelTooltip(scatter, labels=names)
    mpld3.plugins.connect(fig, tooltip)
    
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
    
    fig, ax = plt.subplots(subplot_kw={'xticks': [], 'yticks': []})
    lines = ax.plot(x, y.T, color='blue', lw=4, alpha=0.1)
    plugins.connect(fig, HighlightLines(lines))
    
    html = mpld3.fig_to_html(fig, d3_url=None, mpld3_url=None, no_extras=False,
                             template_type="general", figid=None, use_http=False)
    return HttpResponse(html)