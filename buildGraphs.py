import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os.path
import folium
import operator
from folium import plugins
from flask import make_response

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
    exists = os.path.isfile("templates/carMap.html")
    if exists:
        return
    data = data[np.isfinite(data["lat"])]
    carMap = folium.Map(location = [41, -96], zoom_start=4)
    heatArr = data[["lat", "long"]].as_matrix()
    carMap.add_child(plugins.HeatMap(heatArr, radius=15))
    carMap.save("templates/carMap.html")
    
def genericBarGraph(data, form):
    categorical = form.catDropdown.data
    floating = form.fltDropdown.data
    fileName = "static/{}+{}".format(categorical, floating)
    exists = os.path.isfile(fileName + ".png")
    if exists:
        return fileName + ".png"
    uniqueCategorical = data[categorical].value_counts()
    uniqueList = []
    floatingMedians = []
    sortingDict = {}
    for i in uniqueCategorical.iteritems():
        sortingDict[i[0]] = data[floating][data[categorical].values == i[0]].median()
    sortedItems = sorted(sortingDict.items(), key=operator.itemgetter(1))
    for i in reversed(sortedItems):
        uniqueList.append(i[0])
        floatingMedians.append(i[1])
    plt.bar(uniqueList, floatingMedians)
    if categorical == "manufacturer":
        plt.xticks(rotation=90)
    if floating == "year":
        axes = plt.gca()
        axes.set_ylim([1960,2020])        
    plt.xlabel(categorical)
    plt.ylabel(floating)
    plt.gcf().subplots_adjust(bottom=0.3)
    fig = plt.gcf()
    fig.set_size_inches(10, 8)
    plt.savefig(fileName)
    plt.clf()
    return fileName + ".png"

def scratch():
    from retrieveData import createDataset
    data = createDataset()
    import seaborn as sns
    sns.set(style="whitegrid")
    ax = sns.violinplot(x=data.price)    
