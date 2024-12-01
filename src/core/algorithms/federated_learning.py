import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split

class FederatedLearning:
    def __init__(self, num_clients=5, epochs=1, batch_size=32):
        self.num_clients = num_clients
        self.epochs = epochs
        self.batch_size = batch_size
        self.global_model = self.create_model()

    def create_model(self):
        """Create a simple neural network model."""
        model = keras.Sequential([
            layers.Flatten(input_shape=(28, 28)),
            layers.Dense(128, activation='relu'),
            layers.Dense(10, activation='softmax')
        ])
        model.compile(optimizer='adam',
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])
        return model

    def load_data(self):
        """Load the MNIST dataset and split it into clients."""
        (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
        x_train = x_train.astype('float32') / 255.0  # Normalize the data
        x_test = x_test.astype('float32') / 255.0

        # Split the data among clients
        client_data = np.array_split(x_train, self.num_clients)
        client_labels = np.array_split(y_train, self.num_clients)

        return client_data, client_labels, x_test, y_test

    def train_on_client(self, client_data, client_labels):
        """Train the model on a single client's data."""
        model = self.create_model()
        model.fit(client_data, client_labels, epochs=self.epochs, batch_size=self.batch_size, verbose=0)
        return model.get_weights()

    def aggregate_weights(self, client_weights):
        """Aggregate weights from all clients."""
        new_weights = [np.zeros_like(weight) for weight in client_weights[0]]
        for weights in client_weights:
            for i in range(len(new_weights)):
                new_weights[i] += weights[i] / self.num_clients
        return new_weights

    def federated_training(self):
        """Perform federated training across all clients."""
        client_data, client_labels, x_test, y_test = self.load_data()
        for round in range(1, 6):  # Simulate 5 rounds of training
            print(f"Round {round}")
            client_weights = []
            for i in range(self.num_clients):
                print(f"Training on client {i + 1}")
                weights = self.train_on_client(client_data[i], client_labels[i])
                client_weights.append(weights)

            # Aggregate weights
            self.global_model.set_weights(self.aggregate_weights(client_weights))

            # Evaluate the global model
            loss, accuracy = self.global_model.evaluate(x_test, y_test, verbose=0)
            print(f"Global model accuracy after round {round}: {accuracy * 100:.2f}%")

if __name__ == "__main__":
    # Example usage of the FederatedLearning class
    federated_learning = FederatedLearning(num_clients=5, epochs=1, batch_size=32)
    federated_learning.federated_training()
