"""This is the main script of the pendulum 2D animation."""

import matplotlib.pyplot as plt
import matplotlib.animation as anim

import pendulum_2d_calc as calc
from pendulum_2d_calc import constants as c

# Generate the data
data = calc.gen_data()

#########################################
### Animation

fig, axs = plt.subplots()
ax_main = axs
ax_main.set_xlim(-c.L*1.5,c.L*1.5)
ax_main.set_ylim(-c.L*1.5,c.L*1.5)
ax_main.set_aspect('equal')
ax_main.set_xlabel('x')
ax_main.set_ylabel('y')

lines = {}
points = {}

for method, data_i   in data.items():
    lines[method] = ax_main.plot([],[],'-', color=data_i['color'], label=data_i['label'])[0]
    points[method] = ax_main.plot([],[],'o', color=data_i['color'])[0]

fix = ax_main.plot(c.r_fix[0],c.r_fix[1],'x', color='k')[0]

def animate(frame):
    t = frame

    for method, data_i in data.items():
        lines[method].set_data([c.r_fix[0],data_i['r'][0,t]], [c.r_fix[1],data_i['r'][1,t]])
        points[method].set_data([data_i['r'][0,t], data_i['r'][1,t]])
    return list(lines.values())+list(points.values())

animation = anim.FuncAnimation(fig, func=animate, frames=c.fps*c.t_max, interval=1000/c.fps, blit=True)

ax_main.legend()
plt.show()