'''
This file defines some common mueller matrix functions.
common_mms.py will use these functions to create child classes to the MuellerMatrix class found in MuellerMat.py

All sign conventions and coordinate definitions follow Golstein's book on Polarization. 
'''

import numpy as np
from pyMuellerMat.physical_models.charis_physical_models import HWP_retardance,IMR_retardance, M3_retardance, M3_diattenuation




#######################################
############# Polarizers ##############
#######################################

#### The functions that define the mueller matrices ####
def general_polarizer_function(px=1., py=1.):
    '''
    The mueller matrix for a general polarizer.
    The default kwargs px=py=1 returns a identity matrix.

    Goldstein Eq'm 5-9
    Kwargs:
    px	- The transmission of polarization along the x-axis
    py  - The transmission of polarization along the y-axis
    '''
    mm = 0.5 * np.array([[px ** 2 + py ** 2, px ** 2 - py ** 2, 0, 0],
                         [px ** 2 - py ** 2, px ** 2 + py ** 2, 0, 0],
                         [0, 0, 2 * px * py, 0],
                         [0, 0, 0, 2 * px * py]])
    return mm

# TODO: Make sure this uses the same x and y axis conventions as the above func
def general_linear_polarizer_function_with_theta(theta = 0):
    """
    The Mueller matrix for a linear polarizer at angle theta (in degrees).

    Args:
        theta: Angle of the polarizer's transmission axis in degrees.

    Returns:
        A 4x4 Mueller matrix representing the linear polarizer.
    """
    # Convert theta from degrees to radians
    theta_rad = np.deg2rad(theta)

    # Calculate px and py
    px = np.cos(theta_rad)
    py = np.sin(theta_rad)

    # Generate the Mueller matrix
    mm = 0.5 * np.array([[px ** 2 + py ** 2, px ** 2 - py ** 2, 0, 0],
                         [px ** 2 - py ** 2, px ** 2 + py ** 2, 0, 0],
                         [0, 0, 2 * px * py, 0],
                         [0, 0, 0, 2 * px * py]])
    return mm


def horizontal_polarizer_function():
    '''
    The mueller matrix for a horizontal polarizer
    The default kwarg px=1 returns an ideal horizontal polarizer.

    Goldstein Eq'n 5-12

    Kwargs:
    px	- The transmission of polarization along the x-axis
    '''
    mm = general_polarizer_function(px=1., py=0.)

    return mm


def vertical_polarizer_function():
    '''
    The mueller matrix for a vertical polarizer
    The default kwarg py=1 returns an ideal vertical polarizer.

    Goldstein Eq'n 5-14 (well.. close to it)

    Kwargs:
    py	- The transmission of polarization along the x-axis
    '''
    mm = general_polarizer_function(px=0., py=1.)

    return mm

# TODO: Test the new transmission_ratio value
def wollaston_prism_function(beam='o', eta=1., transmission_ratio = 1.):
    '''
    A function that returns mueller matrix for an ideal wollaston prism.

    Goldstein Eq'n 5-18

    kwargs:
    beam	- Equal to 'o' or 'e', corresponding to ordinary and extraordinary beams
    eta 	- A modulation efficiency term.
    transmission_ratio  - A scalar ratio between the o and e beams of the matrix
                          that is equivalent to EM ratio gain
    '''
    if (beam != 'o') & (beam != 'e'):
        print("For a wollaston prism you must specify a beam of either 'o' or 'e'.")
        print("Assuming you want 'o' for now.")
        beam = 'o'

    # If the ordinary beam then sign = 1
    if beam == 'o':
        sign = eta
    # If the extraordinary beam then sign = -1
    else:
        sign = -eta
        # Nulling out the ratio effect for the extraordinary beam
        transmission_ratio = 1

    mm = transmission_ratio * 0.5 * np.array([[1, sign, 0, 0],
                         [sign, 1, 0, 0],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0]])
    return mm


def general_diattenuator_function(d_h=0,d_45=0,d_r=0, T_avg=1):
    '''
    The mueller matrix for a general diattenuator.
    
    Chipman Eq'n 6.59
    
    Kwargs:
    d_h   -   Diattenuation for the horizontal component
    d_45  -   Diattenuation for the 45 degree component
    d_r   -   Diattenuation for the circular component
    T_avg -   The average transmission of the diattenuator
    '''
    d = np.sqrt(d_h**2 + d_45**2 + d_r**2)
    a = np.sqrt(1 - d**2)
    # return identity if no diattenuation
    if np.isclose(d, 0):
        return np.eye(4)
    else:
        coef = (T_avg*(1-a))/d**2
        mm1 = np.array([[1, d_h, d_45, d_r],
                        [d_h, a,0,0],
                        [d_45,0,a,0],
                        [d_r,0,0,a]])
        mm2 = np.array([[0,0,0,0],
                       [0,d_h**2, d_h*d_45, d_h*d_r],
                       [0,d_h*d_45, d_45**2, d_45*d_r],
                       [0,d_h*d_r, d_45*d_r, d_r**2]])
        mm = T_avg * mm1 + coef * mm2
        return mm


