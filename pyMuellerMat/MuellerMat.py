'''
The main body of the code that contains all the class definitions

'''

import inspect
from pyMuellerMat import common_mm_functions
import copy
import numpy as np


class MuellerMatrix(object):
    '''
    A mueller matrix whose main function is 'evaluate' that returns a 4x4 mueller matrix.

    All MuellerMatrix objects will have a 'theta' argument that will rotate the matrix by theta.

    This mueller matrix class differs from the SystemMuellerMatrix class
    #TODO: Define all the sign conventions.

    '''

    def __init__(self, mueller_matrix_function, name=None):
        '''
        Initializing the object - all that you need to pass in is the mueller_matrix_function.
        The function should have no arguments, but can have keyword arguments and it should return an array of size [4,4].
        The keyword arguments will be automatically detected and stored in the the property_list property.
        Two rotational parameters will be appended to the property_list: 'theta' and 'delta_theta'.
        They will be added together to form the total rotation angle. We define them both, so that we can include 
        a fixed offset on top of a rotating optic. 

        Class properties:

        name 	       -    A string that is used to describe this object
        function       -    A python function that returns a 4x4 mueller matrix. It must not have any arguments, but can have keyword arguments.
        property_list     -    A list of keyword arguments for the 'function'
        property_defaults -    The default values for the function's keywords
        default_propertys -    A dictionary of the default keyword arguments for the function (Aside: Could consider just making this a function rather than a property)
        default_mm     -    A 4x4 mueller matrix that is evaluated using the default_propertys
        propertys          -    A dictionary of propertys representing the user's current inputs
        mm             -    A 4x4 mueller matrix that was generated by evaluating the 'function' with the current 'propertys'
        '''

        # Give this mueller matrix a name.
        self.name = name

        # Assign the function to the object.
        self.function = mueller_matrix_function

        # TODO: Perhaps make a check so the function has no arguments (but can have keyword arguments)

        # Get the function's keyword arguments - I found this example of how to do this here: https://stackoverflow.com/questions/11915032/get-keyword-arguments-for-function-python
        # TODO: There may be a python 3 compatability problem here.
        argspec = inspect.getargspec(self.function)

        if argspec.defaults is not None:
            self.property_list = argspec.args[-len(argspec.defaults):]
            self.property_defaults = [arg for arg in argspec.defaults[-len(
                argspec.defaults):]]  # The output is a tuple, so we need to do it this way.
        else:
            self.property_list = []
            self.property_defaults = []

        # Add 'theta' the rotation value. All mueller matrices are rotatable.
        self.property_list.insert(0, 'theta')
        self.property_defaults.insert(0, 0.)

        # Add 'delta_theta' the rotational offset value. All mueller matrices might have an offset.
        self.property_list.insert(0, 'delta_theta')
        self.property_defaults.insert(0, 0.)

        # TODO: Get the property default values.
        self.default_property_dict = {}
        for i, kwarg in enumerate(self.property_list):
            self.default_property_dict[kwarg] = self.property_defaults[i]

        # Copy this to the working propertys property
        self.properties = copy.deepcopy(self.default_property_dict)

        # TODO: Run some test to make sure that the output of the function is a 4x4 array

        # Evaluate the mueller matrix based on the defaults and store it in self.mm
        self.default_mm = self.evaluate()
        self.mm = copy.deepcopy(self.default_mm)

    def evaluate(self):
        '''
        Evaluate the function to obtain a 4x4 mueller matrix.
        This function updates current values of self.properties

        Inputs:
        theta	-	The rotation angle to apply in degrees
        '''

        # TODO: Update self.properties with the new properties that have been passed. Not all properties have to be updated.

        function_properties = copy.deepcopy(self.properties)
        theta = function_properties.pop('theta') + function_properties.pop('delta_theta')
        
        # Evaluate the function with all the properties
        mm = self.function(**function_properties)

        # if theta != 0: Apply a rotation
        if theta != 0:
            mm = np.matmul(np.matmul(common_mm_functions.rotator_function(-theta), mm),
                           common_mm_functions.rotator_function(theta))

        # Update the object's mm property
        self.mm = mm

        # Return the mueller matrix
        return mm

    def invert():
        '''
        A function that returns the inverse of the current mueller matrix, self.mm
        '''


