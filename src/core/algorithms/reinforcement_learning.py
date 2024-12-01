import numpy as np
import gym
import matplotlib.pyplot as plt

class QLearningAgent:
    def __init__(self, env, learning_rate=0.1, discount_factor=0.99, exploration_rate=1.0, exploration_decay=0.995, min_exploration_rate=0.01):
        self.env = env
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay
        self.min_exploration_rate = min_exploration_rate
        self.q_table = np.zeros((env.observation_space.n, env.action_space.n))

    def choose_action(self, state):
        """Choose an action using an epsilon-greedy policy."""
        if np.random.rand() < self.exploration_rate:
            return self.env.action_space.sample()  # Explore
        else:
            return np.argmax(self.q_table[state])  # Exploit

    def update_q_table(self, state, action, reward, next_state):
        """Update the Q-table using the Q-learning formula."""
        best_next_action = np.argmax(self.q_table[next_state])
        td_target = reward + self.discount_factor * self.q_table[next_state][best_next_action]
        td_delta = td_target - self.q_table[state][action]
        self.q_table[state][action] += self.learning_rate * td_delta

    def train(self, num_episodes):
        """Train the agent over a number of episodes."""
        rewards = []
        for episode in range(num_episodes):
            state = self.env.reset()
            total_reward = 0
            done = False
            
            while not done:
                action = self.choose_action(state)
                next_state, reward, done, _ = self.env.step(action)
                self.update_q_table(state, action, reward, next_state)
                state = next_state
                total_reward += reward
            
            rewards.append(total_reward)
            self.exploration_rate = max(self.min_exploration_rate, self.exploration_rate * self.exploration_decay)
        
        return rewards

    def plot_rewards(self, rewards):
        """Plot the rewards over episodes."""
        plt.plot(rewards)
        plt.title("Rewards over Episodes")
        plt.xlabel("Episode")
        plt.ylabel("Total Reward")
        plt.show()

if __name__ == "__main__":
    # Create the Frozen Lake environment
    env = gym.make("FrozenLake-v1", is_slippery=False)  # Set is_slippery=True for a stochastic environment

    # Initialize the Q-learning agent
    agent = QLearningAgent(env)

    # Train the agent
    num_episodes = 1000
    rewards = agent.train(num_episodes)

    # Plot the rewards
    agent.plot_rewards(rewards)

    # Close the environment
    env.close()
