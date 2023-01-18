# %% [markdown]
# Load the required libraries and frameworks

# %%

import holoviews as hv
import panel as pn
import numpy as np
import pandas as pd
import geopandas as gpd
import re
from panel.template import FastGridTemplate
from panel.template import DarkTheme
import hvplot.pandas
import param

# %% [markdown]
# Load the data and declare the colours to be used in the graphs.

# %%
df = pd.read_csv("./data/trips_by_year.csv", sep=",")
df2 = pd.read_csv("./data/trips_by_month.csv", sep=",")
df3 = pd.read_csv("./data/trips_by_hour.csv", sep=",")
df3["mean"] = df3["trips"].mean()


MAIN = "#D6ADD0"
ACCENT = "#724175"
HEADER_ACCENT = "#1c1c1c"

# %%
# NOT IN USE. USING CLASS NOW. 
def _KDIMS_create_barandlinewidget(data,title, x, xlabel):
   
    def plot(column="duration(year)"):
        def hooks(plot, element):
            p = plot.state
            p.toolbar.autohide = True
            p.toolbar.logo = None
            if "trips" in column:
                p.yaxis.ticker=[0,2000000,4000000,6000000,8000000]
                p.yaxis.major_label_overrides={0:"0",2000000:"2M",4000000:"4M",6000000:"6M",8000000:"8M"} 
            else:
                p.yaxis.ticker = np.arange(0, 1400, 200)
                p.yaxis.major_label.overrides={0:"0", 200:"200", 400:"400", 600:"600", 800:"800", 1000:"1000",1200:"1200", 1400:"1400"}
    
        return data.hvplot(kind="bar",
                           x=x,
                           title=title,
                           y=column,
                           color=MAIN,
                           xlabel=xlabel,
                           line_color="white",
                           responsive=True,
                           min_width=350,
                           min_height=250,
                           ylabel=re.sub(r"\([a-z,A-Z]*\)","", str(column)).capitalize(),
                           label=re.sub(r"\([a-z,A-Z]*\)","", str(column)).capitalize()).opts(legend_position='top', hooks=[hooks]) \
                               * data.hvplot(kind="line",
                                           x=x,
                                           y=f"mean{column}",
                                           responsive=True, 
                                           line_color="white",
                                           label="Mean")

    dmap = hv.DynamicMap(plot, kdims=["column"],sizing_mode="stretch_both").redim.values(column=[f"duration({x})", f"trips({x})"])
    hv_panel = pn.panel(dmap)
    widget = hv_panel[1]
    return pn.Column(
        pn.Row(*widget),
        hv_panel[0],
        
        sizing_mode="stretch_both",
    )

# %% [markdown]
# Create a function to create all the combo bar/line charts that can be drawn based on a widget that lets you select the Y axis. It creates the charts based on a parameterized class, that way the widget (selector, slider or any other type) is linked automaticaly, and the chart gets created by calling a self function and sent to a view function that creates a dynamic map, ensuring the chart will update as soon as anything is changed. 
# 
# # To fix https://panel.holoviz.org/user_guide/Param.html

# %%

