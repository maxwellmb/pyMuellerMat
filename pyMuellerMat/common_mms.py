'''
This file defines some common mueller matrices as child classes to the MuellerMatrix class found in MuellerMat.py

The top of the file contains the functions 

All sign conventions and coordinate definitions follow Golstein's book on Polarization. 
'''

import numpy as np
from pyMuellerMat.common_mm_functions import *
from pyMuellerMat import MuellerMat


#######################################
############# Polarizers ##############
#######################################

class Polarizer(MuellerMat.MuellerMatrix):
    '''
    A MuellerMat.MuellerMatrix child class for a general polarizer
    '''

    def __init__(self, name='Polarizer'):
        super(Polarizer, self).__init__(general_polarizer_function, name=name)


class HorizontalPolarizer(MuellerMat.MuellerMatrix):
    '''
    A MuellerMat.MuellerMatrix child class for a horizontal polarizer
    '''

    def __init__(self, name='HorizontalPolarizer'):
        super(HorizontalPolarizer, self).__init__(horizontal_polarizer_function, name=name)


class VerticalPolarizer(MuellerMat.MuellerMatrix):
    '''
    A MuellerMat.MuellerMatrix child class for a vertical polarizer
    '''

    def __init__(self, name='VerticalPolarizer'):
        super(VerticalPolarizer, self).__init__(vertical_polarizer_function, name=name)


class WollastonPrism(MuellerMat.MuellerMatrix):
    '''
    A MuellerMat.MuellerMatrix child class for a wollaston prism
    '''

    def __init__(self, name='WollastonPrism'):
        super(WollastonPrism, self).__init__(wollaston_prism_function, name=name)


######################################
############# Retarders ##############
######################################

class Retarder(MuellerMat.MuellerMatrix):
    '''
    A MuellerMat.MuellerMatrix child class for a general polarizer
    '''

    def __init__(self, name='Retarder', phi=0):
        super(Retarder, self).__init__(general_retarder_function, name=name)


class HWP(MuellerMat.MuellerMatrix):
    '''
    A MuellerMat.MuellerMatrix child class for a half-wave polarizer
    '''

    def __init__(self, name='HalfwaveRetarder'):
        super(HWP, self).__init__(halfwave_retarder_function, name=name)


class QWP(MuellerMat.MuellerMatrix):
    '''
    A MuellerMat.MuellerMatrix child class for a quarter-wave polarizer
    '''

    def __init__(self, name='QuarterwaveRetarder'):
        super(QWP, self).__init__(quarterwave_retarder_function, name=name)


#################################
############# MISC ##############
#################################

#### The MuellerMatrix child classes ####
class Rotator(MuellerMat.MuellerMatrix):
    '''
    A MuellerMat.MuellerMatrix child class for a general rotator
    '''

    def __init__(self, name='Rotator'):
        super(Rotator, self).__init__(rotator_function, name=name)


class DiattenuatorRetarder(MuellerMat.MuellerMatrix):
    '''
    A MuellerMat.MuellerMatrix child class for a diattenuator retarder (Goldstein)
    '''

    def __init__(self, name='DiattenuatorRetarder'):
        super(DiattenuatorRetarder, self).__init__(diattenuator_retarder_function, name=name)


class DiattenuatorRetarder2(MuellerMat.MuellerMatrix):
    '''
    A MuellerMat.MuellerMatrix child class for a diattenuator retarder (Witzel)
    '''

    def __init__(self, name='DiattenuatorRetarder2'):
        super(DiattenuatorRetarder2, self).__init__(diattenuator_retarder_function2, name=name)

class InstrumentalPolarization(MuellerMat.MuellerMatrix):
    '''
    A MuellerMat.MuellerMatrix child class for instrumental polarization
    '''
    def __init__(self, name='InstrumentalPolarization'):
        super(InstrumentalPolarization, self).__init__(instrumental_polarization_function, name=name)


class UV_Sign_Flip(MuellerMat.MuellerMatrix):
    '''
    A MuellerMat.MuellerMatrix child class for instrumental polarization
    '''

    def __init__(self, name='UV_Sign_Flip'):
        super(UV_Sign_Flip, self).__init__(UV_sign_flip_function, name=name)
