from django.shortcuts import render
import pandas as pd
import json

def index(request):
    # Read the CSV file
    df = pd.read_csv(r'C:\Users\Hp\OneDrive\Desktop\00-coding\ev_charging_data2.csv')
    
    # Prepare data for JSON
    data = {
        'time': df['Time Elapsed_s'].tolist(),
        'current': df['Charging Current_A'].tolist(),
        'voltage': df['Charging Voltage_V'].tolist(),
        'power': (df['Charging Power_kW'] * 1000).tolist(),  # Convert to Watts
        'temperature': df['Battery Temperature_C'].tolist()
    }
    
    # Convert to JSON for JavaScript
    chart_data = json.dumps(data)
    
    return render(request, 'visualization/index.html', {'chart_data': chart_data})