import pandas as pd
import panel as pn
import hvplot.pandas
import holoviews as hv
from holoviews.operation.timeseries import rolling, rolling_outlier_std

hv.extension('bokeh')

def map(widget):
    df = pd.read_csv("./data/stations_start.csv")
    return df.hvplot.points("lon", "lat",
                         geo=True,
                         responsive=True,
                         hover_cols="value",
                         title=str(widget))


widget = pn.widgets.IntSlider(name='Value', value=10, start=1, end=3000)

pn.Column(widget)
dmap = hv.DynamicMap(pn.bind(map, widget=widget))


pn.Row(pn.WidgetBox('## Map Filter', widget), 
             dmap).servable().show()
