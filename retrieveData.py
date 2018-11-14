import os.path
import pandas as pd
import numpy as np
from flask_wtf import FlaskForm
from wtforms import Form, SelectField, validators
from wtforms.validators import Length, ValidationError, DataRequired

categorical = [
    "manufacturer", "condition", "cylinders", "fuel", "year",
    "title_status", "transmission", "drive", "size", "type", "paint_color"
]   

floaters = [
    "price", "year", "odometer"
]

def createDataset():
    exists = os.path.isfile("craigslistVehicles.csv")
    if not exists:
        return None
    data = pd.read_csv("craigslistVehicles.csv")
    return cleanData(data)
    
def cleanData(data):
    data.price = data.price[~((data.price-data.price.mean()).abs() > .05*data.price.std())]
    data.odometer = data.odometer[~((data.odometer-data.odometer.mean()).abs() > 3*data.odometer.std())]
    data.year = data.year[~((data.year-data.year.mean()).abs() > 10*data.year.std())]
    return data

class getBarGraphCriteria(FlaskForm):
    ctg = []
    flt = []
    
    for i in categorical:
        ctg.append((i, i.title()))
    for i in floaters:
        flt.append((i, i.title()))
    
    catDropdown = SelectField("Category", choices = ctg)
    fltDropdown = SelectField("Numeric Value", choices = flt)

class getLineGraphCriteria(FlaskForm):
    ctg = [("no_category", "No Category")]
    flt = []
    
    for i in categorical:
        ctg.append((i, i.title()))
    for i in floaters:
        flt.append((i, i.title()))
    cat = SelectField("Category", choices = ctg)
    fltOne = SelectField("X Axis", choices = flt)
    fltTwo = SelectField("Y Axis", choices = flt)
    
