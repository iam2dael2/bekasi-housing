from flask import Flask, url_for, redirect, request, render_template
from flask_bootstrap import Bootstrap4
from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired
import numpy as np
import pandas as pd
import pickle
import sklearn

app = Flask(__name__)
app.secret_key = "any-string-you-want-just-keep-it-secret"

bootstrap = Bootstrap4(app)


class HouseForm(FlaskForm):
    bedroom = IntegerField("Bedrooms", validators=[DataRequired()])
    bathroom = IntegerField("Bathrooms", validators=[DataRequired()])
    land_area = IntegerField("Land Area (m2)", validators=[DataRequired()])
    building_area = IntegerField("Building Area (m2)", validators=[DataRequired()])
    electric_power = IntegerField("Electric Power (Watt)", validators=[DataRequired()])
    floor_num = IntegerField("Number of Floors", validators=[DataRequired()])
    prop_cond = SelectField("Property Condition",
                            choices=[(0, "New"), (1, "Good"), (2, "Renovated"), (3, "Needs Renovation")],
                            validators=[DataRequired()])
    furn_cond = SelectField("Furniture Condition",
                            choices=[(0, "Unfurnished"), (1, "Semi Furnished"), (2, "Furnished")],
                            validators=[DataRequired()])
    certificate = SelectField("Certificate",
                              choices=[("SHM - Sertifikat Hak Milik", "SHM - Sertifikat Hak Milik"),
                                       ("HGB - Hak Guna Bangunan", "HGB - Hak Guna Bangunan"),
                                       ("Lainnya (PPJB, Girik, Adat, dll)", "Lainnya (PPJB, Girik, Adat, dll)")],
                              validators=[DataRequired()])
    submit = SubmitField("Submit")


def convert_data(data):
    filename = "../encoder.sav"
    enc = pickle.load(open(filename, 'rb'))

    new_data = pd.DataFrame(data=[data],
                            columns=["bedroom", "bathroom", "land_area", "building_area", "electric_power", "floor_num",
                                     "prop_cond", "furn_cond", "certificate"])
    cert_encoded = enc.transform(new_data[["certificate"]]).toarray()[0]
    result = np.array([data[:-1] + list(cert_encoded)])
    return result


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=['GET', 'POST'])
def predict():
    is_predict = False
    house_form = HouseForm()
    if request.method == "POST":
        bedroom = house_form.bedroom.data
        bathroom = house_form.bathroom.data
        land_area = house_form.land_area.data
        building_area = house_form.building_area.data
        electric_power = house_form.electric_power.data
        floor_num = house_form.floor_num.data
        prop_cond = house_form.prop_cond.data
        furn_cond = house_form.furn_cond.data
        certificate = house_form.certificate.data

        data = [bedroom, bathroom, land_area, building_area, electric_power, floor_num, prop_cond, furn_cond, certificate]
        new_data = convert_data(data)

        is_predict = True
        model_filename = "../model.sav"
        model = pickle.load(open(model_filename, 'rb'))
        prediction = "{:,}".format(round(model.predict(new_data)[0] * 10**9))

        return render_template("generic.html", is_predict=is_predict, prediction=prediction)
    return render_template("generic.html", form=house_form, is_predict=is_predict)


if __name__ == "__main__":
    app.run(debug=True)
