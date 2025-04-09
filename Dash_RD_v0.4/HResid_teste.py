# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 15:47:29 2020

@author: carol
"""

import numpy as np


###############################################################################

class Param_EoS ():
    
    ###########################################################################
    
    def __init__(self, T, P, y, EoS): 
        
        # self.R = R
        self.T = T
        self.P = P
        self.y = y
        self.EoS = EoS
        
        # Número de componentes #
        self.Nc = np.size(self.y)   
        
        self.R = 8.314462                # J/mol/K [constante dos gases]
                    # C1	   C2	   C3	   n-C6	n-C7	n-C8	CO2	   i-C4	i-C5	N2	   n-C4	n-C5
        self.Tc = np.array([190.6, 305.3,	369.8,	507.6,	540.2,	568.7,	304.2,	408.1,	460.4,	126.2,	425.1,	469.7]) # Temperatura crítica [K]
        self.Pc = np.array([45.99, 48.72,	42.48,	30.25,	27.40,	24.90,	73.83,	36.48,	33.90,	34.00,	37.96,	33.70]) # Pressão crítica [bar]
        self.Vc = np.array([98.6,  145.5,	200.0,	371.0,	428.0,	486.0,	94.0,	262.7,	306.0,	89.2,	255.0,	313.0]) # Volume molar crítico [cm^3/mol]
        self.Zc = np.array([0.286, 0.279,	0.276,	0.266,	0.261,	0.256,	0.274,	0.282,	0.227,	0.289,	0.274,	0.270]) # Fator de compressibilidade crítico
        self.w = np.array([ 0.012, 0.100,	0.152,	0.301,	0.350,	0.400,	0.224,	0.181,	0.227,	0.038,	0.200,	0.252]) # Fator acêntrico
        
        if self.EoS == 'PR':
            ' Parâmetros Peng-Robinson '
            # Parâmetro binário da mistura #
            self.kij = np.zeros((self.Nc,self.Nc))
                                     # C1	      C2	    C3	     n-C6	     n-C7	    n-C8	     CO2	    i-C4	    i-C5	    N2	      n-C4	 n-C5
            self.kij[0,:] = np.array([    0.0,  -0.0026,  0.014,  0.0422,   0.0352,  0.0496,  0.0919,   0.0256,  -0.0056, 0.0311,   0.0133,  0.023])   #C1
            self.kij[1,:] = np.array([-0.0026,      0.0, 0.0011,   -0.01,   0.0067,  0.0185,  0.1322,  -0.0067,      0.0, 0.0515,   0.0096,  0.0078])  #C2
            self.kij[2,:] = np.array([  0.014,   0.0011,    0.0,  0.0007,   0.0056,     0.0,  0.1241,  -0.0078,   0.0111, 0.0852,   0.0033,  0.0267])  #C3
            self.kij[3,:] = np.array([ 0.0422,    -0.01, 0.0007,     0.0,  -0.0078,     0.0,    0.11,      0.0,      0.0, 0.1496,  -0.0056,  0.0])     #C6
            self.kij[4,:] = np.array([ 0.0352,   0.0067, 0.0056, -0.0078,      0.0,     0.0,     0.1,      0.0,      0.0, 0.1441,   0.0033,  0.0074])  #C7
            self.kij[5,:] = np.array([ 0.0496,   0.0185,    0.0,     0.0,      0.0,     0.0,     0.0,      0.0,      0.0,  -0.41,      0.0,  0.0])     #C8
            self.kij[6,:] = np.array([ 0.0919,   0.1322, 0.1241,    0.11,      0.1,     0.0,     0.0,     0.12,   0.1219, -0.017,   0.1333,  0.1222])  #CO2
            self.kij[7,:] = np.array([ 0.0256,  -0.0067,-0.0078,     0.0,      0.0,     0.0,    0.12,      0.0,      0.0, 0.1033,  -0.0004,  0.0])     #iC4
            self.kij[8,:] = np.array([-0.0056,      0.0, 0.0111,     0.0,      0.0,     0.0,  0.1219,      0.0,      0.0, 0.0922,  0.00292,  0.0])     #iC5
            self.kij[9,:] = np.array([ 0.0311,   0.0515, 0.0852,  0.1496,   0.1441,   -0.41,  -0.017,   0.1033,   0.0922,    0.0,     0.08,  0.1])     #N2
            self.kij[10,:] = np.array([0.0133,   0.0096, 0.0033, -0.0056,   0.0033,     0.0,  0.1333,  -0.0004,  0.00292,   0.08,      0.0,  0.0174])  #nC4
            self.kij[11,:] = np.array([ 0.023,   0.0078, 0.0267,     0.0,   0.0074,     0.0,  0.1222,      0.0,      0.0,    0.1,   0.0174,  0.0])     #nC5
        
            # Parâmetros da EoS # 
            self.delta = 1 + 2**(1/2)
            self.epsilon = 1 - 2**(1/2)
            self.omega = 0.07780
            self.psi = 0.45724
        
        elif self.EoS == 'SRK':
            ' Parâmetros SRK '
            # Parâmetro binário da mistura #
            self.kij = np.zeros((self.Nc,self.Nc))
                                     # C1	      C2	     C3	    n-C6	    n-C7	   n-C8	    CO2	  i-C4	      i-C5	   N2	     n-C4	    n-C5
            self.kij[0,:] = np.array([     0.0,  0.00042, 0.02415, 0.02207,  -0.0065, 0.09582,     0.0, 0.04607,  0.09351,    0.0,  0.02264,  0.01581])  #C1
            self.kij[1,:] = np.array([ 0.00042,      0.0, 0.00169, -0.0433,  0.01800, -0.1550,     0.0, 0.00551,      0.0,    0.0,  0.00532,  0.01425])  #C2
            self.kij[2,:] = np.array([ 0.02415,  0.00169,     0.0, 0.00305,  0.03611, 0.00530,     0.0, -0.0029,  0.00306,    0.0,  -0.0021, -0.0043])   #C3
            self.kij[3,:] = np.array([ 0.02207,  -0.0433, 0.00305,     0.0,  0.00211,     0.0,     0.0,     0.0,      0.0,    0.0,   0.0124,  0.0])      #C6
            self.kij[4,:] = np.array([ -0.0065,  0.01800, 0.03611, 0.00211,      0.0, 0.00749,     0.0,     0.0,      0.0,    0.0,  -0.0069,  0.01587])  #C7
            self.kij[5,:] = np.array([  0.0496,   0.0185,     0.0,     0.0,      0.0,     0.0,     0.0,     0.0,      0.0,  -0.41,      0.0,  0.0])      #C8
            self.kij[6,:] = np.array([     0.0,      0.0,     0.0,     0.0,      0.0,     0.0,     0.0,     0.0,      0.0,    0.0,      0.0,  0.0])      #CO2
            self.kij[7,:] = np.array([ 0.04607,  0.00551, -0.0029,     0.0,      0.0,     0.0,     0.0,     0.0,      0.0,    0.0,  -0.0038,  0.0])      #iC4
            self.kij[8,:] = np.array([ 0.09351,      0.0, 0.00306,     0.0,      0.0,     0.0,     0.0,     0.0,      0.0,    0.0,  0.00783,  0.0])      #iC5
            self.kij[9,:] = np.array([     0.0,      0.0,     0.0,     0.0,      0.0,     0.0,     0.0,     0.0,      0.0,    0.0,      0.0,  0.0])      #N2
            self.kij[10,:] = np.array([0.02264,  0.00532, -0.0021,  0.0124,  -0.0069, 0.00416,     0.0, -0.0038,  0.00783,    0.0,      0.0,  0.0382])   #nC4
            self.kij[11,:] = np.array([0.01581,  0.01425, -0.0043,     0.0,  0.01587, -0.0023,     0.0,     0.0,      0.0,    0.0,   0.0382,  0.0])      #nC5   
        
            # Parâmetros da EoS # 
            self.delta = 1
            self.epsilon = 0
            self.omega = 0.08664
            self.psi = 0.42748
            
        else:
            ' Parâmetros RK '
            # Parâmetro binário da mistura #
            self.kij = np.zeros((self.Nc,self.Nc))
        
            # Parâmetros da EoS # 
            self.delta = 1
            self.epsilon = 0
            self.omega = 0.08664
            self.psi = 0.42748
                
    ###########################################################################

    def Mistura (self):
        
        # Alocação de variáveis #
        self.Tcij = np.zeros((self.Nc,self.Nc))
        self.Zcij = np.zeros((self.Nc,self.Nc))
        self.Vcij = np.zeros((self.Nc,self.Nc))
        self.Pcij = np.zeros((self.Nc,self.Nc))
        self.wij = np.zeros((self.Nc,self.Nc))
        self.Tci = np.zeros(self.Nc)
        self.Pci = np.zeros(self.Nc)
        self.wi = np.zeros(self.Nc)
        
        ''' Calcula parâmetros da mistura '''        

        for i in range(self.Nc):
            for j in range(self.Nc):            
                self.Tcij[i,j] = np.sqrt(self.Tc[i]*self.Tc[j])*(1-self.kij[i,j]) 
                self.Zcij[i,j] = (self.Zc[i] + self.Zc[j]) / 2      
                self.Vcij[i,j] = ((self.Vc[i]**(1/3) + self.Vc[j]**(1/3)) / 2)**3      
                self.Pcij[i,j] = self.Zcij[i,j]*self.R*self.Tcij[i,j] / self.Vcij[i,j]      
                self.wij[i,j] = (self.w[i] + self.w[j]) / 2      

                self.Tci[i] = np.dot(np.dot(self.y[i],self.y),self.Tcij[i,:])
                self.Pci[i] = np.dot(np.dot(self.y[i],self.y),self.Pcij[i,:])
                self.wi[i] = np.dot(np.dot(self.y[i],self.y),self.wij[i,:])

        # Parâmetros da mistura #                
        self.Tcm = np.sum(self.Tci)
        self.Pcm = np.sum(self.Pci)
        self.wm = np.sum(self.wi)
        
        return self.Tcm, self.wm
            

###############################################################################
        
class EoS_mistura ():
    
    ###########################################################################
    
    def __init__(self, param, Tcm, wm, EoS):
       
        # Parâmetros de entrada #
        self.R = param.R
        self.P = param.P
        self.y = param.y
        self.T = param.T
        self.Tc = param.Tc
        self.Pc = param.Pc
        self.w = param.w
        self.Nc = param.Nc
        self.omega = param.omega
        self.psi = param.psi
        self.Tcm = Tcm
        self.wm = wm
        self.EoS = EoS
        
        # Alocação de variáveis #
        self.aij = np.zeros((self.Nc,self.Nc))
        self.at = np.zeros(self.Nc)
        self.temp = np.zeros((self.Nc,self.Nc))
        self.api = np.zeros(self.Nc)
        self.ai = np.zeros(self.Nc)
        self.bi = np.zeros(self.Nc)
       
    ###########################################################################
    
    def AB (self):
                
        # Temperatura reduzida (K) #
        self.Tr = self.T/self.Tc
        self.Trm = self.T/self.Tcm
                
        ''' Calcula parâmetros da Equação de Estado '''
        
        if self.EoS == 'PR': 
            # Peng-Robinson (PR) #
            kappai = 0.37464 + 1.54226*self.w - 0.26992*self.w**2
            alphai = (1 + kappai*(1 - np.sqrt(self.Tr)))**2  
            self.kappa = 0.37464 + 1.54226*self.wm - 0.26992*self.wm**2
            self.alpha = (1 + self.kappa*(1 - np.sqrt(self.Trm)))**2 

            for i in range(self.Nc):
        
                # Peng-Robinson (PR) #
                self.ai[i] = self.psi*self.R**2*np.divide(np.dot(alphai[i], self.Tc[i]**2),self.Pc[i])
                self.bi[i] = self.omega*self.R*np.divide(self.Tc[i],self.Pc[i])
                
        elif self.EoS == 'SRK':
            # Soave/Redlich/Kwong (SRK) #
            kappai = 0.480 + 1.574*self.w - 0.176*self.w**2
            alphai = (1 + kappai*(1 - np.sqrt(self.Tr)))**2        
            self.kappa = 0.480 + 1.574*self.wm - 0.176*self.wm**2
            self.alpha = (1 + self.kappa*(1 - np.sqrt(self.Trm)))**2        

            for i in range(self.Nc):
        
                # Soave/Redlich/Kwong (SRK) #
                self.ai[i] = self.psi*self.R**2*np.divide(np.dot(alphai[i], self.Tc[i]**2),self.Pc[i])
                self.bi[i] = self.omega*self.R*np.divide(self.Tc[i],self.Pc[i])
        else:
           
            self.kappa = 0
            self.alpha = 0       

            for i in range(self.Nc):

                # Redlich/Kwong (RK)  #
                self.ai[i] = self.psi*self.R**2*np.divide(np.dot(self.Tr[i]**(-1/2),self.Tc[i]**2),self.Pc[i])
                self.bi[i] = self.omega*self.R*np.divide(self.Tc[i],self.Pc[i])

        ''' Calcula parâmetros da mistura '''               
        for i in range(self.Nc):
            for j in range(self.Nc):            
                self.aij[i,j] = np.sqrt(self.ai[i]*self.ai[j])      
                
                self.at[i] = np.dot(np.dot(self.y[i],self.y),self.aij[i,:])        
                
                # Partes do cálculo de a parcial #
                self.temp[i,j] = 2*self.y[j]*self.aij[i,j]
                self.api[i] = np.sum(self.temp[i,:])
        
        self.a = np.sum(self.at)
        self.b = np.sum(np.dot(self.y,self.bi))
        
        ''' Calcula parâmetros do fator de compressibilidade '''
        self.q = self.a/(self.b*self.R*self.T)
        self.beta = self.b*self.P/(self.R*self.T)
        
        return self.q, self.beta, self.kappa, self.alpha
    
    
###############################################################################
        
class HR ():
    
    ###########################################################################

    def __init__(self, param, EoS_mistura, EoS):
                
        # Instancia parâmetros #
        self.delta = param.delta
        self.epsilon = param.epsilon
        self.P = param.P
        self.R = param.R
        self.y = param.y
        self.Nc = param.Nc
        self.T = param.T
        self.Tcm = EoS_mistura.Tcm
        
        # Instancia classe #
        self.EoS_mistura = EoS_mistura
        self.EoS = EoS

    ###########################################################################
    
    def run (self):
        
        # Temperatura reduzida #
        self.Trm = self.T/self.Tcm
        
        # Resolve parâmetros de PR #
        self.q, self.beta, self.kappa, self.alpha = self.EoS_mistura.AB()
        
        ''' Calcula fator de compressibilidade '''
        # c3*z**3 + c2*z**2 + c1*z + c0 = 0
        
        # Calcula coeficientes do cálculo do fator de compressibilidade #        
        if self.EoS == 'PR':
            # PR #
            c3 = 1.0
            c2 = - (1 - self.beta)
            c1 = self.q*self.beta - 3*self.beta**2 - 2*self.beta
            c0 = - (self.q*self.beta**2 - self.beta**2 - self.beta**3)
            
        else:
            # RK e SRK #
            c3 = 1.0
            c2 = - 1.0
            c1 = - (self.beta + self.beta**2 - self.q*self.beta)
            c0 = - (self.q*self.beta**2 )           
        
        # Resolve eq. cúbica do fator de compressibilidade #
        coef = [float(np.squeeze(c)) for c in [c3, c2, c1, c0]]
        self.sol = np.roots(coef)
        # self.sol = np.roots([c3,c2,c1,c0])          

        # O fator de compressibilidade do vapor deve ser a maior raíz e o do 
        # líquido deve ser a menor raíz
        self.Z = np.max(np.real(self.sol))        # Fator de compressibilidade do vapor

        I = (1/(self.delta - self.epsilon))*np.log((self.Z + self.delta*self.beta)/(self.Z + self.epsilon*self.beta))
                    
        if self.EoS == 'PR' or self.EoS == 'SRK':
            self.dalfa = - self.kappa*(self.Trm/self.alpha)**(1/2)

        else:
            self.dalfa = -1/2
        
        # Entalpia residual #            
        self.HR = self.R*self.T*(self.Z - 1 + (self.dalfa - 1)*self.q*I)
        
        # print(self.HR)
                    
        return self.HR
        
        
