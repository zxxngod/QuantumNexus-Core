import os
import json
import logging
import requests
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta
from typing import List, Dict, Any
from kafka import KafkaConsumer, KafkaProducer
import threading
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ThreatIntelligence:
    def __init__(self, api_key: str, data_source: str, kafka_topic: str):
        self.api_key = api_key
        self.data_source = data_source
        self.kafka_topic = kafka_topic
        self.model = IsolationForest(contamination=0.01)  # 1% expected anomalies
        self.scaler = StandardScaler()
        self.threat_data = pd.DataFrame()
        self.consumer = KafkaConsumer(self.kafka_topic, bootstrap_servers='localhost:9092', auto_offset_reset='earliest')
        self.producer = KafkaProducer(bootstrap_servers='localhost:9092')

    def fetch_threat_data(self) -> None:
        """Fetch threat intelligence data from an external API."""
        try:
            response = requests.get(self.data_source, headers={'Authorization': f'Bearer {self.api_key}'})
            response.raise_for_status()
            self.threat_data = pd.DataFrame(response.json())
            logging.info("Threat data fetched successfully.")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching threat data: {e}")

    def preprocess_data(self) -> None:
        """Preprocess the threat data for anomaly detection."""
        if self.threat_data.empty:
            logging.warning("No threat data to preprocess.")
            return

        # Example preprocessing steps
        self.threat_data['timestamp'] = pd.to_datetime(self.threat_data['timestamp'])
        self.threat_data.set_index('timestamp', inplace=True)
        self.threat_data = self.threat_data.resample('1H').mean().fillna(0)  # Resample to hourly data
        self.threat_data_scaled = self.scaler.fit_transform(self.threat_data)

    def detect_anomalies(self) -> List[Dict[str, Any]]:
        """Detect anomalies in the threat data using Isolation Forest."""
        if self.threat_data_scaled is None:
            logging.warning("No scaled threat data available for anomaly detection.")
            return []

        anomalies = self.model.fit_predict(self.threat_data_scaled)
        anomaly_indices = np.where(anomalies == -1)[0]
        detected_anomalies = self.threat_data.iloc[anomaly_indices].to_dict(orient='records')
        logging.info(f"Detected {len(detected_anomalies)} anomalies.")
        return detected_anomalies

    def enrich_threat_data(self, anomalies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Enrich detected anomalies with additional threat intelligence."""
        enriched_data = []
        for anomaly in anomalies:
            # Example enrichment: Add threat score from an external service
            threat_score = self.get_threat_score(anomaly['ip_address'])
            anomaly['threat_score'] = threat_score
            enriched_data.append(anomaly)
        return enriched_data

    def get_threat_score(self, ip_address: str) -> float:
        """Get threat score for a given IP address from an external threat intelligence API."""
        try:
            response = requests.get(f"https://api.threatscore.com/{ip_address}", headers={'Authorization': f'Bearer {self.api_key}'})
            response.raise_for_status()
            return response.json().get('threat_score', 0.0)
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching threat score for {ip_address}: {e}")
            return 0.0

    def automate_response(self, enriched_anomalies: List[Dict[str, Any]]) -> None:
        """Automate response actions based on detected anomalies."""
        for anomaly in enriched_anomalies:
            if anomaly['threat_score'] > 75:  # Threshold for high threat
                self.block_ip(anomaly['ip_address'])
                self.send_alert_to_siem(anomaly)
                logging.info(f"Blocked IP: {anomaly['ip_address']} due to high threat score.")

    def block_ip(self, ip_address: str) -> None:
        """Block an IP address (placeholder for actual blocking logic)."""
        logging.info(f"Blocking IP address: {ip_address}")
        # Here you would implement the actual blocking logic, e.g., updating firewall rules.

    def send_alert_to_siem(self, anomaly: Dict[str, Any]) -> None:
        """Send an alert to a SIEM system."""
        alert_message = json.dumps(anomaly)
        self.producer.send('siem_alerts', value=alert_message.encode('utf-8'))
        logging.info(f"Sent alert to SIEM for IP: {anomaly['ip_address']}")

    def run(self) -> None:
        """Run the threat intelligence pipeline."""
        self.fetch_threat_data()
        self.preprocess_data()
        anomalies = self.detect_anomalies()
        if anomalies:
            enriched_anomalies = self.enrich_threat_data(anomalies)
            self.automate_response(enriched_anomalies)

    def start_data_streaming(self) -> None:
        """Start consuming real-time threat data from Kafka."""
        for message in self.consumer:
            threat_data = json.loads(message.value.decode('utf-8'))
            self.threat_data = self.threat_data.append(threat_data, ignore_index=True)
            logging.info("Received real-time threat data from Kafka.")
            self.preprocess_data()
            anomalies = self.detect_anomalies()
            if anomalies:
                enriched_anomalies = self.enrich_threat_data(anomalies)
                self.automate_response(enriched_anomalies)

    def retrain_model(self) -> None:
        """Periodically retrain the anomaly detection model."""
        while True:
            time.sleep(3600)  # Retrain every hour
            if not self.threat_data.empty:
                self.model.fit(self.scaler.fit_transform(self.threat_data))
                logging.info("Model retrained with new threat data.")

if __name__ == "__main__":
    # Example usage
    API_KEY = "your_api_key_here"
    DATA_SOURCE = "https://api.threatdata.com/threats"
    KAFKA_TOPIC = "threat_data"

    threat_intelligence = ThreatIntelligence(api_key=API_KEY, data_source=DATA_SOURCE, kafka_topic=KAFKA_TOPIC)
    
    # Start the data streaming in a separate thread
    threading.Thread(target=threat_intelligence.start_data_streaming, daemon=True).start()
    
    # Start the model retraining in a separate thread
    threading.Thread(target=threat_intelligence.retrain_model, daemon=True).start()
    
    # Run the initial threat intelligence pipeline
    threat_intelligence.run()
