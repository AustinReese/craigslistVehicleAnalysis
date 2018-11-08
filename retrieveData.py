import os.path
import pandas as pd
import numpy as np
from flask_wtf import FlaskForm
from wtforms import Form, SelectField, validators
from wtforms.validators import Length, ValidationError, DataRequired

categorical = [
    "city", "manufacturer", "make", "condition", "cylinders", "fuel",
    "title_status", "transmission", "drive", "size", "type", "paint_color"
]   

floaters = [
    "price", "year", "odometer", "lat", "long"
]

def createDataset():
    exists = os.path.isfile("craigslistVehicles.csv")
    if not exists:
        return None
    return pd.read_csv("craigslistVehicles.csv")

class getLineGraphCriteria(FlaskForm):
    ctg = []
    flt = []
    categorical.remove("city")
    categorical.append("year")
    floaters.remove("lat")
    floaters.remove("long")
    floaters.remove("year")
    
    for i in categorical:
        ctg.append((i, i.title()))
    for i in floaters:
        flt.append((i, i.title()))
    
    catDropdown = SelectField("Category", choices = ctg)
    fltDropdown = SelectField("Numeric Value", choices = flt)   
        
