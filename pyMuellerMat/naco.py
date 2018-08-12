import numpy as np
import common_mm_functions as cmf
import common_mms as cmm
import MuellerMat


def naco_function_mmb(ip_q = 0, ip_u=0, u_eff=0.93,uq_crosstalk = -0.2 ):
	'''
	A function that describes naco's Mueller Matrix in front of the HWP. 
	
	Here, by default we assume the instrumental polarization has been subtracted. 

	Keyword arguments: 
	pa           - the parallactic angle, in degrees
	ip_q		 - the Q instrumental polarization
	ip_u		 - the U instrumental polarization. 
	u_eff        - the Stokes U efficiency, in the instrument frame
	uq_crosstalk - the u to q crosstalk in the instrument frame
	'''

	mm_naco = np.array([[1,    0, 0,            0],
					   [ip_q, 1, uq_crosstalk, 0],
					   [ip_u,  0, u_eff,       0],
					   [0,    0, 0,            1]])

	return mm_naco


class NACO_mmb(MuellerMat.MuellerMatrix):
	'''
	A MuellerMat.MuellerMatrix child class for NACO in front of the HWP.
	'''
	def __init__(self,name="NACO"):
		super(NACO_mmb,self).__init__(naco_function_mmb, name=name)

def make_mm_mmb():
	'''
	A function that returns the system mueller matrix for NACO based on Max's Luhman 16 fitting
	'''

	m_naco = NACO_mmb() #The NACO Mueller Matrix
	m_p = cmm.Rotator()

	mm_list = [m_naco,m_p]

	naco_mm = MuellerMat.SystemMuellerMatrix(mm_list)

	return naco_mm