######################################
############# Retarders ##############
######################################

#### The functions that define the mueller matrices ####
def general_retarder_function(phi=0.):
    '''
    The mueller matrix for a general retarder.
    The default kwargs phi=0 corresponds to the identity matrix

    Golstein Eq'n 5-27
    Kwargs:
    phi	-	The phase retardance between the x and y components in radians
    '''
    mm = np.array([[1, 0, 0, 0],
                   [0, 1, 0, 0],
                   [0, 0, np.cos(phi), np.sin(phi)],
                   [0, 0, -np.sin(phi), np.cos(phi)]])

    return mm

def halfwave_retarder_function():
    '''
    The mueller matrix for a half-wave retarder

    Goldstein Eq'n 5-32
    '''
    return general_retarder_function(phi=np.pi)


def quarterwave_retarder_function():
    '''
    The mueller matrix for a quarter-wave retarder.
    Goldstein Eq'n 5-28
    '''
    return general_retarder_function(phi=np.pi / 2.)

def elliptical_retarder_function(phi_h=0, phi_45=0, phi_r=0):
    '''
    The mueller matrix for an elliptical retarder.
    
    Chipman Eq'n 6.28

    Kwargs:
    phi_h   -   Retardance for the horizontal component
    phi_45  -   Retardance for the 45 degree component
    phi_r   -   Retardance for the circular component
    '''
    phi = np.sqrt(phi_h**2 + phi_45**2 + phi_r**2)
    # return identity if no retardance
    if np.isclose(phi, 0):
        return np.eye(4)
    else:
        c = np.cos(phi)
        s = np.sin(phi)
        t = 1 - c
        two_two = (phi_h**2 + (phi_45**2+phi_r**2)*c)/phi**2
        two_three = (phi_45*phi_h*t)/phi**2+(phi_r*s)/phi
        two_four = (phi_r*phi_h*t)/phi**2-(phi_45*s)/phi
        three_two = (phi_h*phi_45*t)/phi**2-(phi_r*s)/phi
        three_three = (phi_45**2 + (phi_h**2+phi_r**2)*c)/phi**2
        three_four = (phi_r*phi_45*t)/phi**2+(phi_h*s)/phi
        four_two = (phi_h*phi_r*t)/phi**2+(phi_45*s)/phi
        four_three = (phi_45*phi_r*t)/phi**2-(phi_h*s)/phi
        four_four = (phi_r**2 + (phi_h**2+phi_45**2)*c)/phi**2

        mm = np.array([[1, 0, 0, 0],
                   [0, two_two, two_three, two_four],
                   [0, three_two, three_three, three_four],
                   [0, four_two, four_three, four_four]])

        return mm


#################################
############# MISC ##############
#################################

#### The functions that define the mueller matrices ####
def rotator_function(pa=0.):
    '''
    The mueller matrix for a rotator.
    The rotation theta defined from the positive x-axis in the direction of the y-axis.

    Goldstein Eq'n 5-41

    Kwargs:
    pa	-	The physical position angle of rotation in degrees. Note, the function will rotate the polarization by 2*pa
    '''

    pa_rad = np.radians(pa)

    mm = np.array([[1, 0, 0, 0],
                   [0, np.cos(2 * pa_rad), np.sin(2 * pa_rad), 0],
                   [0, -np.sin(2 * pa_rad), np.cos(2 * pa_rad), 0],
                   [0, 0, 0, 1]])
    return mm


def diattenuator_retarder_function(epsilon=1, phi=0.):
    '''
    The function that describes a linear diattenuator that has a retardance (van Holstein et al. 2020, Eq'n 20)

    Inputs:
    epsilon -	The diattenuation
    phi		-	The phase retardance between the x and y components in radians

    '''
    mm = np.array([[1, epsilon, 0, 0],
                   [epsilon, 1, 0, 0],
                   [0, 0, np.sqrt(1 - epsilon ** 2) * np.cos(phi), np.sqrt(1 - epsilon ** 2) * np.sin(phi)],
                   [0, 0, -np.sqrt(1 - epsilon ** 2) * np.sin(phi), np.sqrt(1 - epsilon ** 2) * np.cos(phi)]])
    return mm


