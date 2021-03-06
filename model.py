from conditional_laws import simul_alpha, simul_beta, simul_H, simul_K, simul_s_p, simul_s_T, simul_T
from conditional_laws_new import *
from conditional_laws_uncertain import *
import numpy as np

class variable:
    def __init__(self, name, value, var_type, true_value = None, law = None):
        self.name = name
        self.value = value
        self.law = law
        self.var_type = var_type
        if true_value is None:
            self.true_value = value
        else:
            self.true_value = true_value

    def __repr__(self):
        return('{} = {} \n'.format(self.name, self.value))

    def __call__(self):
        return self.value

class model:
    def __init__(self, params = {}, data = {}, constants = {}):
        self.params = params
        self.data = data
        self.constants = constants
        self.acc_H = 0
        self.acc_K = 0
        self.n_iteration = 0

    def __repr__(self):
        s = ''
        s += '\n Constants: \n'
        for key in self.constants.keys():
            s += self.constants[key].__repr__()
        s += '\n Parameters: \n'
        for key in self.params.keys():
            s += self.params[key].__repr__()
        s += '\n Data: \n'
        for key in self.data.keys():
            s += self.data[key].__repr__()
        return s

    def add(self, var):
        if type(var) != list:
            var = [var]
        for x in var:
            try:
                var_type = x.var_type
                dic = self.__getattribute__(var_type)
                name = x.name
                dic[name] = x
            except:
                print('No type defined for {}'.format(x))


    def delete(self, var):
        if type(var) != list:
            var = [var]
        for x in var:
            try:
                dic = self.__getattribute__(x.var_type)
                del dic[x.name]
            except:
                print('Impossible to delete {}'.format(x.name))


    def eval(self, key):
        if key in self.params.keys():
            return self.params[key].law(self)

class PaleoModel(model):
    def __init__(self, t1, t2, t3, t4, S, V, C, T2, RP, H_init = 0.5, K_init = 0.5, step_H = 0.05, step_K = 0.05, n_iterations_MH = 100):
        past = variable(name='past', var_type='constants', value=t2-t1)
        present = variable(name='present', var_type='constants', value=t3-t1)
        future = variable(name='future', var_type='constants', value=t4-t1)
        step_H = variable(name='step_H', var_type='constants', value=step_H)
        step_K = variable(name='step_K', var_type='constants', value=step_K)
        n_iteration = variable(name='n_iteration', var_type='constants', value=n_iterations_MH)

        alpha = variable(name='alpha', var_type='params', value=np.array([0,1]), law = simul_alpha)
        beta = variable(name='beta', var_type='params', value=np.array([0,1,1,1]),law = simul_beta)
        sigma_p = variable(name='sigma_p', var_type='params', value=1, law = simul_s_p)
        sigma_T = variable(name='sigma_T', var_type='params', value=1, law = simul_s_T)

        H = variable(name='H', var_type='params', value=H_init, law = simul_H)
        K = variable(name='K', var_type='params', value=K_init, law = simul_K)
        T13 = variable(name='T13', var_type='params', value=np.zeros(past()+future()-present()),law = simul_T)

        self.t1 = t1
        self.t2 = t2
        self.t3 = t3
        self.t4 = t4
        # Init with true values
        # alpha = variable(name='alpha', var_type='params', value=np.array([-0.19,0.4]), law = simul_alpha)
        # beta = variable(name='beta', var_type='params', value=np.array([-0.57,0.02,-0.02,0.15]),law = simul_beta)
        # sigma_p = variable(name='sigma_p', var_type='params', value=0.007, law = simul_s_p)
        # sigma_T = variable(name='sigma_T', var_type='params', value=0.015, law = simul_s_T)
        # H = variable(name='H', var_type='params', value=H_init, law = simul_H)
        # K = variable(name='K', var_type='params', value=K_init, law = simul_K)
        # T13 = variable(name='T13', var_type='params', value=np.load('T13.npy'),law = simul_T)

        T2 = variable(name='T2', var_type='data', value = T2)
        RP = variable(name ='RP', var_type='data', value=RP)
        S = variable(name ='S', var_type='data', value=S)
        V = variable(name ='V', var_type='data', value=V)
        C = variable(name ='C', var_type='data', value=C)

        super().__init__()
        self.add([past, present, future, step_H, step_K, n_iteration, alpha, beta, sigma_p, sigma_T, H, K, T13, T2, RP, S, V, C])

