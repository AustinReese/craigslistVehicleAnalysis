from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import Form, SelectField, validators
from wtforms.validators import Length, ValidationError, DataRequired
import buildGraphs
import retrieveData

app = Flask(__name__)
# so very secret...
app.config['SECRET_KEY'] = "CraigsistFilter"
bootstrap = Bootstrap(app)

data = retrieveData.createDataset()

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/lineGraphs", methods=["GET", "POST"])
def lineGraphs():
    form = retrieveData.getLineGraphCriteria()
    if form.is_submitted():
        img = buildGraphs.genericBarGraph(data, form)
        return render_template("lineGraphs.html", form = form, img = img)
    return render_template("lineGraphs.html", form = form, img = None)

@app.route("/heatMap")
def heatMap():
    buildGraphs.buildHeatmap(data)
    return render_template("carMap.html")

if __name__ == "__main__":
    app.run(debug=True)