def _create_barandlinewidget(data, x, title="Title"):
    class Plot(param.Parameterized):
        
        select_your_metric = param.ObjectSelector(default=f"trips({x})", objects=[f"duration({x})", f"trips({x})"])
        
        @param.depends("select_your_metric")
        def create_plot(self):
            
            def hooks(plot, element):
                p = plot.state
                p.toolbar.autohide = True
                p.toolbar.logo = None
                if "trips" in self.select_your_metric:
                    p.yaxis.ticker=[0,2000000,4000000,6000000,8000000]
                    p.yaxis.major_label_overrides={0:"0",2000000:"2M",4000000:"4M",6000000:"6M",8000000:"8M"} 
                else:
                    p.yaxis.ticker = np.arange(0, 1400, 200)
                    p.yaxis.major_label.overrides={0:"0", 200:"200", 400:"400", 600:"600", 800:"800", 1000:"1000",1200:"1200", 1400:"1400"}
    
                
            return data.hvplot(kind="bar",
                            x=x,
                            title=title,
                            y=self.select_your_metric,
                            color="#faceff",
                            xlabel=str(x).capitalize(),
                            line_color="white",
                            responsive=True,
                            min_width=350,
                            min_height=250,
                            ylabel=re.sub(r"\([a-z,A-Z]*\)","", str(self.select_your_metric)).capitalize(),
                            label=re.sub(r"\([a-z,A-Z]*\)","", str(self.select_your_metric)).capitalize()).opts(legend_position='top', hooks=[hooks]) \
                                * data.hvplot(kind="line",
                                            x=x,
                                            y=f"mean{self.select_your_metric}",
                                            responsive=True, 
                                            line_color="white",
                                            label="Mean")
        @param.depends("select_your_metric")
        def view(self):
            plot = hv.DynamicMap(self.create_plot)
            return plot
        
    p = Plot()
    return pn.Column(
            pn.Row(
            #pn.layout.VSpacer(sizing_model="stretch_both"),
            pn.Param(p.param,
                 show_name=False,
                 show_labels = False,
                 sizing_mode="stretch_both"               
                 ),sizing_mode="stretch_both"),
            pn.Row(
        p.view, sizing_mode="stretch_both"
    ),sizing_mode="stretch_both")


# %%
# NOT IN USE. WE'RE CLASSY NOW
def _NOTINUSE_create_barandline(data,title, x, y, y2, xlabel, ylabel, label, label2):
    def hooks(plot, element):
        p = plot.state
        p.toolbar.autohide = True
        p.toolbar.logo = None
        p.yaxis.ticker=[0,2000000,4000000,6000000,8000000]
        p.yaxis.major_label_overrides={0:"0",2000000:"2M",4000000:"4M",6000000:"6M",8000000:"8M"} 
        p.toolbar_location = "above"
 
    def plot():
        return data.hvplot.bar(title=title,
                               x=x,
                               xlabel=xlabel,
                               ylabel=ylabel,
                               y=y,
                               color=MAIN,
                               responsive=True,
                               line_color="white",
                               min_width=350,
                               min_height=250,
                               label=label).opts(legend_position="right",
                               hooks=[hooks]) \
        * df3.hvplot.line(x=x,
                          y=y2,
                          color=ACCENT,
                          responsive=True,
                          min_width=300,
                          min_height=150,
                          line_color="white",
                          label=label2)
    return pn.Column(
        pn.pane.HoloViews(hv.DynamicMap(plot), sizing_mode="stretch_both"),
                sizing_mode="stretch_both",
    )

# %% [markdown]
# Same as the combination chart, but without a widget to update since this chart doesn't have multiple metrics to show. 

# %%
def _create_barandline(data, title="Title"):
    
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
                            color=MAIN,
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
                                            line_color="white",
                                            label="Mean")
        def view(self):
            plot = hv.DynamicMap(self.create_plot)
            return plot
        
    p = Plot()
    
    return pn.Column(p.view, sizing_mode="stretch_both")

# %% [markdown]
# Now we create a map with all the docks. In this case, we remove the X and Y axis, since they dont offer any useful information.
# 
# Same as the other interactive plots that use panel widgets or parameters to filter or select data, we need to be careful not to have the same names (as in the columns or other keys used to select the target of the widget), because if the keyword is the same in different widgets, the plots targeted by those two widgets will become linked. The easiest solution is to name every data column (if using pandas dataframes) something different, for example, relating it to the general dataframe. Eg: if we have two dataframes df1 and df2 with the same columns height and width, we will name the columns height(df1) weight(df1) and height(df2) weight(df2)

# %%
def _create_map():
    df = pd.read_csv("./data/coordinatesClean.csv")
    def map():
        return df.hvplot.points("loncoord", "latcoord", geo=True, hover_cols='Name',tiles=True, xaxis=None, yaxis=None, color=ACCENT, responsive=True)
    return pn.Column(
        pn.pane.HoloViews(hv.DynamicMap(map), sizing_mode="stretch_both"),
                sizing_mode="stretch_both",
    )

