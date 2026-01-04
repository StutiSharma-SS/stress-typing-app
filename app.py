from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import numpy as np
from model import StressPredictor

app = Flask(__name__)
CORS(app)

# Initialize the ML model
predictor = StressPredictor()

@app.route('/')
def home():
    """Serve the main HTML page"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict_stress():
    """
    API endpoint to predict stress level based on typing behavior
    Expected JSON input:
    {
        "typing_speed": float,  # keys per second
        "avg_pause": float,     # average pause in milliseconds
        "error_rate": float     # backspaces per total keys
    }
    """
    try:
        data = request.get_json()
        
        # Extract features
        typing_speed = data.get('typing_speed', 0)
        avg_pause = data.get('avg_pause', 0)
        error_rate = data.get('error_rate', 0)
        
        # Validate input
        if typing_speed < 0 or avg_pause < 0 or error_rate < 0:
            return jsonify({'error': 'Invalid input values'}), 400
        
        # Make prediction
        stress_level, confidence = predictor.predict(
            typing_speed, avg_pause, error_rate
        )
        
        # Get stress management tips
        tips = get_stress_tips(stress_level)
        
        response = {
            'stress_level': stress_level,
            'confidence': round(confidence * 100, 2),
            'tips': tips,
            'features': {
                'typing_speed': round(typing_speed, 2),
                'avg_pause': round(avg_pause, 2),
                'error_rate': round(error_rate * 100, 2)
            }
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_stress_tips(stress_level):
    """Return stress management tips based on predicted level"""
    tips = {
        'Low': [
            '✓ Great job! Your typing pattern shows minimal stress.',
            '✓ Keep maintaining healthy work habits.',
            '✓ Continue taking regular breaks.'
        ],
        'Medium': [
            '⚠ Moderate stress detected. Consider taking a short break.',
            '⚠ Practice deep breathing exercises for 2-3 minutes.',
            '⚠ Stretch your hands and shoulders to release tension.'
        ],
        'High': [
            '⚠️ High stress levels detected. Time for a break!',
            '⚠️ Step away from the screen for 10-15 minutes.',
            '⚠️ Try meditation or go for a short walk.',
            '⚠️ Consider talking to someone if stress persists.'
        ]
    }
    return tips.get(stress_level, [])

if __name__ == '__main__':
    print("🚀 Starting Stress Prediction Server...")
    print("📊 ML Model loaded successfully!")
    print("🌐 Open http://localhost:5000 in your browser")
    app.run(debug=True, port=5000)