class SystemMuellerMatrix(object):
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

        # Make a master list of keyword arguments for all the functions. Each keyword will be prefixed by M$_, where $ corresponds to the position of the given matrix in the list.
        self.master_property_dict = {}

        # A list of names
        self.names = []

        # The list of mueller matrices
        self.mueller_matrix_list = mueller_matrix_list

        # Step through the mueller matrices and build the keyword list
        for i, mm in enumerate(self.mueller_matrix_list):

            # Get the name of each mueller matrix. If there is no name then assign M$_, where $ corresponds to the position of the given matrix in the list.
            if mm.name is not None:
                name = mm.name
            else:
                name = "M{}".format(i)

            # Add each properties dictionary to the master dictionary
            self.master_property_dict[name] = mm.properties

            # Append this mm's name to the master list.
            self.names.append(name)

        # Make a mueller matrix for all the default parameters
        self.default_mm = self.evaluate()

        # Put the default mueller matrix in the 'current' mueller matrix
        self.mm = copy.deepcopy(self.default_mm)

    def evaluate(self, new_property_dict=None):
        '''
        Compute the system mueller matrix by evaluating each individual mueller matrix based on the keyword dictionary, property_dict.
        property_dict will be a nested dictionary of the form {'M0': {'property1': value, 'property2': value}, 'M1': {'property1': value, 'property2': value}, etc},
        where M0 and M1 are the names of the first and second mueller matrices and 'property1' and 'property2' represent the keywords needed for their respective functions
        and may vary in actual name between the two functions.
        '''

        # Update the property dicts based on the new_property_dict if it exists
        if new_property_dict is not None:

            # TODO: Put in some sort of check to make sure that the
            # new_property_dict is in the right format

            # Get the names of the mueller matrices
            mm_names = new_property_dict.keys()
            # Cycle through the mueller matrices and update their components
            for mm_name in mm_names:
                # If we have a correct mueller matrix then update the parameters.
                if mm_name in self.master_property_dict:

                    # Now do the same things with the keywords
                    mm_keys = new_property_dict[mm_name].keys()
                    for mm_key in mm_keys:
                        if mm_key in self.master_property_dict[mm_name].keys():
                            # Update the keyword!
                            self.master_property_dict[mm_name][mm_key] = new_property_dict[mm_name][mm_key]

        # The number of mueller matrices in the list
        n_mms = len(self.mueller_matrix_list)

        # Start off with an identity matrix
        mm = np.eye(4)

        # Cycle through the mueller matrices and multiply them together
        # for i in range(n_mms):
        #     properties = self.master_property_dict[self.names[-i]]
        #     self.mueller_matrix_list[-i].properties = properties
        #     new_mm = self.mueller_matrix_list[-i].evaluate()
        #     mm = np.matmul(mm, new_mm)
        #     # mm = np.matmul(new_mm,mm)

        for i in range(n_mms):
            properties = self.master_property_dict[self.names[i]]
            self.mueller_matrix_list[i].properties = properties
            new_mm = self.mueller_matrix_list[i].evaluate()
            # mm = np.matmul(mm, new_mm)
            mm = mm@new_mm
            # mm = np.matmul(new_mm,mm)

        self.mm = mm

        return mm

    def invert():
        '''
        A function that returns the inverse of the current mueller matrix, self.mm
        '''

    def print_properties():
        '''
        Print out all the property arguments.
        Maybe format it nicely so the keywoords go along well with
        '''

        # print(self.master_property_list)

# class MeasurementMatrix:
# 	'''
# 	This is a similar structure to how we evaluate GPI data.
# 	'''

# 	def ___init___(self, M_sys):
