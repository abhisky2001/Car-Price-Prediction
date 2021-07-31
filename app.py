# -*- coding: utf-8 -*-
"""

@author: Abhinav Aravindan
"""

from flask import Flask, render_template, request, jsonify
import requests
import pickle
import numpy as np
import sklearn 
from sklearn.preprocessing import StandardScaler
import flasgger 
from flasgger import Swagger

app = Flask(__name__)

pickle_in = open('random_forest_regression_model.pkl','rb')
classifier = pickle.load(pickle_in)

@app.route('/',methods=['GET'])
def Home():
    return render_template('homepage.html')

standard_to = StandardScaler()
@app.route('/predict',methods=['POST'])
def predict_car_price():
    fuel_diesel = 0
    if request.method == 'POST':
        #Obtaining User Inputs
        
        year = int(request.form['year'])
        #Current year is 2021
        year = 2021 - year
        
        Present_Price = float(request.form['Present_Price'])
        Kms_Driven = np.log(int(request.form['Kms_Driven']))
        Owner = int(request.form['Owner'])
        
        fuel_petrol = request.form['fuel_petrol']
        if(fuel_petrol == 'fuel_petrol'):
            fuel_petrol = 1
            fuel_diesel = 0
        else:
            fuel_petrol = 0
            fuel_diesel = 1
            
        Seller_Type_Individual = request.form['Seller_Type_Individual']
        if(Seller_Type_Individual == 'Individual'):
            Seller_Type_Individual = 1
        else:
            Seller_Type_Individual = 0	
            
        Transmission_Mannual = request.form['Transmission_Mannual']
        if(Transmission_Mannual == 'Mannual'):
            Transmission_Mannual = 1
        else:
            Transmission_Mannual = 0
            
        #Prediction
        prediction = classifier.predict([[Present_Price, Kms_Driven, Owner, year, fuel_diesel, fuel_petrol, Seller_Type_Individual, Transmission_Mannual]])
        output = round(prediction[0],2)
        if (output < 0):
            return render_template('homepage.html',prediction_text = "Sorry, this Car cannot be sold")
        else:
            return render_template('homepage.html',prediction_text= "Estimated Selling Price is Rs {} Lakhs".format(output))
    else:
        return render_template('homepage.html')

if __name__ == '__main__':
    app.run(debug = 'True')

