from flask import Flask, render_template, request, jsonify
from sklearn.preprocessing import StandardScaler
import pandas as pd
import pickle

app = Flask(__name__)

# Load the trained model, scaler, and encoder
with open('models/linear_regression.pkl', 'rb') as model_file:
    model = pickle.load(model_file)
with open('models/scaler.pkl', 'rb') as file:
    scaler = pickle.load(file)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods = ['POST'])
def predict():
        
        designation = int(request.form['designation'])
        resource_allocation = float(request.form['resource_allocation'])
        mental_fatigue_score = float(request.form['mental_fatigue_score'])
        company_type = request.form['company_type']
        wfh_setup_available = request.form['wfh_setup_available']
        gender = request.form['gender']
        
        input_data = pd.DataFrame({'Designation':[designation],
                                   'Resource Allocation':[resource_allocation],
                                   'Mental Fatigue Score':[mental_fatigue_score],
                                   'Company Type_Service' : [company_type],
                                   'WFH Setup Available_Yes': [wfh_setup_available],
                                   'Gender_Male':[gender]})
        #converting the categorical values into binary
        input_data['Company Type_Service'] = 1 if input_data.at[0, 'Company Type_Service'] == 'Service' else 0
        input_data['WFH Setup Available_Yes'] = 1 if input_data.at[0, 'WFH Setup Available_Yes'] == 'Yes' else 0
        input_data['Gender_Male'] = 1 if input_data.at[0, 'Gender_Male'] == 'Male' else 0

        # Performing standard scaling on the input_data
        scaled_data = scaler.transform(input_data)
        # Make a prediction using the model
        prediction = model.predict(scaled_data)[0]
        rounded_prediction = round(prediction, 2) 
        return render_template('index.html', prediction=rounded_prediction)


if __name__ == "__main__":
    app.run(debug = True)