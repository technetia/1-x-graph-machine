# math_funcs.py

from __future__ import division

__all__ = ["FUNCTIONS", "CONSTANTS"]

import sys as _sys
import math
    
CONSTANTS = {
    "e" : math.e,
    "pi" : math.pi
}

# implement inverse hyperbolic functions if Python 2.5
if _sys.version_info[1] < 6:
    def asinh(x):
        """
        Inverse of hyperbolic sine.
        """
        return math.log(x+sqrt(x**2+1))

    def acosh(x):
        """
        Inverse of hyperbolic cosine.
        """
        return math.log(x+sqrt(x**2-1))

    def atanh(x):
        """
        Inverse of hyperbolic tangent.
        """
        return 0.5*math.log((1+x)/(1-x))
    
else:
    asinh = math.asinh
    acosh = math.acosh
    atanh = math.atanh

def ln(x):
    """
    A synonym for natural logarithm, just in case people are
    used to punching in ln for natural logarithm.

    The reason why we don't just have ln = math.log is because
    math.log can be called with a second argument indicating
    the base of the logarithm...that would be confusing for a
    function for only natural logarithm.
    """
    return math.log(x)

def csc(x):
    """
    Trigonometric function cosecant (reciprocal of sine).
    """
    return 1 / math.sin(x)

def sec(x):
    """
    Trigonometric function secant (reciprocal of cosine).
    """
    return 1 / math.cos(x)

def cot(x):
    """
    Trigonometric function cotangent (reciprocal of tangent).
    """
    return 1 / math.tan(x)

def acsc(x):
    """
    Inverse of cosecant.
    """
    return math.asin(1 / x)

def asec(x):
    """
    Inverse of secant.
    """
    return math.acos(1 / x)

def acot(x):
    """
    Inverse of cotangent.
    """
    return math.atan(1 / x)

def csch(x):
    """
    Hyperbolic cosecant (reciprocal of hyperbolic sine).
    """
    return 1 / math.sinh(x)

def sech(x):
    """
    Hyperbolic secant (reciprocal of hyperbolic cosine).
    """
    return 1 / math.cosh(x)

def coth(x):
    """
    Hyperbolic cotangent (reciprocal of hyperbolic tangent).
    """
    return 1 / math.tanh(x)

def acsch(x):
    """
    Inverse of hyperbolic cosecant.
    """
    return asinh(1 / x)

def asech(x):
    """
    Inverse of hyperbolic secant.
    """
    return acosh(1 / x)

def acoth(x):
    """
    Inverse of hyperbolic cotangent.
    """
    return atanh(1 / x)

FUNCTIONS = {
    # misc. functions
    "abs" : abs,
    "sqrt" : math.sqrt,

    # integral conversion functions
    "floor" : math.floor,
    "ceil" : math.ceil,

    # angle conversion functions
    "deg" : math.degrees,
    "rad" : math.radians,
    
    # trigonometric functions
    "sin" : math.sin,
    "cos" : math.cos,
    "tan" : math.tan,
    "asin" : math.asin,
    "acos" : math.acos,
    "atan" : math.atan,
    
    "csc" : csc,
    "sec" : sec,
    "cot" : cot,
    "acsc" : acsc,
    "asec" : asec,
    "acot" : acot,

    # hyperbolic functions
    "sinh" : math.sinh,
    "cosh" : math.cosh,
    "tanh" : math.tanh,
    "asinh" : asinh,
    "acosh" : acosh,
    "atanh" : atanh,
    
    "csch" : csch,
    "sech" : sech,
    "coth" : coth,
    "acsch" : acsch,
    "asech" : asech,
    "acoth" : acoth,
    
    # exponential/logarimithic functions
    "exp" : math.exp,
    "log" : math.log,
    "log10" : math.log10,
    "ln" : ln,
}
