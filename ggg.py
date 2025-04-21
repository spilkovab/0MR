import gymnasium as gym
from stable_baselines3 import PPO

# create environment
env_train = gym.make("LunarLander-v3")
model = PPO("MlpPolicy", env=env_train, device='cpu')
# reset environment to random state
model.learn(total_timesteps=10000)
model.save("ppo_lunarlander")


while True:
    # random action in action space
    action = env_train.action_space.sample()
    observation, reward, terminated, truncated, info = env_train.step(action)
    # env.render()

    if terminated or truncated:
        env_train.reset()