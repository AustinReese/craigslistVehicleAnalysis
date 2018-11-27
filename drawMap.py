from retrieveData import createDataset
import plotly as py
import plotly.figure_factory as ff
import pandas as pd
import numpy as np

FILE_NAME = "craigslistVehiclesFull.csv"

def drawMap(data):
    py.tools.set_credentials_file(username="reesau01", api_key="yjUva46BiW9MhKLlFvgE")
    
    counties = data.groupby(by='county_fips', as_index=False).agg({'url': pd.Series.nunique})
    counties = counties.rename(columns={"url": "fip_count"})
    
    fips = counties.county_fips.tolist()
    counts = counties.fip_count.tolist()
    
    fig = ff.create_choropleth(
        fips = fips,
        values = counts,
        county_outline = {'color': 'rgb(255,255,255)', 'width': 0.5}, 
        round_legend_values = True,
        legend_title='Sales by County', title='Cars for sale across America'
    )
    
    py.plotly.plot(fig, filename="hello", auto_open = True)
    
drawMap(createDataset(FILE_NAME))