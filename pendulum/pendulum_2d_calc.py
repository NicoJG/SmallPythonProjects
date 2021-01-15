"""This module calculates all needed data for the pendulum_2d_anim.py where a 2D pendulum is animated.
All the calculations are in my OneNote Notebook"""

import numpy as np
from scipy.integrate import odeint

class constants:
    """constants defining the pendulum and the time aspect"""
    # timing constants
    fps = 60 # frames per second
    t_max = 10 # end time of the simulation in s
    dt = 1/fps # seconds per frame
    t = np.arange(start=0, step=dt, stop=t_max)
    # physical constants
    r_fix = np.array([0,0]) # where the pendulum is attached to in m
    L = 1 # length of the pendulum in m
    phi_0 = 0.8 # starting value of phi in rad
    phi_dot_0 = 0 # starting angular velocity in rad/s
    g = 9.81 # gravitational acceleration in m/s^2
    omega = np.sqrt(g/L) # angular frequency in 1/s

class mathematical_functions:
    """mathematical functions describing the problems solution"""

    def r(phi):
        """calculate the position based on phi"""
        c = constants
        e_phi = np.array([np.sin(phi), -np.cos(phi)])
        return np.reshape(c.r_fix,(2,1)) + c.L * e_phi

    def r_dot(phi, phi_dot):
        """calculate the velocity based on phi and phi_dot"""
        c = constants
        e_phi_dot = np.array([np.cos(phi), np.sin(phi)])
        return c.L * phi_dot * e_phi_dot

    def r_double_dot(phi, phi_dot, phi_double_dot):
        """calculate the acceleration based on phi, phi_dot and phi_double_dot"""
        c = constants
        e_phi_dot = np.array([np.cos(phi), np.sin(phi)])
        e_phi_double_dot = np.array([-np.sin(phi), np.cos(phi)])
        return c.L * phi_double_dot * e_phi_dot + c.L * phi_dot**2 * e_phi_double_dot

    def phi_double_dot(phi):
        """calculate phi_double_dot via the exact ordinary differential equation"""
        c = constants
        return -c.omega*np.sin(phi) # TODO omega ersetzen

    def phi(t):
        """small angle approximation solution for phi(t)"""
        c = constants
        return c.phi_0*np.cos(c.omega*t) + c.phi_dot_0*np.sin(c.omega*t)

    # small angle approximation derivative
    def phi_dot(t):
        """small angle approximation solution for phi_dot(t)"""
        c = constants
        return -c.phi_0*np.sin(c.omega*t) + c.phi_dot_0*np.cos(c.omega*t)

def gen_data_approx() -> dict:
    """Generates all the data of the small angle approximation"""
    c = constants
    f = mathematical_functions

    phi_approx = f.phi(c.t)
    phi_dot_approx = f.phi_dot(c.t)
    r_approx = f.r(phi_approx)
    r_dot_approx = f.r_dot(phi_approx, phi_dot_approx)
    r_double_dot_approx = f.r_double_dot(phi_approx, phi_dot_approx, f.phi_double_dot(phi_approx))

    data_approx = {"phi":phi_approx,"phi_dot":phi_dot_approx, "r":r_approx, "r_dot":r_dot_approx, "r_double_dot":r_double_dot_approx}
    return data_approx

def gen_data_exact() -> dict:
    """Generates all the data of the numerical integration of the exact differential equation."""
    c = constants
    f = mathematical_functions

    def phi_ode(y, t):
        """function for the numerical integration through odeint"""
        phi, phi_dot = y
        dydt = [phi_dot, f.phi_double_dot(phi)]
        return dydt

    y_0 = [c.phi_0, c.phi_dot_0]
    y = odeint(phi_ode, y_0, c.t)
    phi_exact = y[:,0]
    phi_dot_exact = y[:,1]

    r_exact = f.r(phi_exact)
    r_dot_exact = f.r_dot(phi_exact, phi_dot_exact)
    r_double_dot_exact = f.r_double_dot(phi_exact, phi_dot_exact, f.phi_double_dot(phi_exact))

    data_exact = {"phi":phi_exact, "phi_dot":phi_dot_exact, "r":r_exact, "r_dot":r_dot_exact, "r_double_dot":r_double_dot_exact}
    return data_exact

def gen_data() -> dict:
    """Generates the data for the animation using the constants defined above.
    Output structure:
        {
            "approx": {"r","r_dot","r_double_dot","phi"},
            "exact": {"r","r_dot","r_double_dot","phi"}
        }"""
    data_approx = gen_data_approx()
    data_exact = gen_data_exact()
    data = {"approx":data_approx, "exact":data_exact}
    return data
