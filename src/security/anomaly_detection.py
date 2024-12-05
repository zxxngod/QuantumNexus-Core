import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

class AnomalyDetection:
    def __init__(self, contamination=0.1):
        """
        Initialize the AnomalyDetection class.

        Parameters:
        - contamination: The proportion of outliers in the data set.
        """
        self.contamination = contamination
        self.model = IsolationForest(contamination=self.contamination, random_state=42)
        self.scaler = StandardScaler()

    def fit(self, data):
        """
        Fit the Isolation Forest model to the data.

        Parameters:
        - data: A pandas DataFrame containing the features for anomaly detection.
        """
        # Scale the data
        scaled_data = self.scaler.fit_transform(data)
        self.model.fit(scaled_data)

    def predict(self, data):
        """
        Predict anomalies in the data.

        Parameters:
        - data: A pandas DataFrame containing the features for prediction.

        Returns:
        - A numpy array with -1 for anomalies and 1 for normal observations.
        """
        scaled_data = self.scaler.transform(data)
        return self.model.predict(scaled_data)

    def detect_anomalies(self, data):
        """
        Detect anomalies in the data and return a DataFrame with results.

        Parameters:
        - data: A pandas DataFrame containing the features for anomaly detection.

        Returns:
        - A DataFrame with the original data and an additional column indicating anomalies.
        """
        predictions = self.predict(data)
        results = data.copy()
        results['Anomaly'] = predictions
        return results

    def visualize_anomalies(self, data, results):
        """
        Visualize the anomalies in the data.

        Parameters:
        - data: A pandas DataFrame containing the original features.
        - results: A DataFrame containing the results with anomaly predictions.
        """
        plt.figure(figsize=(10, 6))
        plt.scatter(data.iloc[:, 0], data.iloc[:, 1], c=results['Anomaly'], cmap='coolwarm', edgecolor='k', s=50)
        plt.title('Anomaly Detection using Isolation Forest')
        plt.xlabel('Feature 1')
        plt.ylabel('Feature 2')
        plt.colorbar(label='Anomaly (-1: Anomaly, 1: Normal)')
        plt.show()

if __name__ == "__main__":
    # Example usage
    # Generate synthetic data for demonstration
    np.random.seed(42)
    normal_data = np.random.normal(loc=0, scale=1, size=(100, 2))
    anomaly_data = np.random.uniform(low=-6, high=6, size=(10, 2))
    data = np.vstack((normal_data, anomaly_data))
    df = pd.DataFrame(data, columns=['Feature 1', 'Feature 2'])

    # Initialize and fit the anomaly detection model
    anomaly_detector = AnomalyDetection(contamination=0.1)
    anomaly_detector.fit(df)

    # Detect anomalies
    results = anomaly_detector.detect_anomalies(df)

    # Print results
    print(results)

    # Visualize anomalies
    anomaly_detector.visualize_anomalies(df, results)
