import gymnasium as gym
import numpy as np
import f110_gym
from f110_planning.tracking import PurePursuitPlanner
from f110_planning.utils import load_waypoints

# 1. Create the environment
env = gym.make('f110-v0', 
               map='data/maps/F1/Oschersleben/Oschersleben_map', 
               render_mode='human', 
               num_agents=1)

# 2. Load waypoints using the utility function
waypoints = load_waypoints('data/maps/F1/Oschersleben/Oschersleben_centerline.tsv')

# 3. Initialize the planner
planner = PurePursuitPlanner(waypoints=waypoints)

# 4. Reset and run the simulation loop
obs, info = env.reset(options={'poses': np.array([[0.0, 0.0, 2.85]])})
done = False

while not done:
    # Plan next action
    action = planner.plan(obs)
    
    # Step the environment
    obs, reward, terminated, truncated, info = env.step(np.array([[action.steer, action.speed]]))
    done = terminated or truncated
    
    env.render()