# %% [markdown]
# Although this map looks very similar to the other one. This map has a slider that acts as a filter, showing you the most popular stations to start a trip starting at the value selected in the slider. 
# It works the same way as the other charts with widgets. The function creates a class with a function to create the plot/map, another one to create the dynamic map view and a hooks function to modify the look of the chart/map.

# %%
# maybe use geoviews in the future instead of hvplot for the map or folio leaflet
def create_mapymcmapface(url):
    class Map(param.Parameterized):
        
        data = pd.read_csv(url)
        value = param.Integer(default=97, bounds=(min(data["value"]), 300000))
        
        @param.depends('value')
        def create_map(self):
            def hooks(plot, element):
                p = plot.state
                p.toolbar.autohide= True
                p.toolbar.logo = None
            df = self.data.loc[self.data["value"] >= self.value]
            return df.hvplot.points('lon', 'lat', title="Most popular stations to start journeys",
                                    geo=True, tiles=True, hover_cols=["station","value"],xaxis=None, yaxis=None, color=ACCENT, responsive=True).opts(hooks=[hooks], framewise=True)
        @param.depends("value")
        def view(self):
            map = hv.DynamicMap(self.create_map)
            return map
        
    map = Map()
    return pn.Column(
        pn.Param(map.param, name="Foo"),
        map.view, sizing_mode="stretch_both")
    


# %% [markdown]
# Now we create the template to make our dashboard look good with minimal effort. In this case I chose the fastgridtemplate, as it allows the user to move and resize the panels, and as you might have noticed, all our charts and maps are responsive, which means they will change in size as we change the size of the panels or our explorer window.
# Also here we can create a header (and change its colours) and a sidebar (not used in this case). As well as other things like the panel collision, the height of the grid rows and other options. 

# %%
template = FastGridTemplate(
    title="London TFL Bike Journeys Dashboard",
    row_height=55,
    prevent_collision=True,
    save_layout=True,
    accent_base_color=HEADER_ACCENT,
    header_background=HEADER_ACCENT,
    header_accent_base_color="Light Coral",
    theme=DarkTheme,
    theme_toggle=False
)

# %% [markdown]
# Once the template is created, we can add as many panels as we want to the main (the body of the dashboard). We select the position of the added panel in the square brackets, for example, the first element below goes from the start to row 7 and from the start to column 6 and the second element from the start to row 5 and from column 6 to 11. 
#  we can also make use of other pn.pane objects like Markdown banners, spacers to make things tidy, etc.

# %%
template.main[:7, 0:6] = _create_map()
template.main[:6, 6:11] = _create_barandlinewidget(data=df2, title="Trips by month", x="month")
template.main[6:7, 6:11] = pn.pane.Markdown("      # Total Trips: 76450245",style={"margin-top":"-30px", "padding":"0,0,0,0"}, width=400, height=0, )
template.main[7:12, 0:11] = _create_barandline(data=df3, title="Trips by time of day")
template.main[12:18, 0:5] = _create_barandlinewidget(data=df, title="Trips by year", x="year")
template.main[18:19,0:5] = pn.Row(pn.pane.Markdown("#    🚴🚴🚴   Over 800 Docks   🚴🚴🚴",style={"margin-top": "-25px"}, width=400, height=10), scroll=False)
template.main[12:20,5:11] = create_mapymcmapface("./data/stations_start.csv")
template.main[20:20, 0:12] = pn.Spacer()

# %% [markdown]
# Lastly, we call our template object and make it servable to be able to use in our local network. If everything is ok, it will create a local server where our dashboard will run, and give us the address, which can be access from any computer in our local network. 
# #### Optional
# We can also show our dashboard (it will open in our default browser) and save it, which will create a html file with our dashboard. 

# %%
template.servable()
template.show()
template.save("./dashboardFastGrid.html")


