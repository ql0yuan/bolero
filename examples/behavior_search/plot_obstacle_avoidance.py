"""
==================
Obstacle Avoidance
==================

We use CMA-ES to optimize a DMP so that it avoids point obstacles.
"""
print(__doc__)

import numpy as np
import matplotlib.pyplot as plt
from bolero.environment import OptimumTrajectory
from bolero.behavior_search import BlackBoxSearch
from bolero.optimizer import CMAESOptimizer
from bolero.representation import DMPBehavior
from bolero.controller import Controller
from dmp import DMP


n_task_dims = 2
obstacles = [np.array([0.5, 0.5]), np.array([0.6, 0.8]), np.array([0.8, 0.6])]
x0 = np.zeros(n_task_dims)
g = np.ones(n_task_dims)
execution_time = 1.0
dt = 0.01
n_features = 10
n_episodes = 500


beh = DMPBehavior(DMP(execution_time, dt, n_features))
env = OptimumTrajectory(x0, g, execution_time, dt, obstacles,
                        penalty_goal_dist=1.0, penalty_obstacle=1000.0,
                        penalty_acc=1.0)
opt = CMAESOptimizer(variance=100.0 ** 2, random_state=0)
bs = BlackBoxSearch(beh, opt)
controller = Controller(environment=env, behavior_search=bs,
                        n_episodes=n_episodes, record_trajectories=True)

rewards = controller.learn(["x0", "g"], [x0, g])
controller.episode_with(bs.get_best_behavior(), ["x0", "g"], [x0, g])
X = np.asarray(controller.trajectories_[-1])
X_hist = np.asarray(controller.trajectories_)

plt.figure()
ax = plt.subplot(121)
ax.set_title("Optimization progress")
ax.plot(rewards)
ax.set_xlabel("Episode")
ax.set_ylabel("Reward")

ax = plt.subplot(122, aspect="equal")
ax.set_title("Learned trajectory ($x_1$, $x_2$)")
env.plot(ax)
ax.plot(X[:, 0], X[:, 1], lw=5, label="Final trajectory")
for it, X in enumerate(X_hist[::n_episodes / 10]):
    ax.plot(X[:, 0], X[:, 1], c="k", alpha=it / 10.0, lw=3, ls="--")
plt.legend(loc="best")
plt.show()
