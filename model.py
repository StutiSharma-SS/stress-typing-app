import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

class StressPredictor:
    """
    Machine Learning model to predict stress levels based on typing behavior
    Uses Random Forest Classifier trained on synthetic data
    """
    
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.train_model()
    
    def generate_synthetic_data(self, n_samples=1000):
        """
        Generate synthetic training data based on typical typing patterns
        
        Features:
        - typing_speed: keys per second (0.5 to 5.0)
        - avg_pause: average pause duration in ms (50 to 2000)
        - error_rate: backspaces per total keys (0.0 to 0.5)
        
        Stress Patterns:
        - Low Stress: Fast typing, short pauses, few errors
        - Medium Stress: Moderate speed, moderate pauses, some errors
        - High Stress: Slow/erratic typing, long pauses, many errors
        """
        np.random.seed(42)
        
        X = []
        y = []
        
        # Generate Low Stress samples (label: 0)
        for _ in range(n_samples // 3):
            typing_speed = np.random.uniform(3.0, 5.0)  # Fast typing
            avg_pause = np.random.uniform(50, 300)      # Short pauses
            error_rate = np.random.uniform(0.0, 0.1)    # Few errors
            X.append([typing_speed, avg_pause, error_rate])
            y.append(0)
        
        # Generate Medium Stress samples (label: 1)
        for _ in range(n_samples // 3):
            typing_speed = np.random.uniform(1.5, 3.5)  # Moderate speed
            avg_pause = np.random.uniform(250, 800)     # Moderate pauses
            error_rate = np.random.uniform(0.08, 0.25)  # Some errors
            X.append([typing_speed, avg_pause, error_rate])
            y.append(1)
        
        # Generate High Stress samples (label: 2)
        for _ in range(n_samples // 3):
            typing_speed = np.random.uniform(0.5, 2.0)  # Slow typing
            avg_pause = np.random.uniform(600, 2000)    # Long pauses
            error_rate = np.random.uniform(0.2, 0.5)    # Many errors
            X.append([typing_speed, avg_pause, error_rate])
            y.append(2)
        
        return np.array(X), np.array(y)
    
    def train_model(self):
        """Train the Random Forest model on synthetic data"""
        X, y = self.generate_synthetic_data()
        
        # Normalize features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train model
        self.model.fit(X_scaled, y)
        
        # Calculate training accuracy
        train_accuracy = self.model.score(X_scaled, y)
        print(f"✓ Model trained with {train_accuracy*100:.2f}% accuracy")
    
    def predict(self, typing_speed, avg_pause, error_rate):
        """
        Predict stress level from typing features
        
        Args:
            typing_speed: Keys per second
            avg_pause: Average pause duration in milliseconds
            error_rate: Ratio of backspaces to total keys
        
        Returns:
            stress_level: 'Low', 'Medium', or 'High'
            confidence: Probability of the prediction (0-1)
        """
        # Prepare features
        features = np.array([[typing_speed, avg_pause, error_rate]])
        features_scaled = self.scaler.transform(features)
        
        # Make prediction
        prediction = self.model.predict(features_scaled)[0]
        probabilities = self.model.predict_proba(features_scaled)[0]
        confidence = probabilities[prediction]
        
        # Map to stress levels
        stress_labels = {0: 'Low', 1: 'Medium', 2: 'High'}
        stress_level = stress_labels[prediction]
        
        return stress_level, confidence

# Test the model when run directly
if __name__ == "__main__":
    predictor = StressPredictor()
    
    # Test cases
    test_cases = [
        (4.5, 100, 0.05, "Low stress (fast, few pauses, no errors)"),
        (2.5, 500, 0.15, "Medium stress (moderate speed and errors)"),
        (1.0, 1200, 0.35, "High stress (slow, long pauses, many errors)")
    ]
    
    print("\n🧪 Testing model predictions:")
    for speed, pause, error, description in test_cases:
        level, conf = predictor.predict(speed, pause, error)
        print(f"\n{description}")
        print(f"  Input: speed={speed}, pause={pause}ms, error={error}")
        print(f"  → Predicted: {level} stress ({conf*100:.1f}% confidence)")