import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

class GAN:
    def __init__(self, latent_dim=100):
        self.latent_dim = latent_dim
        self.generator = self.build_generator()
        self.discriminator = self.build_discriminator()
        self.gan = self.build_gan()

    def build_generator(self):
        """Build the generator model."""
        model = keras.Sequential([
            layers.Dense(256, activation='relu', input_dim=self.latent_dim),
            layers.BatchNormalization(),
            layers.Dense(512, activation='relu'),
            layers.BatchNormalization(),
            layers.Dense(1024, activation='relu'),
            layers.BatchNormalization(),
            layers.Dense(28 * 28, activation='tanh'),
            layers.Reshape((28, 28, 1))
        ])
        return model

    def build_discriminator(self):
        """Build the discriminator model."""
        model = keras.Sequential([
            layers.Flatten(input_shape=(28, 28, 1)),
            layers.Dense(512, activation='relu'),
            layers.Dense(256, activation='relu'),
            layers.Dense(1, activation='sigmoid')
        ])
        return model

    def build_gan(self):
        """Build the GAN model."""
        self.discriminator.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        self.discriminator.trainable = False  # Freeze the discriminator when training the GAN
        gan_input = layers.Input(shape=(self.latent_dim,))
        generated_image = self.generator(gan_input)
        gan_output = self.discriminator(generated_image)
        model = keras.Model(gan_input, gan_output)
        model.compile(loss='binary_crossentropy', optimizer='adam')
        return model

    def train(self, x_train, epochs=10000, batch_size=128, sample_interval=1000):
        """Train the GAN."""
        # Normalize the data to [-1, 1]
        x_train = (x_train.astype(np.float32) - 127.5) / 127.5

        # Create labels for real and fake images
        real_labels = np.ones((batch_size, 1))
        fake_labels = np.zeros((batch_size, 1))

        for epoch in range(epochs):
            # Train the discriminator
            idx = np.random.randint(0, x_train.shape[0], batch_size)
            real_images = x_train[idx]

            noise = np.random.normal(0, 1, (batch_size, self.latent_dim))
            generated_images = self.generator.predict(noise)

            d_loss_real = self.discriminator.train_on_batch(real_images, real_labels)
            d_loss_fake = self.discriminator.train_on_batch(generated_images, fake_labels)
            d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)

            # Train the generator
            noise = np.random.normal(0, 1, (batch_size, self.latent_dim))
            g_loss = self.gan.train_on_batch(noise, real_labels)

            # Print the progress
            if epoch % sample_interval == 0:
                print(f"{epoch} [D loss: {d_loss[0]:.4f}, acc.: {100 * d_loss[1]:.2f}%] [G loss: {g_loss:.4f}]")
                self.sample_images(epoch)

    def sample_images(self, epoch, examples=10, dim=(1, 10), figsize=(10, 1)):
        """Generate and save images from the generator."""
        noise = np.random.normal(0, 1, (examples, self.latent_dim))
        generated_images = self.generator.predict(noise)
        generated_images = 0.5 * generated_images + 0.5  # Rescale to [0, 1]

        plt.figure(figsize=figsize)
        for i in range(examples):
            plt.subplot(dim[0], dim[1], i + 1)
            plt.imshow(generated_images[i, :, :, 0], cmap='gray')
            plt.axis('off')
        plt.tight_layout()
        plt.savefig(f"gan_generated_epoch_{epoch}.png")
        plt.close()

if __name__ == "__main__":
    # Load the MNIST dataset
    (x_train, _), (_, _) = keras.datasets.mnist.load_data()
    x_train = np.expand_dims(x_train, axis=-1)  # Add channel dimension
