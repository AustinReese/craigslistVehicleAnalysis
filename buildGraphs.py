import pandas as pd
import numpy as np
import matplotlib
#multithreading to prevent crashes
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os.path
import folium
import operator
from folium import plugins
from flask import make_response

def lineGraphAvg(data, form):
    x = form.fltOne.data
    y = form.fltTwo.data
    cat = form.cat.data
    fileName = "static/{}+{}+{}+line.png".format(x, y, cat)    
    exists = os.path.isfile(fileName)
    if exists:
        return fileName
    data[x] = data[x].round(decimals=-3)
    data[y] = data[y].round(decimals=-3)
    medianY = data.groupby(x)[y].median()
    medianYRolling = medianY.rolling(75).mean()
    xData = medianYRolling.index.values
    yData = medianYRolling.values
    fig, ax = plt.subplots(figsize = (16, 16))
    ax.set_title("{} and {}".format(x.title(), y.title()))
    ax.set_ylabel(y)
    ax.set_xlabel(x)
    ax.plot(xData, yData, label="All {}s".format(cat))
    catValues = data[cat].value_counts()
    for i in catValues.iteritems():
        catData = data[data[cat].values == i[0]]
        medianY = catData.groupby(x)[y].median()
        medianYRolling = medianY.rolling(25).mean()
        xData = medianYRolling.index.values
        yData = medianYRolling.values
        ax.plot(xData, yData, label=i[0])
    ax.legend(loc="upper left")
    plt.savefig(fileName)
    return fileName

    
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
    fileName = "static/{}+{}+bar".format(categorical, floating)
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
