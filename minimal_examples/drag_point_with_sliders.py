'''Drag a point in a plot and sync this with sliders'''

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

x_min, x_max = -1,1
y_min, y_max = -1,1

x = 0
y = 0
epsilon = 10
dragging = False

mpl.rcParams['figure.subplot.right'] = 0.8
fig, axs = plt.subplots(figsize=(9,8))
ax = axs
ax.set_xlim(x_min,x_max)
ax.set_ylim(y_min,y_max)
point = ax.plot(x,y,'o',markersize=10)[0]
ax_slider_x = fig.add_axes(rect=[0.82, 0.8, 0.13, 0.03])
slider_x = mpl.widgets.Slider(ax_slider_x, 'x', x_min, x_max, valinit=x, valfmt='%.2f')
ax_slider_y = fig.add_axes(rect=[0.82, 0.7, 0.13, 0.03])
slider_y = mpl.widgets.Slider(ax_slider_y, 'y', y_min, y_max, valinit=y, valfmt='%.2f')

def update_x(val):
    global x
    x = val
    update_plot()

def update_y(val):
    global y
    y = val
    update_plot()

def update_plot():
    point.set_data(x,y)

def update_sliders():
    slider_x.set_val(x)
    slider_y.set_val(y)

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
    if event.inaxes is None:
        return
    if dragging:
        x = event.xdata
        y = event.ydata
        update_plot()
        update_sliders()

slider_x.on_changed(update_x)
slider_y.on_changed(update_y)
fig.canvas.mpl_connect('button_press_event', on_mouse_press)
fig.canvas.mpl_connect('button_release_event', on_mouse_release)
fig.canvas.mpl_connect('motion_notify_event', on_mouse_motion)

plt.show()