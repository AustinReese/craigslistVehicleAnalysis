import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
from folium import plugins
from flask import make_response


def cleanData(data):
    data.price = data.price[~((data.price-data.price.mean()).abs() > .05*data.price.std())]
    data.odometer = data.odometer[~((data.odometer-data.odometer.mean()).abs() > 2*data.odometer.std())]    
    return data

def linePlotOdomPrice(data):
    #data.plot.scatter(x="price", y="odometer", c="Red")
    data.odometer = data.odometer.round(decimals=-3)
    medianPrice = data.groupby("odometer")["price"].median()
    medianPriceRolling = medianPrice.rolling(75).mean()
    odometers = medianPriceRolling.index.values
    prices = medianPriceRolling.values
    fig, ax = plt.subplots(figsize = (16, 16))
    ax.set_title("Price and Odometer Reading")
    ax.set_ylabel("Price (In Dollars)")
    ax.set_xlabel("Odometer (In Miles)")
    ax.plot(odometers, prices, label="All Types")
    types = data.type.value_counts()
    for i in types.iteritems():
        typeData = data[data.type.values == i[0]]
        medianPrice = typeData.groupby("odometer")["price"].median()
        medianPriceRolling = medianPrice.rolling(75).mean()
        odometers = medianPriceRolling.index.values
        prices = medianPriceRolling.values
        ax.plot(odometers, prices, label=i[0])
    ax.legend(loc="upper left")
    plt.show()
    
def buildHeatmap(data):
    data = data[np.isfinite(data["lat"])]
    carMap = folium.Map(location = [41, -96], zoom_start=4)
    heatArr = data[["lat", "long"]].as_matrix()
    carMap.add_child(plugins.HeatMap(heatArr, radius=15))
    carMap.save("/templates/carMap.html")
    
def genericBarGraph(data, form):
    categorical = form.catDropdown.data
    floating = form.fltDropdown.data
    uniqueCategorical = data[categorical].value_counts()
    uniqueList = []
    floatingMedians = []
    for i in uniqueCategorical.iteritems():
        uniqueList.append(i[0])
        floatingMedians.append(data[floating][data[categorical].values == i[0]].median())
    plt.bar(uniqueList, floatingMedians)
    plt.show()
    