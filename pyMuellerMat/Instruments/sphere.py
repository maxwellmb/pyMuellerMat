import numpy as np

# import pyMuellerMat.common_mm_functions import *
import pyMuellerMat.common_mm_functions as cmf
import pyMuellerMat.common_mms as cmm
from pyMuellerMat import MuellerMat

# def sphere_hwp(epsilon=1,retardance=0.,offset=0.):
def sphere_hwp_function(band='H'):
	'''
	A function that describes the SPHERE hwp as a diattenuator_retarder. 
	Based on Rob van Holstein's master's thesis. 
	'''

	if band == 'Y':
		epsilon = 1.00046
		phi = np.radians(184.2)
		offset = 0.18589
	elif band == 'J':
		epsilon = 1.000851
		phi = np.radians(182.5)
		offset = 0.18589
	elif band == 'H':
		epsilon = 1.00055
		phi = np.radians(170.5)
		offset = 0.18589
	elif band == 'K':
		epsilon = 1.00082
		phi = np.radians(177.5)
		offset = 0.18589
	else:
		print("The band you entered is not recognized. Please enter 'Y,J,H or K'.")
		print("Assuming you want 'H' band.")
		epsilon = 1.00055
		phi = np.radians(170.5)
		offset = 0.18589

	#Setup a diattenuator retarder
	mm = cmf.diattenuator_retarder_function(epsilon=epsilon,phi=phi)

	#Apply the offset as a rotation
	mm = np.matmul(np.matmul(cmf.rotator_function(-offset),mm),cmf.rotator_function(offset))

	return mm

class SphereHWP(MuellerMat.MuellerMatrix):
	'''
	A MuellerMat.MuellerMatrix child class for the sphere HWP
	'''
	def __init__(self,name='Sphere_HWP'):
		super(SphereHWP, self).__init__(sphere_hwp_function,name=name)

def sphere_derotator_function(band='H'):
	'''
	A function that describes the SPHERE derotator as a diattenuator_retarder. 
	Based on Rob van Holstein's master's thesis. 
	'''
	if band == 'Y':
		epsilon = 1.00182
		phi = np.radians(126.1)
		offset = 0.53088
	elif band == 'J':
		epsilon = 1.01658
		phi = np.radians(203.9)
		offset = 0.53088
	elif band == 'H':
		epsilon = 1.00453
		phi = np.radians(99.39)
		offset = 0.53088
	elif band == 'K':
		epsilon = 0.99302
		phi = np.radians(84.17)
		offset = 0.53088
	else:
		print("The band you entered is not recognized. Please enter 'Y,J,H or K'.")
		print("Assuming you want 'H' band.")
		epsilon = 1.00453
		phi = np.radians(99.39)
		offset = 0.53088

	#Setup a diattenuator retarder
	mm = cmf.diattenuator_retarder_function(epsilon=epsilon,phi=phi)

	#Apply the offset as a rotation
	mm = np.matmul(np.matmul(cmf.rotator_function(-offset),mm),cmf.rotator_function(offset))

	return mm

class SphereDerotator(MuellerMat.MuellerMatrix):
	'''
	A MuellerMat.MuellerMatrix child class for the sphere HWP
	'''
	def __init__(self,name='Sphere_Derotator'):
		super(SphereDerotator, self).__init__(sphere_derotator_function,name=name)

def sphere_M4_function(band='H'):
	'''
	A function that describes the SPHERE M4 mirror as a diattenuator_retarder. 
	Based on Rob van Holstein's master's thesis. 
	'''

	if band == 'Y':
		epsilon = 0.9526
		phi = np.radians(188.1)
	elif band == 'J':
		epsilon = 0.9662
		phi = np.radians(186.6)
	elif band == 'H':
		epsilon = 0.9738
		phi = np.radians(185.0)
	elif band == 'K':
		epsilon = 0.9785
		phi = np.radians(183.7)
	else:
		print("The band you entered is not recognized. Please enter 'Y,J,H or K'.")
		print("Assuming you want 'H' band.")
		epsilon = 0.9738
		phi = np.radians(185.0)

	#Setup a diattenuator retarder
	mm = cmf.diattenuator_retarder_function(epsilon=epsilon,phi=phi)

	return mm

class SphereM4(MuellerMat.MuellerMatrix):
	'''
	A MuellerMat.MuellerMatrix child class for the sphere HWP
	'''
	def __init__(self,name='Sphere_M4'):
		super(SphereM4, self).__init__(sphere_M4_function,name=name)

def sphere_UT_function(band='H'):
	'''
	A function that describes the mueller matrix of the UT3 telescope as a diattenuator_retarder. 
	Based on Rob van Holstein's master's thesis. 
	'''

	if band == 'Y':
		epsilon = 0.9666
		phi = np.radians(188.1)
	elif band == 'J':
		epsilon = 0.9761
		phi = np.radians(186.6)
	elif band == 'H':
		epsilon = 0.9813
		phi = np.radians(185.0)
	elif band == 'K':
		epsilon = 0.9851
		phi = np.radians(183.7)
	else:
		print("The band you entered is not recognized. Please enter 'Y,J,H or K'.")
		print("Assuming you want 'H' band.")
		epsilon = 0.9813
		phi = np.radians(185.0)

	#Setup a diattenuator retarder
	mm = cmf.diattenuator_retarder_function(epsilon=epsilon,phi=phi)

	return mm

class SphereMUT(MuellerMat.MuellerMatrix):
	'''
	A MuellerMat.MuellerMatrix child class for the sphere HWP
	'''
	def __init__(self,name='Sphere_MUT'):
		super(SphereMUT, self).__init__(sphere_UT_function,name=name)

def sphere_polarizers_function(band='H'):
	'''
	A function that describes the efficiency of the polarizers.
	'''

	if band == 'Y':
		efficiency = 0.9607
	elif band == 'J':
		efficiency = 0.9791
	elif band == 'H':
		efficiency = 0.9910
	elif band == 'K':
		efficiency = 0.9688
	else:
		print("The band you entered is not recognized. Please enter 'Y,J,H or K'.")
		print("Assuming you want 'H' band.")
		efficiency = 0.9910
		

	mm = np.array([[1,0,				  0, 0],
				   [0,np.sqrt(efficiency),0, 0],
				   [0,0,				  1.,0],
				   [0,0,				  0, 1.0]])

	return mm

class SpherePolarizers(MuellerMat.MuellerMatrix):
	'''
	A MuellerMat.MuellerMatrix child class for the sphere HWP
	'''
	def __init__(self,name='Sphere_M4'):
		super(SpherePolarizers, self).__init__(sphere_polarizers_function,name=name)

def make_mm():
	'''
	A function that returns the system mueller matrix for SPHERE (based on Rob van Holstein's Masters thesis)
	'''

	#Initialize all the mueller matrices
	m_p = cmm.Rotator()
	m_p.name = 'SkyRotation'
	m_ut = SphereMUT()
	m_az = cmm.Rotator()
	m_az.name = 'TelescopeAlt'
	m_m4 = SphereM4()
	m_hwp = SphereHWP()
	m_der = SphereDerotator()
	m_cl = SpherePolarizers()

	mm_list = [m_cl,m_der,m_hwp,m_m4,m_az,m_ut,m_p]
	sphere_mm = MuellerMat.SystemMuellerMatrix(mm_list)

	return sphere_mm

