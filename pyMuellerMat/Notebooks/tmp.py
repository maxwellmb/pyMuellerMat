

def model(x,sys_mm,hwp_angles, imrot_angles):


    flc.properties['phi'] = 2*np.pi*x[0] #Pick your FLC retardance here. ##FREE PARAMETER
    flc.properties['theta'] = 0. ##FREE PARAMETER



    double_diff = 
    double_summ = 

    return double_diff, double_summ

def residuals(x,data,sym_mm,hwp_angles,etc....):
    

   resid = model(x) - data
   return resid

def logl(x,data,.....):
    

    residuals
    ....

    return x


first_guess_x = []

first_guess_model = model(x)

plot_first_guess()

emcee_fitting()