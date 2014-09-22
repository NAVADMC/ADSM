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

import matplotlib.pyplot as plt
import numpy as np
import mpld3

def scatterplot_demo(request):
    fig, ax = plt.subplots(subplot_kw=dict(axisbg='#EEEEEE'))
    N = 100000
    
    scatter = ax.scatter(np.random.normal(size=N),
                         np.random.normal(size=N),
                         c=np.random.random(size=N),
                         s=1000 * np.random.random(size=N),
                         alpha=0.3,
                         cmap=plt.cm.jet)
    ax.grid(color='white', linestyle='solid')
    
    ax.set_title("Scatter Plot (with tooltips!)", size=20)
    
    labels = ['point {0}'.format(i + 1) for i in range(N)]
    tooltip = mpld3.plugins.PointLabelTooltip(scatter, labels=labels)
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