class PaleoModel2(model):
    def __init__(self, t1, t2, t3, t4, S, V, C, T2, RP, H_init = 0.5, K_init = 0.5, step_H = 0.05, step_K = 0.05, n_iterations_MH = 100, T13=None):
        past = variable(name='past', var_type='constants', value=t2-t1)
        present = variable(name='present', var_type='constants', value=t3-t1)
        future = variable(name='future', var_type='constants', value=t4-t1)
        step_H = variable(name='step_H', var_type='constants', value=step_H)
        step_K = variable(name='step_K', var_type='constants', value=step_K)
        n_iteration = variable(name='n_iteration', var_type='constants', value=n_iterations_MH)

        alpha = variable(name='alpha', var_type='params', value=np.array([0,1]), law = simul_alpha2)
        beta = variable(name='beta', var_type='params', value=np.array([5,0.5,-0.5,2]),law = simul_beta2)
        sigma_p = variable(name='sigma_p', var_type='params', value=1, law = simul_s_p2)
        sigma_T = variable(name='sigma_T', var_type='params', value=1, law = simul_s_T2)

        H = variable(name='H', var_type='params', value=H_init, law = simul_H2)
        K = variable(name='K', var_type='params', value=K_init, law = simul_K2)
        T13 = variable(name='T13', var_type='params', value=np.zeros(t4-t3 + t2-t1),law = simul_T2)
        # T13 = variable(name='T13', var_type='params', value=T13,law = simul_T2)

        self.t1 = t1
        self.t2 = t2
        self.t3 = t3
        self.t4 = t4
        # Init with true values
        # alpha = variable(name='alpha', var_type='params', value=np.array([-0.19,0.4]), law = simul_alpha)
        # beta = variable(name='beta', var_type='params', value=np.array([-0.57,0.02,-0.02,0.15]),law = simul_beta)
        # sigma_p = variable(name='sigma_p', var_type='params', value=0.007, law = simul_s_p)
        # sigma_T = variable(name='sigma_T', var_type='params', value=0.015, law = simul_s_T)
        # H = variable(name='H', var_type='params', value=H_init, law = simul_H)
        # K = variable(name='K', var_type='params', value=K_init, law = simul_K)
        # T13 = variable(name='T13', var_type='params', value=np.load('T13.npy'),law = simul_T)

        T2 = variable(name='T2', var_type='data', value = T2)
        RP = variable(name ='RP', var_type='data', value=RP)
        S = variable(name ='S', var_type='data', value=S)
        V = variable(name ='V', var_type='data', value=V)
        C = variable(name ='C', var_type='data', value=C)

        super().__init__()
        self.add([past, present, future, step_H, step_K, n_iteration, alpha, beta, sigma_p, sigma_T, H, K, T13, T2, RP, S, V, C])

class PaleoModel3(model):
    """
    Same as PaleoModel2, but we now include random variability in the forcing prediction.
    Most of the simulation laws are the same so we only rewrite a few of them in the new laws file.
    """
    def __init__(self, t1, t2, t3, t4, S, V, V_spike, C, C_var, T2, RP, H_init = 0.5, K_init = 0.5, step_H = 0.05, step_K = 0.05, n_iterations_MH = 100, T13=None):
        past = variable(name='past', var_type='constants', value=t2-t1)
        present = variable(name='present', var_type='constants', value=t3-t1)
        future = variable(name='future', var_type='constants', value=t4-t1)
        step_H = variable(name='step_H', var_type='constants', value=step_H)
        step_K = variable(name='step_K', var_type='constants', value=step_K)
        n_iteration = variable(name='n_iteration', var_type='constants', value=n_iterations_MH)

        alpha = variable(name='alpha', var_type='params', value=np.array([0,1]), law = simul_alpha2)
        beta = variable(name='beta', var_type='params', value=np.array([5,0.5,-0.5,2]),law = simul_beta3)
        sigma_p = variable(name='sigma_p', var_type='params', value=1, law = simul_s_p2)
        sigma_T = variable(name='sigma_T', var_type='params', value=1, law = simul_s_T3)

        H = variable(name='H', var_type='params', value=H_init, law = simul_H2)
        K = variable(name='K', var_type='params', value=K_init, law = simul_K2)
        T13 = variable(name='T13', var_type='params', value=np.zeros(t4-t3 + t2-t1),law = simul_T3)
        # T13 = variable(name='T13', var_type='params', value=T13,law = simul_T2)

        self.t1 = t1
        self.t2 = t2
        self.t3 = t3
        self.t4 = t4
        # Init with true values
        # alpha = variable(name='alpha', var_type='params', value=np.array([-0.19,0.4]), law = simul_alpha)
        # beta = variable(name='beta', var_type='params', value=np.array([-0.57,0.02,-0.02,0.15]),law = simul_beta)
        # sigma_p = variable(name='sigma_p', var_type='params', value=0.007, law = simul_s_p)
        # sigma_T = variable(name='sigma_T', var_type='params', value=0.015, law = simul_s_T)
        # H = variable(name='H', var_type='params', value=H_init, law = simul_H)
        # K = variable(name='K', var_type='params', value=K_init, law = simul_K)
        # T13 = variable(name='T13', var_type='params', value=np.load('T13.npy'),law = simul_T)
        
        T2 = variable(name='T2', var_type='data', value = T2)
        RP = variable(name ='RP', var_type='data', value=RP)
        
        # The constant values are not normalized nor transformed
        S_cst = variable(name ='S_cst', var_type='data', value=S)
        V_cst = variable(name ='V_cst', var_type='data', value=V)
        V_spike = variable(name ='V_spike', var_type='data', value=V_spike)
        C_cst = variable(name ='C_cst', var_type='data', value=C)
        C_var = variable(name ='C_var', var_type='data', value=C_var)
        
        V = np.log(1-V)
        C = np.log(C)
        S = (S - S[:present()].mean())/S[:present()].std()
        V = (V - V[:present()].mean())/V[:present()].std()
        C = (C - C[:present()].mean())/C[:present()].std()
        
        # The param values are normalized and transformed
        S = variable(name ='S', var_type='params', value=S, law=simul_S3)
        V = variable(name ='V', var_type='params', value=V, law=simul_V3)
        C = variable(name ='C', var_type='params', value=C, law=simul_C3)

        super().__init__()
        self.add([past, present, future, step_H, step_K, n_iteration, alpha, beta, sigma_p, sigma_T, H, K, T13, T2, RP, S, V, C, S_cst, V_cst, C_cst, V_spike, C_var])
