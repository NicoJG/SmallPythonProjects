import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim

# animation constants
fps = 60 # frames per second
t_max = 10 # end time of the simulation in s
dt = 1/fps # seconds per frame

# physical constants
r_fix = np.array([0,0]) # where the pendulum is attached to in m
L = 5 # length of the pendulum in m
phi_0 = np.pi/4 # starting value of phi in rad
phi_dot_0 = 0 # starting angular velocity in rad/s
g = 9.81 # gravitational acceleration in m/s^2
omega = np.sqrt(g/L) # angular frequency in 1/s

# calculate the position based on phi(t)
def r(phi):
    e_phi = np.array([np.sin(phi), -np.cos(phi)])
    return r_fix.reshape(2,1) + L * e_phi

# calculate the velocity based on phi and phi_dot
def r_dot(phi, phi_dot):
    e_phi_dot = np.array([np.cos(phi), np.sin(phi)])
    return L * phi_dot * e_phi_dot

# calculate the acceleration based on phi, phi_dot and phi_double_dot
def r_double_dot(phi, phi_dot, phi_double_dot):
    e_phi_dot = np.array([np.cos(phi), np.sin(phi)])
    e_phi_double_dot = np.array([-np.sin(phi), np.cos(phi)])
    return L * phi_double_dot * e_phi_dot + L * phi_dot**2 * e_phi_double_dot

# exact ode
phi_double_dot = lambda phi : -omega*np.sin(phi)

# small angle approximation solution
phi = lambda t : phi_0*np.cos(omega*t) + phi_dot_0*np.sin(omega*t)
# small angle approximation derivative
phi_dot = lambda t : -phi_0*np.sin(omega*t) + phi_dot_0*np.cos(omega*t)

#########################################

### small angle approximation data construction
t = np.arange(start=0,step=dt,stop=t_max)
r_approx = r(phi(t))

print(r_approx)

plt.plot(t, r_approx[0], label='r_approx_x')
plt.plot(t, r_approx[1], label='r_approx_y')

plt.legend()
plt.show()