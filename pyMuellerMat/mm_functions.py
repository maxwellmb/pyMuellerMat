import numba
import numpy as np

@numba.njit()
def lp_mm(theta: float = 0):
    """
    Rotated linear polarizer

    Parameters
    ----------
    theta : float
        Angle of polarization in radians.

    Notes
    -----
    Chipman 2019, Eq. 6.37
    """
    cos2th = np.cos(2 * theta)
    sin2th = np.sin(2 * theta)
    mm = 0.5 * np.array((
        (1, cos2th, sin2th, 0),
        (cos2th, cos2th**2, sin2th * cos2th, 0),
        (sin2th, sin2th * cos2th, sin2th**2, 0),
        (0, 0, 0, 0)
    ), dtype="f4")
    return mm

@numba.njit()
def wp_mm(theta: float = 0, delta: float = 0):
    """
    Rotated generic waveplate

    Parameters
    ----------
    theta : float
        Angle of fast axis in radians.
    delta : float
        Retardance in radians. For HWP use pi, for QWP use pi/2, etc.

    Notes
    -----
    Chipman 2019, Eq. 6.23
    """
    cos2th = np.cos(2 * theta)
    sin2th = np.sin(2 * theta)
    cosd = np.cos(delta)
    sind = np.sin(delta)
    mm = np.array((
        (1, 0, 0, 0),
        (0, cos2th**2 + cosd * sin2th**2, (1 - cosd) * cos2th * sin2th, -sind * sin2th),
        (0, (1 - cosd) * cos2th * sin2th, cosd * cos2th**2 + sin2th**2, cos2th * sind),
        (0, sind * sin2th, -cos2th * sind, cosd)
    ), dtype="f4")
    return mm
