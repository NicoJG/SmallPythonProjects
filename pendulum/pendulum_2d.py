import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim
from scipy.integrate import odeint

# animation constants
fps = 60 # frames per second
t_max = 10 # end time of the simulation in s
dt = 1/fps # seconds per frame

# physical constants
r_fix = np.array([0,0]) # where the pendulum is attached to in m
L = 5 # length of the pendulum in m
phi_0 = np.pi/6 # starting value of phi in rad
phi_dot_0 = 1 # starting angular velocity in rad/s
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
phi_double_dot = lambda phi, omega : -omega*np.sin(phi)

# small angle approximation solution
phi = lambda t : phi_0*np.cos(omega*t) + phi_dot_0*np.sin(omega*t)
# small angle approximation derivative
phi_dot = lambda t : -phi_0*np.sin(omega*t) + phi_dot_0*np.cos(omega*t)

#########################################
# data construction

t = np.arange(start=0,step=dt,stop=t_max)

### small angle approximation
r_approx = r(phi(t))

### exact ode integration
def phi_ode(y, t, omega):
    phi, phi_dot = y
    dydt = [phi_dot, phi_double_dot(phi,omega)]
    return dydt

y_0 = [phi_0,phi_dot_0]

y = odeint(phi_ode, y_0, t, args=(omega,))
phi_exact = y[:,0]
phi_dot_exact = y[:,1]
print(phi_exact)
r_exact = r(phi_exact)


#########################################
### Animation

fig, axs = plt.subplots()
ax_main = axs
ax_main.set_xlim(-L*1.5,L*1.5)
ax_main.set_ylim(-L*1.5,L*1.5)
ax_main.set_aspect('equal')
ax_main.set_xlabel('x')
ax_main.set_ylabel('y')

fix = ax_main.plot(r_fix[0],r_fix[1],'x', color='k')[0]

line_approx = ax_main.plot([],[],'-', color='b', label='small angle approx.')[0]
point_approx = ax_main.plot([],[],'o', color='b')[0]

line_exact = ax_main.plot([],[],'-', color='r', label='numerical ode integration')[0]
point_exact = ax_main.plot([],[],'o', color='r')[0]

def animate(frame):
    global line_approx, point_approx
    t = frame
    line_approx.set_data([r_fix[0], r_approx[0,t]], [r_fix[1], r_approx[1,t]])
    point_approx.set_data(r_approx[0,t],r_approx[1,t])

    line_exact.set_data([r_fix[0], r_exact[0,t]], [r_fix[1], r_exact[1,t]])
    point_exact.set_data(r_exact[0,t],r_exact[1,t])

    return line_approx,point_approx,line_exact,point_exact

animation = anim.FuncAnimation(fig, func=animate, frames=fps*t_max, interval=1000/fps, blit=True)

ax_main.legend()
plt.show()