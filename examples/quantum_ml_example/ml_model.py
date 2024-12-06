# ml_model.py

import numpy as np
from qiskit import QuantumCircuit, Aer, transpile, assemble, execute
from qiskit_machine_learning.algorithms import QSVC
from qiskit_machine_learning.datasets import breast_cancer

# Load dataset
data, labels = breast_cancer(training_size=20, test_size=10, plot_data=True)

# Create a quantum support vector classifier
qsvc = QSVC(quantum_kernel=True)

# Train the model
qsvc.fit(data, labels)

# Test the model
accuracy = qsvc.score(data, labels)
print(f"Model accuracy: {accuracy:.2f}")

# Make predictions
predictions = qsvc.predict(data)
print("Predictions:", predictions)
