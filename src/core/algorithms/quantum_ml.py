import numpy as np
from qiskit import QuantumCircuit, Aer, execute
from qiskit.circuit import Parameter
from qiskit.aer import AerSimulator
from qiskit_machine_learning.algorithms import QSVC
from qiskit_machine_learning.datasets import breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

class QuantumMachineLearning:
    def __init__(self):
        self.backend = Aer.get_backend('aer_simulator')
        self.qsvc = None

    def load_data(self):
        """Load the breast cancer dataset."""
        data, labels = breast_cancer(training_size=20, test_size=10, plot_data=False)
        return data, labels

    def preprocess_data(self, data, labels):
        """Preprocess the data by splitting into training and testing sets."""
        X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)
        return X_train, X_test, y_train, y_test

    def train_qsvm(self, X_train, y_train):
        """Train a Quantum Support Vector Machine (QSVM)."""
        self.qsvc = QSVC(quantum_kernel=self.create_quantum_kernel())
        self.qsvc.fit(X_train, y_train)

    def create_quantum_kernel(self):
        """Create a quantum kernel for the QSVM."""
        def quantum_kernel(x1, x2):
            """Custom quantum kernel function."""
            circuit = QuantumCircuit(2)
            circuit.h(0)
            circuit.h(1)
            circuit.cx(0, 1)
            circuit.measure_all()

            # Execute the circuit
            job = execute(circuit, self.backend, shots=1024)
            result = job.result()
            counts = result.get_counts(circuit)
            return counts

        return quantum_kernel

    def predict(self, X_test):
        """Make predictions using the trained QSVM."""
        return self.qsvc.predict(X_test)

    def evaluate(self, y_test, y_pred):
        """Evaluate the model's performance."""
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy * 100:.2f}%")
        return accuracy

    def plot_results(self, y_test, y_pred):
        """Plot the results of the predictions."""
        plt.figure(figsize=(10, 6))
        plt.scatter(range(len(y_test)), y_test, color='blue', label='True Labels', alpha=0.6)
        plt.scatter(range(len(y_pred)), y_pred, color='red', label='Predicted Labels', alpha=0.6)
        plt.title('True vs Predicted Labels')
        plt.xlabel('Sample Index')
        plt.ylabel('Label')
        plt.legend()
        plt.show()

if __name__ == "__main__":
    # Example usage of the QuantumMachineLearning class
    qml = QuantumMachineLearning()
    
    # Load and preprocess data
    data, labels = qml.load_data()
    X_train, X_test, y_train, y_test = qml.preprocess_data(data, labels)

    # Train the QSVM
    qml.train_qsvm(X_train, y_train)

    # Make predictions
    y_pred = qml.predict(X_test)

    # Evaluate the model
    qml.evaluate(y_test, y_pred)

    # Plot results
    qml.plot_results(y_test, y_pred)
