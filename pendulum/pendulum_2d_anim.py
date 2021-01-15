"""This is the main script of the pendulum 2D animation."""

import matplotlib.pyplot as plt
import matplotlib.animation as anim

import pendulum_2d_calc as calc
from pendulum_2d_calc import constants as c

# Generate the data
data = calc.gen_data()
r_approx = data["approx"]["r"]
r_exact = data["exact"]["r"]

#########################################
### Animation

fig, axs = plt.subplots()
ax_main = axs
ax_main.set_xlim(-c.L*1.5,c.L*1.5)
ax_main.set_ylim(-c.L*1.5,c.L*1.5)
ax_main.set_aspect('equal')
ax_main.set_xlabel('x')
ax_main.set_ylabel('y')

fix = ax_main.plot(c.r_fix[0],c.r_fix[1],'x', color='k')[0]

line_approx = ax_main.plot([],[],'-', color='b', label='small angle approx.')[0]
point_approx = ax_main.plot([],[],'o', color='b')[0]

line_exact = ax_main.plot([],[],'-', color='r', label='numerical ode integration')[0]
point_exact = ax_main.plot([],[],'o', color='r')[0]

def animate(frame):
    global line_approx, point_approx
    t = frame
    line_approx.set_data([c.r_fix[0], r_approx[0,t]], [c.r_fix[1], r_approx[1,t]])
    point_approx.set_data(r_approx[0,t],r_approx[1,t])

    line_exact.set_data([c.r_fix[0], r_exact[0,t]], [c.r_fix[1], r_exact[1,t]])
    point_exact.set_data(r_exact[0,t],r_exact[1,t])

    return line_approx,point_approx,line_exact,point_exact

animation = anim.FuncAnimation(fig, func=animate, frames=c.fps*c.t_max, interval=1000/c.fps, blit=True)

ax_main.legend()
plt.show()