'''Drag a point in a plot'''

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

x = 0
y = 0
epsilon = 5
dragging = False

fig, axs = plt.subplots()
ax = axs
point = ax.plot(x,y,'o')[0]

def on_mouse_press(event):
    global dragging
    if event.inaxes is None:
        return
    if event.button != 1:
        return
    trans_data_to_disp = ax.transData.transform
    xy_disp = trans_data_to_disp([x,y])
    xy_mouse = np.array([event.x,event.y])
    if np.linalg.norm(xy_disp-xy_mouse) <= epsilon:
        dragging = True

def on_mouse_release(event):
    global dragging
    dragging = False

def on_mouse_motion(event):
    global x,y
    if dragging:
        x = event.xdata
        y = event.ydata
        point.set_data(x,y)
        fig.canvas.draw()

fig.canvas.mpl_connect('button_press_event', on_mouse_press)
fig.canvas.mpl_connect('button_release_event', on_mouse_release)
fig.canvas.mpl_connect('motion_notify_event', on_mouse_motion)

plt.show()