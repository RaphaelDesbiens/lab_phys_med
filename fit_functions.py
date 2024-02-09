from scipy.optimize import curve_fit
import numpy as np
from math import exp, sqrt


def linear_function(x, m, b):

    return m*x + b


def linear_function_zero(x, m):
    return m * x + 0.23136066952780163


def constant_function(x, b):
    return 0*x + b


def linear_fit(x, y, intercept=False):
    if intercept:
        return curve_fit(linear_function_zero, x, y)
    return curve_fit(linear_function, x, y)


def constant_fit(x, y):
    return curve_fit(constant_function, x, y)


def gaussian_function(x, a, mu, sigma, b):
    return a * np.exp(-(x - mu)**2 / (2 * sigma**2)) + b


def gaussian_fit(x, y, guesses):

    return curve_fit(gaussian_function, x, y, guesses)


def pdd_function(x, a_pdd, n, mu, b_pdd):
    num_1 = x
    denom_1 = np.sqrt(x**2 + abs(n))
    expon = np.exp(-mu*x)

    return a_pdd*(num_1/denom_1)*expon + b_pdd


def pdd_fit(x, y, guesses):

    return curve_fit(pdd_function, x, y, guesses)


def expon_function(x, a, mu):

    return a*np.exp(-x*mu)


def expon_fit(x, y):

    return curve_fit(expon_function, x, y)
