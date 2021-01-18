"""This is the main script of the pendulum 2D animation."""

from matplotlib.axes import Axes
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import numpy as np

import pendulum_2d_calc as calc
from pendulum_2d_calc import constants as c

# Generate the data
data = calc.gen_data()

# List the visual properties of all plots
visuals = {}
visuals['approx'] = {'color':'b', 'label':'small angle approximation'}
visuals['exact'] = {'color':'r', 'label':'numerical ode integration'}
velocity_scl = 0.5

# init figure
fig = plt.figure()
fig.suptitle('2D pendulum')

# init axes / subplots
ax_main = plt.subplot(221, box_aspect=1)
x_min = np.min([np.min(data[method]['r'][0]) for method in data]+[c.r_fix[0]])
x_max = np.max([np.max(data[method]['r'][0]) for method in data]+[c.r_fix[0]])
y_min = np.min([np.min(data[method]['r'][1]) for method in data]+[c.r_fix[1]])
y_max = np.max([np.max(data[method]['r'][1]) for method in data]+[c.r_fix[1]])
x_margin = 0.1*np.abs(x_max-x_min)
y_margin = 0.1*np.abs(y_max-y_min)
ax_main.set_xlim(x_min-x_margin, x_max+x_margin)
ax_main.set_ylim(y_min-y_margin, y_max+y_margin)
ax_main.set_xlabel('x')
ax_main.set_ylabel('y')
ax_main.set_title('physical space')
ax_main.set_anchor('SE')

ax_y = plt.subplot(222, sharey=ax_main, box_aspect=1)
ax_y.set_xlim(0,c.t_max)
ax_y.set_xlabel('t / s')
ax_y.set_ylabel('y')
ax_y.set_title('y coordinate')
ax_y.set_anchor('SW')

ax_x =  plt.subplot(223, sharex=ax_main, box_aspect=1)
ax_x.set_ylim(c.t_max,0)
ax_x.set_ylabel('t / s')
ax_x.set_xlabel('x')
ax_x.set_title('x coordinate')
ax_x.set_anchor('NE')

ax_phasespace =  plt.subplot(224, box_aspect=1)
phi_min = np.min([np.min(data[method]['phi']) for method in data])
phi_max = np.max([np.max(data[method]['phi']) for method in data])
phi_dot_min = np.min([np.min(data[method]['phi_dot']) for method in data])
phi_dot_max = np.max([np.max(data[method]['phi_dot']) for method in data])
ax_phasespace.set_xlim(phi_min-0.3, phi_max+0.3)
ax_phasespace.set_ylim(phi_dot_min-0.3, phi_dot_max+0.3)
ax_phasespace.set_xlabel('phi / rad')
ax_phasespace.set_ylabel('phi_dot / rad s^-1')
ax_phasespace.set_title('phasespace of the angle')
ax_phasespace.set_anchor('NW')


# init plots
lines = {}
points = {}
velocity_arrows = {}
y_plots = {}
x_plots = {}
phasespace_lines = {}
phasespace_points = {}

for method, visuals_i   in visuals.items():
    # main plots
    lines[method] = ax_main.plot([],[],'-', color=visuals_i['color'], label=visuals_i['label'])[0]
    points[method] = ax_main.plot([],[],'o', color=visuals_i['color'])[0]
    velocity_arrows[method] = ax_main.arrow(0,0,0,0)
    # graph plots
    y_plots[method] = ax_y.plot([],[],'-', color=visuals_i['color'])[0]
    x_plots[method] = ax_x.plot([],[],'-', color=visuals_i['color'])[0]
    phasespace_lines[method] = ax_phasespace.plot([],[],'-', color=visuals_i['color'])[0]
    phasespace_points[method] = ax_phasespace.plot([],[],'o', color=visuals_i['color'])[0]

fix = ax_main.plot(c.r_fix[0],c.r_fix[1],'x', color='k')[0]

# set the legend
fig.legend()

# do the animation

def animate(frame):
    t = frame

    for method, data_i in data.items():
        # main plots
        lines[method].set_data([c.r_fix[0],data_i['r'][0,t]], [c.r_fix[1],data_i['r'][1,t]])
        points[method].set_data([data_i['r'][0,t], data_i['r'][1,t]])
        ax_main.patches.remove(velocity_arrows[method])
        velocity_arrows[method] = ax_main.arrow(*data_i['r'][:,t], *(velocity_scl*data_i['r_dot'][:,t]), color=visuals[method]['color'], head_width=0.05)
        # graph plots
        y_plots[method].set_data(c.t[:t],data_i['r'][1,:t])
        x_plots[method].set_data(data_i['r'][0,:t],c.t[:t])
        phasespace_lines[method].set_data(data_i['phi'][:t],data_i['phi_dot'][:t])
        phasespace_points[method].set_data(data_i['phi'][t],data_i['phi_dot'][t])

    artists = []
    artists.extend(list(lines.values()))
    artists.extend(list(points.values()))
    artists.extend(list(velocity_arrows.values()))
    artists.extend(list(y_plots.values()))
    artists.extend(list(x_plots.values()))
    artists.extend(list(phasespace_lines.values()))
    artists.extend(list(phasespace_points.values()))
    return artists

animation = anim.FuncAnimation(fig, func=animate, frames=c.fps*c.t_max, interval=1000/c.fps, blit=True)

plt.show()