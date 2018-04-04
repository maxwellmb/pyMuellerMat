

class MuellerMatrix:
	'''
	A mueller matrix whose main function is a function that returns a 4x4 mueller matrix
	'''

	def __init__(self,mueller_matrix_function,function_kwarg_names):
		'''
		Initializing the object
		'''
		self.function = mueller_matrix_function
		self.kwarg_names = function_kwarg_names

	def evaluate(**kwargs):
		'''
		'''

		for kwarg in kwarg_names:
			






class SystemMuellerMatrix:
	'''
	This is an object that represents the mueller matrix for a given system. 
	It will typically be made up of one or more other mueller matrices.
	'''

	def __init__(self, mueller_matrix_list=[]):
		'''
		The initialization accepts a list of MuellerMatrix objects
		'''
