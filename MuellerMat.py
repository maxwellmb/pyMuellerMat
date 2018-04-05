import inspect

class MuellerMatrix:
	'''
	A mueller matrix whose main function is 'evaluate' that returns a 4x4 mueller matrix. 

	All MuellerMatrix objects will have a 'theta' argument that will rotate the matrix by theta. 

	#TODO: Define all the sign conventions. 

	'''

	def __init__(self,mueller_matrix_function, name = None):
		'''
		Initializing the object - all that you need to pass in the mueller_matrix_function. 
		The function should have no arguments, but can have keyword arguments and it should return an array of size [4,4]. 
		'''

		#Give this mueller matrix a name. 
		self.name = None
		
		#Assign the function to the object. 
		self.function = mueller_matrix_function

		#Perhaps make a check so the function has no arguments (but can have keyword arguments)

		#Get the function's keyword arguments - I found this example of how to do this here: https://stackoverflow.com/questions/11915032/get-keyword-arguments-for-function-python
		#There may be a python 3 compatability thing here. 
		argspec = inspect.getargspec(thefunction)
		self.kwarg_list = argspec.args[-len(argspec.defaults):]

		#Get the kwarg defaults. 
		self.kwarg_defaults = 

		#Add 'theta' the rotation value. All mueller matrices are rotatable. 
		sefl.kwarg_list.insert(0,'theta')

		#Run some test to make sure that the output of the function is a 4x4 array

	def evaluate(theta=0,**kwargs):
		'''
		Evaluate the function to obtain a 4x4 mueller matrix
		'''

		#Check that all the required kwargs have been supplied. 

		#Evaluate the function with all the kwargs

		#if theta != 0: Apply a rotation 

		# return a 4x4 mueller matrix


class SystemMuellerMatrix:
	'''
	This is an object that represents the mueller matrix for a given system. 
	It will typically be made up of one or more other mueller matrices.
	'''

	def __init__(self, mueller_matrix_list=[]):
		'''
		The initialization accepts a list of MuellerMatrix objects. 
		They will eventually be evaluated as: 

			S_out = M0 * M1 * M2 * .... * M_n * S_in
		'''

		#Make a master list of keyword arguments for all the functions. Each keyword will be prefixed by M$_, where $ corresponds to the position of the given matrix in the list. 
		self.master_kwarg_dict = {}

		#The list of mueller matrices
		self.mueller_matrix_list=mueller_matrix_list
		
		#Step through the mueller matrices and build the keyword list
		for i,mm in enumerate(self.mueller_matrix_list):
			if mm.name is not None:
				name = mm.name
			else name = "M{}".format(i)

			self.master_kwarg_dict[name] = mm.kwarg_list

			self.names.append(name)
		

	def evaluate(kwarg_dict):
		'''
		Compute the system mueller matrix by evaluating each individual mueller matrix based on the keyword dictionary, kwarg_dict. 
		kwarg_dict will be a nested dictionary of the form {'M0': {'kwarg1': value, 'kwarg2': value}, 'M1': {'kwarg1': value, 'kwarg2': value}, etc}, 
		where M0 and M1 are the names of the first and second mueller matrices and 'kwarg1' and 'kwarg2' represent the keywords needed for their respective functions 
		and may vary in actual name between the two functions. 
		'''

		#For each mueller matrix:
		 # get the appropriate nested dictionary from kwarg_dict

	def print_kwargs():
		'''
		Print out all the kwarg arguments. 
		Maybe format it nicely so the keywoords go along well with 
		'''

		# print(self.master_kwarg_list)

		


class MeasurementMatrix: 
	'''
	This is a similar structure to how we evaluate GPI data. 
	'''

	def ___init___(self, M_sys):



		












