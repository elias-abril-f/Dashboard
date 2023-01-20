import panel as pn
import plotly.graph_objects as go
import pandas as pd
from panel.template import FastGridTemplate, DarkTheme
import param
import holoviews as hv
import hvplot.pandas
    
df5 = pd.read_csv("./../pop.csv")
df3 = pd.read_csv("./data/trips_by_hour.csv", sep=",")
df4 = pd.read_csv("./data/trips_by_weekday.csv", sep=",")
df3["mean"] = df3["trips"].mean()

fig = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 50,
      thickness = 20,
      label = df5["source"],
      line = dict(color = "black", width = 0.5),
    ),
    link = dict(
      source = df5["sourceid"], # indices correspond to labels, eg A1, A2, A1, B1, ...
      target = df5["targetid"],
      value = df5["value"]
  ))])
def _create_barandline(data, main, accent, title="Title"):
    
    class Plot(param.Parameterized):        
        def create_plot(self):
            
            def hooks(plot, element):
                p = plot.state
                p.toolbar.autohide = True
                p.toolbar.logo = None
                p.yaxis.ticker=[0,2000000,4000000,6000000,8000000]
                p.yaxis.major_label_overrides={0:"0",2000000:"2M",4000000:"4M",6000000:"6M",8000000:"8M"} 
                
            return data.hvplot(kind="bar",
                            x="time",
                            title=title,
                            y="trips",
                            color=main,
                            xlabel="Hour",
                            line_color="white",
                            responsive=True,
                            min_width=350,
                            min_height=250,
                            ylabel="Trips",
                            label="Trips").opts(legend_position='right', hooks=[hooks]) \
                                * data.hvplot(kind="line",
                                            x="time",
                                            y="mean",
                                            responsive=True,
                                            color = accent, 
                                            line_color="white",
                                            label="Mean")
        def view(self):
            plot = hv.DynamicMap(self.create_plot)
            return plot
        
    p = Plot()
    return pn.Column(p.view, sizing_mode="stretch_both", margin=(-20,0))
sankey = pn.Column(pn.pane.Plotly(fig, width=500,height=500))

template = FastGridTemplate(
    title="London TFL Bike Journeys Dashboard",
    row_height=55,
    prevent_collision=True,
    save_layout=True,
    theme=DarkTheme,
    theme_toggle=False,
    sidebar = [pn.pane.Markdown("# **INSTRUCTIONS**\n- All the panels are fully resoponsive. You can move them and resize them and their content adapts to the new size\n\n- Click and drat a panel from the top left corner to move it. \n\n- Collitions as diabled to avoid panels jumping all over the place. Move a panel out of the way before attempting to move another one into that spot. \n\n- Click and drag the bottom right corner to resize a panel.\n\n- If you press the top right corner you can see that panel fullscreen\n\n- Click the hamburger menu in the header to close the sidebar and enjoy the dashboard full size. \n\n- In the right end of the header you have 2 icons. The first one reset the layout and the second one is the activity indicator")]
)



template.main[8:13, 0:12] = _create_barandline(data=df3, main="#78C0E0", accent="#449DD1", title="Trips by time of day")
template.main[0:6, 0:6] = sankey

template.show()