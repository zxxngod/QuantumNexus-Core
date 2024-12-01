import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from qiskit import QuantumCircuit, Aer, execute
from qiskit.circuit import Parameter
from qiskit.aer import AerSimulator
from qiskit_machine_learning.kernels import QuantumKernel

class HybridLearning:
    def __init__(self):
        self.backend = Aer.get_backend('aer_simulator')
        self.qkernel = None
        self.classifier = None

    def load_data(self):
        """Load the Iris dataset."""
        data = load_iris()
        X, y = data.data, data.target
        return X, y

    def preprocess_data(self, X, y):
        """Preprocess the data by splitting into training and testing sets."""
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        return X_train, X_test, y_train, y_test

    def create_quantum_kernel(self):
        """Create a quantum kernel for the hybrid model."""
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

    def train_hybrid_model(self, X_train, y_train):
        """Train a hybrid model using a classical SVM with a quantum kernel."""
        self.qkernel = QuantumKernel(quantum_instance=self.backend)
        self.qkernel.set_feature_map(self.create_quantum_kernel())
        
        # Transform the training data using the quantum kernel
        self.classifier = SVC(kernel=self.qkernel.evaluate(X_train, X_train))
        self.classifier.fit(X_train, y_train)

    def predict(self, X_test):
        """Make predictions using the trained hybrid model."""
        return self.classifier.predict(X_test)

    def evaluate(self, y_test, y_pred):
        """Evaluate the model's performance."""
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy * 100:.2f}%")
        return accuracy

if __name__ == "__main__":
    # Example usage of the HybridLearning class
    hybrid_model = HybridLearning()
    
    # Load and preprocess data
    X, y = hybrid_model.load_data()
    X_train, X_test, y_train, y_test = hybrid_model.preprocess_data(X, y)

    # Train the hybrid model
    hybrid_model.train_hybrid_model(X_train, y_train)

    # Make predictions
    y_pred = hybrid_model.predict(X_test)

    # Evaluate the model
    hybrid_model.evaluate(y_test, y_pred)
