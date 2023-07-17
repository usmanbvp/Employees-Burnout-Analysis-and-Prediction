from flask import Flask, render_template, request
import joblib
import pandas as pd
from sklearn.preprocessing import  StandardScaler

app = Flask(__name__)

# Load the pre-trained model
with open('model.pkl', 'rb') as f:
    model= joblib.load(f)

# Load the label encoders
with open('encoder.pkl', 'rb') as f:
    label_encoders = joblib.load(f)

# Load the standard scaler
with open('scaler.pkl', 'rb') as f:
    scaler = joblib.load(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get the input values from the form
    international_plan = request.form['international_plan']
    voice_mail_plan = request.form['voice_mail_plan']
    account_length = int(request.form['account_length'])
    number_vmail_messages = float(request.form['number_vmail_messages'])
    total_day_minutes = float(request.form['total_day_minutes'])
    total_day_calls = float(request.form['total_day_calls'])
    total_eve_minutes = float(request.form['total_eve_minutes'])
    total_eve_calls = float(request.form['total_eve_calls'])
    total_night_minutes = float(request.form['total_night_minutes'])
    total_night_calls = float(request.form['total_night_calls'])
    total_intl_minutes = float(request.form['total_intl_minutes'])
    total_intl_calls = float(request.form['total_intl_calls'])
    customer_service_calls = float(request.form['customer_service_calls'])
    
    # Perform label encoding on the categorical columns
    label_encoder = LabelEncoder()
    international_plan = label_encoder.fit_transform([international_plan])[0]
    voice_mail_plan = label_encoder.fit_transform([voice_mail_plan])[0]
    
    # Create a DataFrame with the input values
    input_df = pd.DataFrame({
        'Designation': [international_plan],
        'Resource Allocation': [voice_mail_plan],
        'Mental Fatigue Score': [account_length],
        'Company Type_Service': [number_vmail_messages],
        'WFH Setup Available_Yes': [total_day_minutes],
        'Gender_Male': [total_day_calls],
    })

    # Perform scaling on the numerical columns
    numerical_cols = ['Account length', 'Number vmail messages', 'Total day minutes', 'Total day calls',
                      'Total eve minutes', 'Total eve calls', 'Total night minutes', 'Total night calls',
                      'Total intl minutes', 'Total intl calls', 'Customer service calls']
    input_df[numerical_cols] = scaler.transform(input_df[numerical_cols])

    # Make predictions using the pre-trained model
    churn_prediction = model_random.predict(input_df)
    print(churn_prediction)

    
    return render_template('index.html', prediction=churn_prediction[0])


if __name__ == '__main__':
    app.run(debug=True)
