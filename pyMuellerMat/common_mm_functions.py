'''
This file defines some common mueller matrix functions.
common_mms.py will use these functions to create child classes to the MuellerMatrix class found in MuellerMat.py

All sign conventions and coordinate definitions follow Golstein's book on Polarization. 
'''

import numpy as np


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


def wollaston_prism_function(beam='o', eta=1.):
    '''
    A function that returns mueller matrix for an ideal wollaston prism.

    Goldstein Eq'n 5-18

    kwargs:
    beam	- Equal to 'o' or 'e', corresponding to ordinary and extraordinary beams
    eta 	- A modulation efficiency term.
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

    mm = 0.5 * np.array([[1, sign, 0, 0],
                         [sign, 1, 0, 0],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0]])
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