def diattenuator_retarder_function2(r1=1., r2=0., delta=0.):
    '''
    The function that describes a linear diattenuator that has a retardance (Witzel)

    Inputs:
    r1      -  	The first reflection coefficient (perpendicular)
    r2      -	The second reflection coefficient (parallel)
    delta   -   The relative retardance between the components

    '''
    mm = np.array([[0.5 * (r1 + r2), 0.5 * (r1 - r2), 0, 0],
                   [0.5 * (r1 - r2), 0.5 * (r1 + r2), 0, 0],
                   [0, 0, np.sqrt(r1 * r2) * np.cos(delta), -np.sqrt(r1 * r2) * np.sin(delta)],
                   [0, 0, np.sqrt(r1 * r2) * np.sin(delta), np.sqrt(r1 * r2) * np.cos(delta)]])
    return mm


def instrumental_polarization_function(IPQ=0,IPU=0,IPV=0):
    '''
    This function describes just instrumental polarization terms
    '''
    mm = np.array([[1,IPQ,0,0],
                   [IPQ,1,0,0],
                   [IPU,0,1,0],
                   [IPV,0,0,1]])

    return mm

def UV_sign_flip_function():
    '''
    This function describes a reflection that flips the signs of U and V
    '''
    mm = np.array([[1,0,0,0],
                    [0,1,0,0],
                    [0,0,-1,0],
                    [0,0,0,-1]])
    return mm

def arbitrary_matrix_function(**kwargs):
    """
    Returns a 4x4 matrix provided by the user via 'mm' or defaults to a zero matrix.
    """
    return kwargs.get('mm', np.zeros((4, 4)))


###################################
############# SPECIAL #############
###################################



def two_layer_HWP_function(wavelength=500, w_SiO2=0, w_MgF2=0):
    '''
    The Mueller matrix for a two layer HWP with one SiO2 crystal layer
    and one MgF2 layer. The physical model is from Joost t Hart 2021.

    Inputs:
    wavelength   -  The wavelength in nm 
    w_SiO2       -  The width of the SiO2 layer
    w_MgF2       -  The width of the MgF2 layer
    
    '''
    phi = HWP_retardance(np.array(wavelength), w_SiO2, w_MgF2)[0]

    mm = np.array([[1, 0, 0, 0],
                   [0, 1, 0, 0],
                   [0, 0, np.cos(phi), np.sin(phi)],
                   [0, 0, -np.sin(phi), np.cos(phi)]])
    return mm

def SCExAO_IMR_function(wavelength=500, d=0):
    '''
    The mueller matrix for the SCExAO image rotator.
    The physical models are from Joost t Hart 2021.
    

    Inputs:
    wavelength    -  The wavelength in nm
    d             -  The width of the film
    
    '''
    phi = IMR_retardance(np.array(wavelength), d)[0]

    mm = np.array([[1, 0, 0, 0],
                   [0, 1, 0, 0],
                   [0, 0, np.cos(phi), np.sin(phi)],
                   [0, 0, -np.sin(phi), np.cos(phi)]])
    return mm

def SUBARU_M3_function(wavelength=500,m1=2.104,b1=14.2,m2=2.1,b2=13.2):
    '''
    The mueller matrix for CHARIS's M3.
    The physical models are from Joost t Hart 2021.
    

    Inputs:
    wavelength    -  The wavelength in nm
    m1,b1,m2,b2            -  Dialectric function approximation exponents
    
    '''

    epsilon = M3_diattenuation(wavelength,m1,b1,m2,b2)
    phi = M3_retardance(wavelength,m1,b1,m2,b2)

    mm = np.array([[1, epsilon, 0, 0],
    [epsilon, 1, 0, 0],
    [0, 0, np.sqrt(1 - epsilon ** 2) * np.cos(phi), np.sqrt(1 - epsilon ** 2) * np.sin(phi)],
    [0, 0, -np.sqrt(1 - epsilon ** 2) * np.sin(phi), np.sqrt(1 - epsilon ** 2) * np.cos(phi)]])
    return mm

