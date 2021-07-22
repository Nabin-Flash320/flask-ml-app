
from logging import debug
from types import MethodType
from flask import Flask, render_template, request
import pickle


model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def pred():
    petrol = 0
    diesel = 0
    individual = 0
    manual = 0
    if request.method == 'POST':
        year = 2020 - int(request.form['year'])
        present_price = float(request.form['price'])
        total_distance = int(request.form['distance'])
        number_of_owners = int(request.form['owner'])
        fuel_type = request.form['fuel']
        role = request.form['role']
        transmission_type = request.form['transmission']

        if fuel_type == 'Petrol':
            petrol = 1
            diesel = 0
        elif fuel_type == 'Diesel': 
            diesel = 1
            petrol = 0
        else:
            diesel = 0
            petrol = 0

        if role == 'Individaul':
            individual = 1
        else:
            individual = 0
        
        if transmission_type == 'Manual':
            manual = 1
        else:
            manual = 0
        
        prd = model.predict([[
            present_price, total_distance, number_of_owners, year, diesel, petrol,
            individual, manual 
        ]])

        output = round(prd[0], 2)
        if output < 0:
            return render_template('index.html',prediction_text="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="You Can Sell The Car at {}".format(output))
    
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)