from retrieveData import createDataset
import plotly as py
import plotly.figure_factory as ff
import pandas as pd
import numpy as np

FILE_NAME = "craigslistVehiclesReduced.csv"

def drawMap(data):
    py.tools.set_credentials_file(username="reesau01", api_key="yjUva46BiW9MhKLlFvgE")
    
    counties = data.groupby(by='county_fips', as_index=False).agg({'url': pd.Series.nunique})
    countyMeans = data.groupby(by = "county_fips", as_index = False)["price"].mean()
    
    counties = counties.rename(columns={"url": "fip_count"})
    
    fips = counties.county_fips.astype("int").tolist()
    counts = counties.fip_count.tolist()
    avgPrices = countyMeans.price.fillna(0).astype("int").tolist()
    
    reducedPrices = []
    for i in avgPrices:
        reducedPrices.append(i / 1000)
    
    fig = ff.create_choropleth(
        fips = fips,
        values = counts,
        county_outline = {'color': 'rgb(255,255,255)', 'width': 0.5}, 
        round_legend_values = True,
        legend_title='Sales by County', title='Cars for sale across America'
    )
    
    py.plotly.plot(fig, filename="carSales", auto_open = True)
    
    fig = ff.create_choropleth(
        fips = fips,
        values = reducedPrices,
        county_outline = {'color': 'rgb(255,255,255)', 'width': 0.5}, 
        round_legend_values = True,
        legend_title='Price by County', title='Average Price by County'
    )
    
    py.plotly.plot(fig, filename="avgPrices", auto_open = True)
    
drawMap(createDataset(FILE_NAME))