def general_diattenuator_retarder_function(d_h=0,d_45=0,d_r=0, T_avg=1, phi_h=0, phi_45=0, phi_r=0):
    '''
    Combination of previous two functions for general diattenuator and elliptical retarder.
    Multiplication order: diattenuator first, then retarder.

    Inputs:
    d_h     -   The diattenuation for the horizontal component
    d_45    -   The diattenuation for the 45 degree component
    d_r     -   The diattenuation for the circular component
    T_avg   -   The average transmission of the diattenuator
    phi_h   -   Retardance for the horizontal component
    phi_45  -   Retardance for the 45 degree component
    phi_r   -   Retardance for the circular component
    '''

    mm_diat = general_diattenuator_function(d_h,d_45,d_r, T_avg)
    mm_ret = elliptical_retarder_function(phi_h, phi_45, phi_r)
    mm = np.matmul(mm_diat, mm_ret)
    return mm

def elliptical_IMR_function(wavelength=500):
    '''
    Hardcoded elliptical retarder function for the SCExAO IMR.
    
    Inputs:
    wavelength   -  The wavelength in nm 
    '''
    wavelength_bins = np.array([1159.5614, 1199.6971, 1241.2219, 1284.184 , 1328.6331, 1374.6208,
        1422.2002, 1471.4264, 1522.3565, 1575.0495, 1629.5663, 1685.9701,
        1744.3261, 1804.7021, 1867.1678, 1931.7956, 1998.6603, 2067.8395,
        2139.4131, 2213.4641, 2290.0781, 2369.3441])
    phi_h_list = np.array([4.31312706, 4.04490182, 3.81881104, 3.54188033, 3.17133585,
       2.74597295, 2.46420845, 2.18764466, 1.93889396, 1.72839182,
       1.52855398, 1.36617595, 1.2501473 , 1.15224628, 1.0693708 ,
       1.01783268, 0.99111784, 0.97012524, 0.96460966, 0.97201315,
       0.98230021, 1.01028539])
    phi_45_list = np.array([6.37563323e-18, 2.81046745e-02, 1.57544066e-02, 1.65265292e-02,
       8.77060264e-03, 1.30015816e-10, 7.98877796e-04, 1.00000000e-10,
       1.82055679e-18, 3.62377836e-17, 1.00000000e-10, 1.00000000e-10,
       2.44626001e-03, 3.15177374e-03, 5.25231957e-03, 3.47119295e-03,
       7.04947853e-03, 9.43217249e-03, 1.18566179e-02, 1.83210208e-02,
       1.69431276e-02, 6.76247167e-02])
    phi_r_list = np.array([2.53065285e-02, 1.75412596e-02, 3.25702366e-24, 9.73850092e-17,
       1.63679577e-16, 1.00000000e-10, 7.60489176e-23, 1.00000000e-10,
       4.40273589e-19, 4.19322465e-17, 1.00000000e-10, 6.70684172e-04,
       4.41932060e-03, 1.09646232e-02, 1.22877305e-02, 1.34954416e-02,
       1.61165870e-02, 1.77312738e-02, 1.63337925e-02, 1.34526311e-02,
       1.15389845e-02, 5.12554414e-03])
    phi_h = np.interp(wavelength, wavelength_bins, phi_h_list)
    phi_45 = np.interp(wavelength, wavelength_bins, phi_45_list)
    phi_r = np.interp(wavelength, wavelength_bins, phi_r_list)
    mm = elliptical_retarder_function(phi_h, phi_45, phi_r)
    return mm

def CHARIS_wollaston_function(wavelength=500, beam='o'):
    '''
    CHARIS wollaston model with hardcoded eta values
    
    Inputs:
    wavelength   -  The wavelength in nm
    beam         -  'o' or 'e' for the ordinary and extraordinary beams
    '''
    wol_eta = np.array([1.  , 0.99220673, 0.99660934, 0.98748931, 0.97977223,
       0.9887953 , 0.99008662, 0.99190127, 0.99125159, 0.99385762,
       0.99246299, 0.99329655, 0.99487966, 0.99382083, 0.99388459,
       0.99286555, 0.99500475, 0.99025065, 0.99027029, 0.9846229 ,
       0.9809924 , 0.96658868])
    wavelength_bins = np.array([1159.5614, 1199.6971, 1241.2219, 1284.184 , 1328.6331, 1374.6208,
        1422.2002, 1471.4264, 1522.3565, 1575.0495, 1629.5663, 1685.9701,
        1744.3261, 1804.7021, 1867.1678, 1931.7956, 1998.6603, 2067.8395,
        2139.4131, 2213.4641, 2290.0781, 2369.3441])
    eta = np.interp(wavelength, wavelength_bins, wol_eta)
    mm = wollaston_prism_function(beam=beam, eta=eta)
    return mm
    
