from django.shortcuts import render
from .forms import PredictionForm
import joblib
import pandas as pd
from datetime import datetime
import os

# Load the model and scaler
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model = joblib.load(os.path.join(BASE_DIR, 'model', 'model.joblib'))
scaler = joblib.load(os.path.join(BASE_DIR, 'model', 'scaler.joblib'))

def predict_view(request):
    predictions = []
    forms = []
    total_power = 100  # Main DC power in kW
    remaining_power = total_power

    if request.method == 'POST':
        valid_forms = []
        for i in range(3):  # Handle 3 forms
            form = PredictionForm(request.POST, prefix=f'form{i}')
            forms.append(form)
            if form.is_valid():
                valid_forms.append(form)

        # Process valid forms
        for form in valid_forms:
            charging_power = min(form.cleaned_data['charging_power'], remaining_power)
            battery_temp = form.cleaned_data['battery_temp']
            soc = form.cleaned_data['soc']
            duration = form.cleaned_data['duration']
            timestamp = form.cleaned_data['timestamp']

            # Create features DataFrame
            features = pd.DataFrame({
                'Charging Power_kW': [charging_power],
                'Battery Temperature_C': [battery_temp],
                'State Of Charge_SoC': [soc],
                'Charging_Duration_h': [duration],
                'hour': [timestamp.hour],
                'day_of_week': [timestamp.weekday()],
                'month': [timestamp.month],
                'is_weekend': [1 if timestamp.weekday() in [5, 6] else 0]
            })

            # Scale features and make prediction
            features_scaled = scaler.transform(features)
            prediction = model.predict(features_scaled)[0]
            
            predictions.append({
                'charging_power': charging_power,
                'battery_temp': battery_temp,
                'soc': soc,
                'duration': duration,
                'timestamp': timestamp,
                'predicted_value': prediction,
                'power_allocation': charging_power
            })
            
            remaining_power -= charging_power

    else:
        # Create 3 empty forms
        for i in range(3):
            forms.append(PredictionForm(prefix=f'form{i}'))

    return render(request, 'prediction/predict.html', {
        'forms': forms,
        'predictions': predictions,
        'total_power': total_power,
        'remaining_power': remaining_power if predictions else total_power
    })