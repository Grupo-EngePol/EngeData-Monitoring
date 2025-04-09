# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 01:45:49 2020

@author: diego
"""

import numpy as np
import pandas as pd
import datetime
import time
import logging


# Packages para rodar na Petrobras:
import sys
# import math
# import socket
# import pandaspi as pdpi
# import importlib
# import pandas_profiling

# To install this package with conda run one of the following: 
# conda install -c conda-forge dash
import dash
from dash import html, dcc
import plotly.graph_objs as go
# import plotly.express as px
from dash.dependencies import Input, Output

from scipy.stats import chi2
from collections import deque
from scipy.optimize import fsolve
from numpy.linalg import qr, inv, matrix_rank
from scipy.stats import median_abs_deviation as MAD
from HResid_teste import Param_EoS, EoS_mistura, HR

#%%
###############################################################################

class DataReconciliation ():
    
    ###########################################################################
    
    def __init__(self, Nvm, Nvu, nt):
        
        # Instancia variáveis de entrada #
        
        self.Nvm = Nvm
        self.Nvu = Nvu
        self.nc = int((self.Nvm + self.Nvu - 3 - 3)/3)
        self.nt = nt
        self.Ner = int(self.nc + 4)
        
        ''' Alocação de variável '''
        # Matrizes do modelo #
        self.E = np.zeros((self.Ner,1))
        self.Ay = np.zeros((self.Ner,self.Nvm))
        self.Au = np.zeros((self.Ner,self.Nvu))
        
        # Restrições na forma de resíduo [h(y,u)=0] #
        self.h = np.zeros((self.Ner,1))
        self.EBG_rec = np.zeros(self.nt)
        self.Et = np.zeros(self.nt)
        self.Erec = np.zeros(self.nt)
        
        # Matrizes da fatoração QR, Q=[Q1 Q2] #
        self.Q1 = np.zeros((self.Ner,self.Nvu))
        self.Q2 = np.zeros((self.Ner,self.Ner-self.Nvu))
        
        # Var não medida estimada no tempo #
        self.u_est = np.zeros((self.Nvu,self.nt))
        # Var reconciliada no tempo #
        self.y_rec = np.zeros((self.Nvm,self.nt))
        
    ###########################################################################

    def Model (self, nc, y, u):
        
        # Modelo em forma de vetor resíduo #
        # linha 0 a nc-1 -> BMC #
        # linha nc, nc+1 e nc+2 somatória das frações molares das correntes 
        # (F, P e R) = 1 #    
        #print('y.shape', y.shape)
        
        # Proteção das vazões negativas
        # res = y[-5:] - abs(y[-5:])
        
        for i in range(nc):
            self.E[i] = (y[-5]*y[i] - y[-4]*y[i+nc] - u[0]*y[i+2*nc])
        self.E[nc] = y[-4] - y[-3] - y[-2] - y[-1]
        self.E[nc+1] = (y[0:nc].sum() - 1)
        self.E[nc+2] = (y[nc:2*nc].sum() - 1)
        self.E[nc+3] = (y[2*nc:3*nc].sum() - 1)
        
        self.Ay[0:nc,0:nc] = y[-5]*np.identity(nc)
        self.Ay[0:nc,nc:2*nc] = - y[-4]*np.identity(nc)
        self.Ay[0:nc,2*nc:3*nc] = - u[0]*np.identity(nc)
        self.Ay[0:nc,-5] = y[0:nc] 
        self.Ay[0:nc,-4] = - y[nc:2*nc]
        self.Ay[nc,-4:] = np.array([1, -1, -1, -1])
        self.Ay[nc+1,0:nc] = np.ones(nc)
        self.Ay[nc+2,nc:2*nc] = np.ones(nc)
        self.Ay[nc+3,2*nc:3*nc] = np.ones(nc)
                
        self.Au[0:nc,0] = - y[2*nc:3*nc]
    
        return self.E, self.Ay, self.Au
    
    ###########################################################################

    def Reconciliation (self, y_m, y_u, V):
        
        # Variáveis de entrada #
        y = y_m
        u = y_u  
        V = V
        
        # Resolve modelo #        
        E =  self.Model(self.nc, y, u)[0] 
        
        # SSE - Soma dos Erros Quadráticos dos dados no modelo #
        self.Et = (E.T@E)
        
        it = 0
        self.flag = 1
        while self.flag > 0 and it < 100:
            
            it+=1
            
            # Somatório quadrático dos erros da linearização sucessiva em y e u # 
            SSEy = 0
            SSEu = 0
            
            # Resolve modelo #
            h, Ay, Au =  self.Model(self.nc, y, u)   
            
            # Modelo do processo linearizado dividido em matriz de var medida (Ay):
            #
            # Ay = [dh(0)/dy(0) dh(0)/dy(1) ... dh(0)/dy(Nvm)]
            #      [dh(1)/dy(0) dh(1)/dy(1) ... dh(1)/dy(Nvm)]
            #      [     .              .     ...          .      ]
            #      [dh(Ner)/dy(0) dh(Ner)/dy(1) ... dh(Ner)/dy(Nvm)]
            #
            # e matriz de var não medida (Au):
            #
            # Au = [dh(0)/du(0) dh(0)/du(1) ... dh(0)/du(Nvu)]
            #      [dh(1)/du(0) dh(1)/du(1) ... dh(1)/du(Nvu)]
            #      [     .              .     ...          .      ]
            #      [dh(Ner)/du(0) dh(Ner)/du(1) ... dh(Ner)/du(Nvu)]
            
            #|--------Feed---------|----------Residuo--------|--------Permeado-------|-----F-----|-----R-----|---R1---|---R2---|---R3---|
    # y_m     xf_1    ...    xf_nc   xr_1    ...    xr_nc     xp_1     ...   xp_nc        F           R         R1       R2       R3
    #         y0      ...   y(nc-1)  y(nc)   ...    y(2*nc-1) y(2*nc)  ...   y(3*nc-1)   y(-5)       y(-4)     y(-3)    y(-2)    y(-1)
            
            #|-----P------|
    # y_u          P   
    #              u0
    
    #          Au[0:nc,0] = -y[2*nc:3*nc]
    
    
            ' Cálculo do b, vetor dos coeficientes lineares do modelo linearizado '
            # Colocando y e u em 2 dimensões:
            y = y.reshape((-1,1))
            u = u.reshape((-1,1))
            b = Ay@y + Au@u - h
            
            # Fatoração QR da matriz linearizada das var não medida #
            Q, R = qr(Au, mode='complete')   
            Q1 = Q[:,0:self.Nvu]
            Q2 = Q[:,self.Nvu:self.Ner]
            R1 = R[0:self.Nvu,0:self.Nvu]
            
            rAu = matrix_rank(Au)
            rR1 = matrix_rank(R1)
            # print('Rank da Matriz R1', rR1)
            # print('Rank da Matriz Au', rAu)
            if rAu != rR1:
                sys.exit('Matrizes Au e R1 tem ranks de valores diferentes: Sistema Não-Observável')
                
            # Calculo do vetor das var reconciliada (y_hat) #
            y_hat = y - V@(Q2.T@Ay).T@inv((Q2.T@Ay)@V@(Q2.T@Ay).T)@(Q2.T@Ay@y - Q2.T@b)
            # Calculo do vetor das var estimadas (u_hat) #
            u_hat = inv(R1)@Q1.T@b - inv(R1)@Q1.T@Ay@y_hat
            
            # Somatório dos erros quadráticos (critério de tolerância) #
            for i in range(self.Nvm):
                SSEy = SSEy + (y[i,0] - y_hat[i,0])**2
                
            for i in range(self.Nvu):
                SSEu = SSEu + (u[i,0] - u_hat[i,0])**2
                
            if SSEy < 1.0e-8 and SSEu < 1.0e-8:
                self.flag = -1
                
            # Var reconciliada (y_hat) e estimada (u_hat):
            # Serão as estimativas da próxima iteração #
            y = y_hat.ravel()
            u = u_hat.ravel()
            
            # Proteção a valores negativos:
            for i in range(self.Nvm-5):
                if y[i] < 0:
                    y[i] = 0
            # for i in range(5):
            #     if y[-5+i] < 0:
            #         y[-5+i] = 1e-10
            # if u < 0:
            #     u = 1e-10
        
        if self.flag < 0:
            
            h =  self.Model(self.nc, y, u)[0]   
            
            # Erro no Balanço global nos dados reconciliados #
            self.EBG_rec = y[-5] - y[-4] - u[0]
            
            # SSE - Soma dos Erros Quadráticos dos dados reconciliados no modelo #
            self.Erec = (h.T@h)
            
            # Armazenando as var reconciliadas e estimadas #
            self.y_rec = y
            self.u_est = u
            
        elif self.flag > 0:
            
            print('Não convergiu -> y_rec = y_m')
            
            # Erro no Balanço global nos dados reconciliados #
            self.EBG_rec = 0
            
            # SSE - Soma dos Erros Quadráticos dos dados reconciliados no modelo #
            self.Erec = self.Et
            
            # Armazenando as var reconciliadas e estimadas #
            self.y_rec = y_m
            self.u_est = y_u
            
            
        return self.y_rec, self.u_est, self.Et, self.Erec, self.EBG_rec, self.flag
    
    def Spectra (self, data, method, TJ, ddof):
        
        # Sliding Window Variance Spectra #
        
        # TJ = Tamanho da Janela #
        # Dados a serem analisados #
        data = np.squeeze(np.asarray(data, dtype=np.float64))
        # Número de pontos #
        ND = data.size
        # Variável que armazenará o espectro #
        spec_var = 0
        points = []
        # Número de janelas #
        NJ = ND - TJ + 1
        soma = 0
        
        # Somatório das variâncias de cada janela #
        for i in range(0,NJ):
            
            if method == 'mean':         
                soma += np.nanvar(data[i:i+TJ], ddof=ddof)
                
            elif method == 'median':
                points.append(np.nanvar(data[i:i+TJ], ddof=ddof)) 
                
        if method=='mean':        
            spec_var = soma/NJ
            
        elif method=='median':
            spec_var = np.nanmedian(points)
            
        return spec_var
    
    ###########################################################################
    
    def Variance(self, y_m, TJ, method, ddof):
        
        Nvm = y_m.shape[0]
        
        ' Matriz de variâncias e vetores de médias e desvios-padrão estimados '
        self.var = np.zeros(Nvm)
        
        for i in range(Nvm):
            self.var[i] =  self.Spectra(data=y_m[i,:], method=method, TJ=TJ, ddof=ddof)
            
        ' Matriz V com var=0 dá LinAlgError: Singular matrix '
        var_defaul = np.array([5.89864639e-07, 9.11458333e-08, 1.78734905e-08, 6.90996361e-11,
                                4.49217007e-12, 3.19509715e-12, 2.86503158e-07, 6.81800240e-10,
                                1.86153366e-10, 2.25865209e-10, 2.85555431e-09, 3.44965843e-10,
                                1.40661934e-06, 9.64609546e-08, 2.58487766e-08, 1.52542421e-10,
                                6.79779179e-12, 2.82867208e-12, 3.41639354e-07, 1.57683659e-09,
                                4.07025227e-10, 2.34980232e-10, 5.42733516e-09, 7.30133006e-10,
                                2.07514262e-06, 6.10351563e-08, 5.26752239e-10, 1.19507744e-12,
                                1.40967361e-12, 2.67617997e-10, 1.89258207e-06, 6.49718046e-12,
                                4.36303453e-12, 2.81733622e-10, 4.26642666e-11, 6.67722024e-12,
                                4.50680602e-01, 4.22686349e-01, 1.31074457e-02, 3.49367782e-02,
                                5.71676363e-02])
        for i in range(Nvm):
            if self.var[i] <= var_defaul[i]/100:
                # self.var[i] = min([v for v in self.var if v !=0])
                self.var[i] = var_defaul[i]
        self.V = np.diag(self.var)
        
        self.dp= np.sqrt(self.var)
        
        return self.V, self.var, self.dp


    ###############################################################################
    #       CÁLCULOS DOS ÍNDICES DE DEEMPENHO DA RECONCILIAÇÃO DE DADOS  
    ###############################################################################
    
    def Fobj_indices(self, y_m, y_rec, nt, TJ):
            
        F1 = np.zeros((Nvm,nt))
        var = self.Variance(y_m, TJ, 'median', 0)[1]
        # var = np.nanvar(y_m, axis=1)
        
        for j in range(nt):
            for i in range(Nvm):
                F1[i,j] = (y_rec[i,j] - y_m[i,j])**2/var[i]
                
        F_sum = np.sum(F1, axis=0)
        F_mean = np.nanmean(F_sum)
        F_median = np.nanmedian(F_sum)
        
        return F_sum, F_mean, F_median
    
    ###########################################################################
    
    def Chi_square(self, Nvm, Nvu, Ner):
        
        # Chi-square: percent point function - ppf (inverse of cdf - cumulative 
        # distribution function) #
        GL = Nvm - (Nvm + Nvu - Ner)
        chi2_u = chi2.ppf(0.995, GL)
        chi2_l = chi2.ppf(0.005, GL)
        
        return chi2_u, chi2_l, GL
    
    ###########################################################################
    
    def DataAnalysis(self, y_m, y_rec, TJ):
        
        nt = y_m.shape[1]
        
        # Análise da Fobj e teste Chi2 #
        self.F_sum, self.F_mean, self.F_median = self.Fobj_indices(y_m, y_rec, nt, TJ)
        
        # The median absolute deviation (MAD) is a robust measure of the 
        # variability of a univariate sample of quantitative data.
        self.MADn_Fobj = MAD(self.F_sum, scale='normal', nan_policy='omit')
        
        return self.F_sum, self.F_mean, self.F_median, self.MADn_Fobj

#%%
###############################################################################
#           CÁLCULO DO BALANÇO DE ENERGIA                #
###############################################################################

nc = 12

# Constante das Capacidades Caloríficas específicas à pressão constante de Gás Ideal 
# ajustada por funções polinomiais Cp/R (van Ness - pg 512 apendice C):
pCp = np.zeros((nc,4))
pCp[0,:] = np.array([1.702, 9.081*1e-3, -2.164*1e-6, 0])                  #C1
pCp[1,:] = np.array([1.131, 19.225*1e-3, -5.561*1e-6, 0])                 #C2
pCp[2,:] = np.array([1.213, 28.785*1e-3, -8.824*1e-6, 0])                 #C3
pCp[3,:] = np.array([3.025, 53.722*1e-3, -16.791*1e-6, 0])                #C6
pCp[4,:] = np.array([3.570, 62.127*1e-3, -19.486*1e-6, 0])                #C7
pCp[5,:] = np.array([4.108, 70.567*1e-3, -22.208*1e-6, 0])                #C8
pCp[6,:] = np.array([5.457, 1.045*1e-3, 0, -1.157e+5])                    #CO2
pCp[7,:] = np.array([1.677, 37.853*1e-3, -11.945*1e-6, 0])                #iC4
pCp[8,:] = np.array([2.464, 45.351*1e-3, -14.111*1e-6, 0])                #iC5 *(igual ao nC5)
pCp[9,:] = np.array([3.28, 0.593*1e-3, 0, 0.04e5])                        #N2
pCp[10,:] = np.array([1.935, 36.915*1e-3, -11.402*1e-6, 0])               #nC4
pCp[11,:] = np.array([2.464, 45.351*1e-3, -14.111*1e-6, 0])               #nC5

A = pCp[:,0]
B = pCp[:,1]
C = pCp[:,2]
D = pCp[:,3]

# Fator ascêntrico (w):
w = np.array([0.12e-1, .100, .152, .301, .350, .400, .224, .181, .252, 0.38e-1, .200, .252])

# Temperatura e Pressão critíca (Tc, Pc):
Tc = np.array([190.6, 305.3, 369.8, 507.6, 540.2, 568.7, 304.2, 408.1, 469.7, 126.2, 425.1, 469.7])
Pc = np.array([45.99, 48.72, 42.48, 30.25, 27.40, 24.90, 73.83, 36.48, 33.70, 34.00, 37.96, 33.70])

# Constante dos gases [Pa.m3/mol/K] = [J/mol/K]
Rg = 8.3145

# Condição Normal:
# Pn = 1 atm = 1.0132e5 Pa
# Tn = 20 C = 293.15 K

Pn = 1.0132e5   # [Pa]
Tn = 293.15     # [K]

Pref = 1.01     # [bar]
Tref = 298      # [K]

VMn = (Rg*Tn)/Pn # [m3/mol]

# Entalpia de gás ideal:
def Hig(T, x):
    H = np.zeros(nc)
    H = (A + (1/2)*B*Tref*(T/Tref + 1) + (1/3)*C*Tref**2*(T**2/Tref**2 + T/Tref + 1) + D/(T*Tref))*(T - Tref)
    Hig = x@H
    return Hig

# Entalpia residual:
def Hres(T, P, y, EoS):
    
    # Instancia parâmetros e resolve regra da mistura #
    param_obj = Param_EoS(T, P, y, EoS)
    Tcm, wm = param_obj.Mistura() 
    
    # Calcula parâmetros da EoS #
    EoS_mistura_obj = EoS_mistura(param_obj, Tcm, wm, EoS)
    EoS_mistura_obj.AB()
    
    # Calcula entalpia residual da mistura #
    HR_obj = HR(param_obj, EoS_mistura_obj, EoS)
    Hr = HR_obj.run()
    
    return Hr 

# Balanço de Energia Global:
def BE(T, *args):
    F, R, P, xf, xr, xp, Tf, Tr, Pr, Pp, Pf, Tc, Pc, w = args
    
    # Feed:
    Hf = Hig(Tf, xf)
    Hrf1 = Hres(Tref, Pref, xf, EoS)
    Hrf2 = Hres(Tf, Pf, xf, EoS)
    H_feed = Rg*Hf - Hrf1 + Hrf2
    
    # Residuo
    Hr = Hig(Tr, xr)
    Hrr1 = Hres(Tref, Pref, xr, EoS)
    Hrr2 = Hres(Tr, Pr, xr, EoS)
    H_residuo = Rg*Hr - Hrr1 + Hrr2
    
    # Permeado
    Hp = Hig(T, xp)
    Hrp1 = Hres(Tref, Pref, xp, EoS)
    Hrp2 = Hres(T, Pp, xp, EoS)
    H_permeado = Rg*Hp - Hrp1 + Hrp2
    
    # BE
    res = 0
    res = F*H_feed - R*H_residuo - P*H_permeado
    
    return res

def args_BE(y_rec, u_est, y_m2):
    
    ######### Variáveis Reconciliadas ##########
    # Convertendo unidades: [kNm^3/h -[1e3/VMn]-> mol/h]
    F = y_rec[-5,0]*1e3/VMn
    R = y_rec[-4,0]*1e3/VMn
    P = u_est[0,0]*1e3/VMn
    
    # Concentrações das correntes:
    xf = y_rec[0:nc,0]
    xr = y_rec[nc:2*nc,0]
    xp = y_rec[2*nc:3*nc,0]
    ############################################

    ######## Variáveis Não Reconciliadas #######
    # y_m2 = [Tf, Tr, Pr, Pp, Pf]
    Tf = y_m2[0,0]
    Tr = y_m2[1,0]
    Pr = y_m2[2,0]
    Pp = y_m2[3,0]
#    Pf = P_feed(Tsat, Ant, xf)      # Calculado por Tsat:
    Pf = y_m2[4,0]                  # Dado estimado:

    # Balanço de Energia:
    args=(F, R, P, xf, xr, xp, Tf, Tr, Pr, Pp, Pf, Tc, Pc, w)
    
    return args

""" Equação de Estado: Peng-Robinson, Soave-Redlich-Kwong ou Redlich-Kwong """
EoS = 'PR'
# EoS = 'SRK'
# EoS = 'RK'



#%%
###############################################################################
#                           DESCRIÇÃO DAS VARIÁVEIS                           #
###############################################################################

main_var = ['Cromatografia alimentação das membranas de CO2 - C1',
    'Cromatografia alimentação das membranas de CO2 - C2',
    'Cromatografia alimentação das membranas de CO2 - C3',
    'Cromatografia alimentação das membranas de CO2 - C6',
    'Cromatografia alimentação das membranas de CO2 - C7',
    'Cromatografia alimentação das membranas de CO2 - C8',
    'Cromatografia alimentação das membranas de CO2 - CO2',
    'Cromatografia alimentação das membranas de CO2 - iC4',
    'Cromatografia alimentação das membranas de CO2 - iC5',
    'Cromatografia alimentação das membranas de CO2 - N2',
    'Cromatografia alimentação das membranas de CO2 - nC4',
    'Cromatografia alimentação das membranas de CO2 - nC5',
    'Cromatografia resíduo das membranas de CO2 - C1',
    'Cromatografia resíduo das membranas de CO2 - C2',
    'Cromatografia resíduo das membranas de CO2 - C3',
    'Cromatografia resíduo das membranas de CO2 - C6',
    'Cromatografia resíduo das membranas de CO2 - C7',
    'Cromatografia resíduo das membranas de CO2 - C8',
    'Cromatografia resíduo das membranas de CO2 - CO2',
    'Cromatografia resíduo das membranas de CO2 - iC4',
    'Cromatografia resíduo das membranas de CO2 - iC5',
    'Cromatografia resíduo das membranas de CO2 - N2',
    'Cromatografia resíduo das membranas de CO2 - nC4',
    'Cromatografia resíduo das membranas de CO2 - nC5',
    'Cromatografia permeado das membranas de CO2 - C1',
    'Cromatografia permeado das membranas de CO2 - C2',
    'Cromatografia permeado das membranas de CO2 - C3',
    'Cromatografia permeado das membranas de CO2 - C6',
    'Cromatografia permeado das membranas de CO2 - C7',
    'Cromatografia permeado das membranas de CO2 - C8',
    'Cromatografia permeado das membranas de CO2 - CO2',
    'Cromatografia permeado das membranas de CO2 - iC4',
    'Cromatografia permeado das membranas de CO2 - iC5',
    'Cromatografia permeado das membranas de CO2 - N2',
    'Cromatografia permeado das membranas de CO2 - nC4',
    'Cromatografia permeado das membranas de CO2 - nC5',
    'Vazão de gás montante ao 1° estágio de membranas',
    'Vazão residual jusante  as membranas de remoção de CO2',
    'Vazão de gás residual do Trem A das membranas de CO2',
    'Vazão de gás residual do Trem B das membranas de CO2',
    'Vazão de gás residual do Trem C das membranas de CO2']
Nvm=len(main_var)

minor_var = ['Pressão residual jusante  as membranas de remoção de CO2',
            'Pressão do permeado jusante a remoção de CO2',
            'Temperatura montante as membranas de remoção de CO2',
            'Temperatura residual jusante as membranas de remoção de CO2']
Nvm2 = len(minor_var)+1



#%%
###############################################################################
#                       LENDO DADOS RECONCILIADOS
###############################################################################
df = 2
if df == 1:
    dados = pd.read_hdf('Membranas_DR_v0.3_(2018-01-01)2.h5','df_RD')
elif df == 2:
    dados = pd.read_hdf('Membranas_DR_v0.4_(2020-05-28).h5','df_RD')


#%%
###############################################################################
#           MONITORAMENTO: ATUALIZAÇÃO DOS DADOS MEDIDOS E RECONCILIADOS      #
###############################################################################

class Monitoramento():
    
    def __init__(self, TamanhoMaximoJanela, TamanhoJanelaAquisicao, label, dados):
        
        self.n = 0
        self.n2 = 0
        self.y_m = []
        self.y_m2 = []
        self.y_rec = []
        self.u_est = []
        self.ts2 = []
        self.df_rec = []
        self.label = label
        self.h = TamanhoJanelaAquisicao
        self.ts_deque = deque(maxlen= TamanhoMaximoJanela)
        self.F_sum = []
        self.F_mean = []
        self.F_median = []
        self.MADn_Fobj = []
        self.flag = []
        self.flag2 = []
        self.parada = False
        
        # Para teste e debug fora da Petrobras -> Comentar #
        #---------------------------------------------------------------------------------------#
        # Configuração da consulta ao PI
        # self.server = 'SBS00AS25'
        # self.login = None
        #---------------------------------------------------------------------------------------#

        self.tags = ['CSP_30100A_2705_AT_001A_C1',
        'CSP_30100A_2705_AT_001A_C2',
        'CSP_30100A_2705_AT_001A_C3',
        'CSP_30100A_2705_AT_001A_C6',
        'CSP_30100A_2705_AT_001A_C7',
        'CSP_30100A_2705_AT_001A_C8',
        'CSP_30100A_2705_AT_001A_CO2',
        'CSP_30100A_2705_AT_001A_IC4',
        'CSP_30100A_2705_AT_001A_IC5',
        'CSP_30100A_2705_AT_001A_N2',
        'CSP_30100A_2705_AT_001A_NC4',
        'CSP_30100A_2705_AT_001A_NC5',
        'CSP_30100A_2705_AT_001B_C1',
        'CSP_30100A_2705_AT_001B_C2',
        'CSP_30100A_2705_AT_001B_C3',
        'CSP_30100A_2705_AT_001B_C6',
        'CSP_30100A_2705_AT_001B_C7',
        'CSP_30100A_2705_AT_001B_C8',
        'CSP_30100A_2705_AT_001B_CO2',
        'CSP_30100A_2705_AT_001B_IC4',
        'CSP_30100A_2705_AT_001B_IC5',
        'CSP_30100A_2705_AT_001B_N2',
        'CSP_30100A_2705_AT_001B_NC4',
        'CSP_30100A_2705_AT_001B_NC5',
        'CSP_30100A_2705_AT_001C_C1',
        'CSP_30100A_2705_AT_001C_C2',
        'CSP_30100A_2705_AT_001C_C3',
        'CSP_30100A_2705_AT_001C_C6',
        'CSP_30100A_2705_AT_001C_C7',
        'CSP_30100A_2705_AT_001C_C8',
        'CSP_30100A_2705_AT_001C_CO2',
        'CSP_30100A_2705_AT_001C_IC4',
        'CSP_30100A_2705_AT_001C_IC5',
        'CSP_30100A_2705_AT_001C_N2',
        'CSP_30100A_2705_AT_001C_NC4',
        'CSP_30100A_2705_AT_001C_NC5',
        'CSP_30100A_2705_FT_001',
        'CSP_30100A_2705_FT_002',
        'CSP_30100A_2705A_FT_001',
        'CSP_30100A_2705B_FT_001',
        'CSP_30100A_2705C_FT_001',
        'CSP_30100A_2705_PT_003',
        'CSP_30100A_2705_PT_004',
        'CSP_30100A_2705_TT_001',
        'CSP_30100A_2705_TT_002']
        
        self.Nvm=len(self.tags)
        
        self.bias = np.ones(len(self.tags))
        
        # Para analisar e debug arquivos HDF5 da Petrobras -> Descomentar #
        #---------------------------------------------------------------------------------------#
        self.dados = dados
        
        if df == 1:
            # self.ini = 2700  # data = 1 - Possível falha na mudança de operação em 04:50h - 02/03/2020
            self.ini = 0
        elif df == 2:
            # self.ini = 400  # data = 2 - Possível falha na mudança de operação em 22:10h - 17/03/2020
            # self.ini = 900  # data = 2 - Possível falha no congelamento de variáveis em 14:00h - 19/03/2020 (final da série)
            self.ini = 0
        elif df == 3:
            # self.ini = 900  # data = 3 - Possível falha no congelamento de variáveis em 12:45h - 26/03/2020
            self.ini = 0
        elif df == 4:
            # self.ini = 9300       # Possível falha na mudança de operação em 11:20h - 03/02/2020
            # self.ini = 11300      # Falha de bias (xR) em 19:30h - 10/02/2018
            # self.ini = 14000      # Falha de bias (xP) em 04:45h - 20/02/2018
            # self.ini = 17400      # Desligamento de operação em 22:30h - 04/03/2018
            # self.ini = 21583      # Reiniciamento de operação e toda a instrumentação em 24:00h - 17/03/2018
            # self.ini = 25000      # Desligamento de operação em 17:45h - 30/03/2018
            # self.ini = 25830      # Reiniciamento de operação e toda a instrumentação em 12:35h - 17/04/2018
            # Período selecionado para a fase de estudos (18/04/2018 00:00h - 30/04/2018 00:00h)
            # self.ini = 22939
            # self.ini = 28100      # Possível falha, mudança de operação 7h - 26/04/2018
            self.ini = 34000
            # self.ini = 34120      # Desligamento de operação em 18h - 16/05/2018
            # self.ini = 34560      # Reiniciamento de operação em 17:40h - 17/05/2018
            # self.ini = 35400      # Possível falha, mudança de operação em 16h 21/05/2018
            # self.ini = 37600      # Falha de congelamento das variáveis em 20:25h - 28/05/2018
            # self.ini = 40850      # Falha de congelamento das variáveis em 21:30h - 8/06/2018
            # self.ini = 0
        else:
            self.ini = 2050
        
        if type(self.dados.index[self.ini]) == str:
            self.start_date = str(self.dados.index[self.ini][:10])
        else:
            self.start_date = str(self.dados.index[self.ini].round('D'))[:10]
        #---------------------------------------------------------------------------------------#
        
        
    def AtualizaDados(self):
        
        self.flag = False
        
        ###############################################################################
        #                             AQUISIÇÃO DE DADOS                              #
        ###############################################################################
        
        # Para teste e debug fora da Petrobras -> Comentar #
        #---------------------------------------------------------------------------------------#
        # Baixando
        # Definindo range de leitura dos dados
#         now = datetime.datetime.now()
#         before = now - datetime.timedelta(1/24*2) # janela de 2 horas
# #         now = now.strftime("%d/%m/%Y %H:%M:%S")
# #         before = before.strftime("%d/%m/%Y %H:%M:%S")
#         session = pdpi.Session(server_name=self.server, login=self.login, tags=self.tags, 
#                                time_range=(before.strftime("%d/%m/%Y %H:%M:%S"), now.strftime("%d/%m/%Y %H:%M:%S")),
#                                time_span='5m')
        
#         dados = session.df
        
        # # Proteção para dados faltantes:
        # dados = dados.apply(pd.to_numeric, errors='coerce')
        # dados = dados.fillna(method='ffill')
        # dados = dados.fillna(method='bfill')
        
        # y_mt = np.array(self.dados).T
        #---------------------------------------------------------------------------------------#
        
        
        # Para analisar e debug arquivos HDF5 da Petrobras -> Descomentar #
        #---------------------------------------------------------------------------------------#
        self.now = self.dados.index[self.ini + self.n2 + self.h].round('min')
        self.dados_h = self.dados.iloc[self.ini + self.n2 : self.ini + self.n2 + self.h, : ]
        
        # Proteção para dados faltantes:
        self.dados_h = self.dados_h.apply(pd.to_numeric, errors='coerce')
        self.dados_h = self.dados_h.ffill()
        self.dados_h = self.dados_h.bfill()
        
        y_mt = np.array(self.dados_h).T
        #---------------------------------------------------------------------------------------#
        
        ###############################################################################
        #                             VETORIZANDO OS DADOS                            #
        ###############################################################################
        
        # Para analisar e debug arquivos HDF5 da Petrobras -> Descomentar #
        #---------------------------------------------------------------------------------------#
        y_mF = y_mt[:self.Nvm-4,:]
        y_mTP = y_mt[-6:-2,-1]
        y_mTP = y_mTP.ravel()
        
        # Banlanço de Energia:
        # Número de variáveis medidas #
        self.Nvm2 = len(y_mTP) + 1
        
        # Número de variáveis não medidas #
        self.Nvu2 = 1
        
        y_m2 = np.zeros(self.Nvm2)
        y_m2[:2] = y_mTP[:2] + 273          # Convertendo [°C] -> [K]
        y_m2[2:-1] = y_mTP[2:]
        y_m2[-1] = y_m2[2] + 0.8            # Supondo que a pressão de entrada seja 0.8 bar maior que do resíduo
        #---------------------------------------------------------------------------------------#
        
        ###############################################################################
        #                 PROTEÇÃO CONTRA PARADA/PARTIDA DE OPERAÇÃO                  #
        ###############################################################################
        
        # condição de operação normal:
            # Vazão limite para pausar/startar o monitoramento [kNm³/h]
        F_lim_parada = 100
        F_lim_partida = 130
        if np.sort(y_mF[-5,:])[0] > F_lim_parada and self.parada == False:
            self.flag2 = True
            self.parada = False
        elif np.sort(y_mF[-5,:])[0] > F_lim_partida and self.parada == True:
            self.flag2 = True
            self.parada = False
            # self.n = 0
        else:
            self.flag2 = False
            self.parada = True
        
        
        
        ###############################################################################
        #           CÁLCULO DE VARIÂNCIA E DESVIO PADRÃO DAS VARIÁVEIS                #
        ###############################################################################
        # Trasformação de dados #
        # Normalizando entre [0,1] as concentrações #
        y_mF[:-5,:] = y_mF[:-5,:]/100.
        
        # Estimativa inicial da var não medida no tempo #
        Nvm, nt = y_mF.shape
        Nvu = 1
        y_uF = np.zeros((Nvu,nt))
        
        # Criando a estimativa inicial da variável não medida (vazão do permeado) #
        y_uF[0,:] = y_mF[-5,:] - y_mF[-4,:]
        
        
        
        # Instancia classe Reconciliação de Dados #
        DR = DataReconciliation(Nvm, Nvu, nt) 
        
        # Matriz V, matriz de variâncias e vetores de desvios-padrão estimados #
        ' Matriz V com var=0 dá LinAlgError: Singular matrix '
        #---------------------------------------------------------------------------#
        # Metricas de estimativa de variância (Janela de aquisição):
        #---------------------------------------------------------------------------#
        # Nível de robustes e outros parâmetros do teste de erro grosseiro
        robust = 0.20
        p_dp = 7
        p_Hdp = 20
        
        
        #---------------------------------------------------------------------------#
        # if self.flag2 == True:
        
        #     var_agora = np.var(y_mF, axis=1, ddof=0).reshape(-1,1)
        
        #     # var_agora = np.var(y_mF, axis=1, ddof=1).reshape(-1,1)
        
        #     # y_mF_L = np.sort(y_mF[:,int(nt*robust):-int(nt*robust)], axis=1)
        #     # var_agora = np.var(y_mF_L, axis=1).reshape(-1,1)
        
        #     # MADn = MAD(y_mF, axis=1, scale='normal', nan_policy='omit').reshape(-1,1)
        #     # var_agora = MADn**2
        
        #     # var_agora = DR.Variance(y_mF, TJ=4, method='median', ddof=0)[1].reshape(-1,1)
        
        #     var_agora[-5:] = DR.Variance(y_mF[-5:,:], TJ=4, method='median', ddof=0)[1].reshape(-1,1)
        
        # elif self.flag2 == False:
        
        #     var_agora = np.array([5.89864639e-07, 9.11458333e-08, 1.78734905e-08, 6.90996361e-11,
        #                           4.49217007e-12, 3.19509715e-12, 2.86503158e-07, 6.81800240e-10,
        #                           1.86153366e-10, 2.25865209e-10, 2.85555431e-09, 3.44965843e-10,
        #                           1.40661934e-06, 9.64609546e-08, 2.58487766e-08, 1.52542421e-10,
        #                           6.79779179e-12, 2.82867208e-12, 3.41639354e-07, 1.57683659e-09,
        #                           4.07025227e-10, 2.34980232e-10, 5.42733516e-09, 7.30133006e-10,
        #                           2.07514262e-06, 6.10351563e-08, 5.26752239e-10, 1.19507744e-12,
        #                           1.40967361e-12, 1.19507744e-13, 1.89258207e-06, 6.49718046e-12,
        #                           4.36303453e-12, 2.81733622e-10, 4.26642666e-11, 6.67722024e-12,
        #                           4.50680602e-01, 4.22686349e-01, 1.31074457e-02, 3.49367782e-02,
        #                           5.71676363e-02]).reshape(-1,1)
        #---------------------------------------------------------------------------#
        
        
        #---------------------------------------------------------------------------#
        var_agora = np.var(y_mF, axis=1, ddof=0).reshape(-1,1)
            
        # var_agora = np.var(y_mF, axis=1, ddof=1).reshape(-1,1)
        
        # y_mF_L = np.sort(y_mF[:,int(nt*robust):-int(nt*robust)], axis=1)
        # var_agora = np.var(y_mF_L, axis=1).reshape(-1,1)
        
        # MADn = MAD(y_mF, axis=1, scale='normal', nan_policy='omit').reshape(-1,1)
        # var_agora = MADn**2
        
        # var_agora = DR.Variance(y_mF, TJ=self.h, method='median', ddof=0)[1].reshape(-1,1)
        
        var_agora[-5:] = DR.Variance(y_mF[-5:,:], TJ=4, method='median', ddof=0)[1].reshape(-1,1)
        #---------------------------------------------------------------------------#
        
        
        # print('iterações', self.n)
        
        #---------------------------------------------------------------------------#
        # Janelas de variânmcias e testes estatísticos de outliers e bias:
        #---------------------------------------------------------------------------#
        if self.n2 == 0:
            
            self.var = var_agora
            self.V = np.diag(var_agora.ravel())
            self.dp = np.std(var_agora.ravel())
            
        else:
            
            if self.n2 < TamanhoMaximoJanela:
                
                self.var = np.hstack((self.var, var_agora))
                for i in range(Nvm):
                    if var_agora[i,-1] == 0:
                        self.var[i,-1] = np.median(self.var[i,:-1])
                
                k=0   
                for i in range(Nvm-5):
                    dp = np.sqrt(np.median(self.var[i,-p_Hdp:]))
                    mu = np.median(y_mF[i,-p_Hdp:])
                    if p_dp*dp < abs(mu-y_mF[i,-1]):
                        k+=1
                        Mag = abs(mu-y_mF[i,-1])/dp
                        
                        self.var[i,-1] = np.sort(self.var, axis=1)[i,-1]*Mag**2
                        # self.var[i,-1] = np.median(self.var[i,:])
                        # self.var[i,-1] = np.median(self.var[i,:])*100
                        # self.var[:,-1] = np.median(self.var)
                        # self.var[i,-1] = np.mean(self.var[i,:])*100
                        # self.var[i,-1] = self.var[i,-1]
                        # self.var[:,-1] = self.var[:,-1]
                        
                if k<=(Nvm*robust):  
                    self.V = np.diag(np.sort(self.var, axis=1)[:,int(self.n2/30)])
                    self.dp = np.std(np.sort(self.var, axis=1)[:,int(self.n2/30)])
                    # self.V = np.diag(self.var[:,-1])
                    # self.dp = np.std(self.var[:,-1])
                    # self.V = np.diag(np.median(self.var, axis=1))
                    # self.dp = np.std(np.median(self.var, axis=1))
                    # self.V = np.diag(np.mean(self.var, axis=1))
                    # self.dp = np.std(np.mean(self.var, axis=1))
                
                else:
                    self.V = np.diag(self.var[:,-1])
                    self.dp = np.std(self.var[:,-1])
                    # self.V = np.diag(np.median(self.var, axis=1))
                    # self.dp = np.std(np.median(self.var, axis=1))
                    # self.V = np.diag(np.mean(self.var, axis=1))
                    # self.dp = np.std(np.mean(self.var, axis=1))
                    # self.V = np.diag(np.var(y_mF, axis=1, ddof=1).reshape(-1,1))
                    # self.dp = np.std(np.var(y_mF, axis=1, ddof=1).reshape(-1,1))
                
            else:
                
                # var_agora = DR.Variance(self.y_m, TJ=100, method='median', ddof=1)[1].reshape(-1,1)
                # var_agora = np.var(self.y_m, axis=1, ddof=0).reshape(-1,1)
                self.var = np.hstack((self.var[:,1:], var_agora))
                for i in range(Nvm):
                    if var_agora[i,-1] == 0:
                        self.var[i,-1] = np.median(self.var[i,:-1])
                
                k=0   
                for i in range(Nvm-5):
                    dp = np.sqrt(np.median(self.var[i,-p_Hdp:]))
                    mu = np.median(y_mF[i,-p_Hdp:])
                    if p_dp*dp < abs(mu-y_mF[i,-1]):
                        k+=1
                        Mag = abs(mu-y_mF[i,-1])/dp
                        
                        self.var[i,-1] = np.sort(self.var, axis=1)[i,-1]*Mag**2
                        # self.var[i,-1] = np.median(self.var[i,:])
                        # self.var[i,-1] = np.median(self.var[i,:])*100
                        # self.var[:,-1] = np.median(self.var)
                        # self.var[i,-1] = np.mean(self.var[i,:])*100
                        # self.var[i,-1] = self.var[i,-1]
                        # self.var[:,-1] = self.var[:,-1]
                        
                if k<=(Nvm*robust):  
                    self.V = np.diag(np.sort(self.var, axis=1)[:,10])
                    self.dp = np.std(np.sort(self.var, axis=1)[:,10])
                    # self.V = np.diag(self.var[:,-1])
                    # self.dp = np.std(self.var[:,-1])
                    # self.V = np.diag(np.median(self.var, axis=1))
                    # self.dp = np.std(np.median(self.var, axis=1))
                    # self.V = np.diag(np.mean(self.var, axis=1))
                    # self.dp = np.std(np.mean(self.var, axis=1))
                    
                else:
                    self.V = np.diag(self.var[:,-1])
                    self.dp = np.std(self.var[:,-1])
                    # self.V = np.diag(np.median(self.var, axis=1))
                    # self.dp = np.std(np.median(self.var, axis=1))
                    # self.V = np.diag(np.mean(self.var, axis=1))
                    # self.dp = np.std(np.mean(self.var, axis=1))
                    # self.V = np.diag(np.var(y_mF, axis=1, ddof=1).reshape(-1,1))
                    # self.dp = np.std(np.var(y_mF, axis=1, ddof=1).reshape(-1,1))       
        #---------------------------------------------------------------------------#
        
        # print('var agora:',var_agora)
        # print('var depois:',self.var)
        
        # self.V = np.diag(var_agora)
        
        y_m_agora = y_mF[:,-1]
        y_u_agora = y_uF[:,-1] 
        
        
        if self.flag2 == True:
            
            #---------------------------------------------------------------------------#
            # Janelas de dados reconciliados, estimados, calculados e análise de bias:
            #---------------------------------------------------------------------------#
            
            
            ###############################################################################
            #                         PRIMEIRO PONTO H=0                                  #
            ###############################################################################
            
            if self.n == 0:  # primeiro ponto
                
                self.y_m = y_m_agora = y_m_agora.reshape((-1,1))
                self.y_m2 = y_m2_agora = y_m2.reshape((-1,1))
                y_u_agora = y_u_agora.reshape((-1,1))
                
                self.ts_deque.append(self.now)
                self.ts2 = pd.DatetimeIndex(self.ts_deque)
                
                # Estimativa inicial de y (var medida) e u (var não medida) #    
                y = y_m_agora[:,0]
                u = y_u_agora[:,0]     
                
                
                ''' Reconciliação de Dados'''
                # # Instancia classe #
                # Reconciliacao_obj = Reconciliacao(Nvm, Nvu, nt)
                # Resolve classe #
                y_rec, u_est, Et, Erec, EBG_rec, flag = DR.Reconciliation(y, u, self.V)
                
                self.y_rec = y_rec.reshape((-1,1))
                self.u_est = u_est.reshape((-1,1))
                
                
                ''' Balanço de Energia '''
                    # Criando a estimativa inicial da variável não medida (temperatura do permeado):
                Tp_guess = 37.0 + 273   # Convertendo [°C] -> [K]
                args = args_BE(self.y_rec, self.u_est, self.y_m2)
                Tp, info, Et2, _ = fsolve(BE, Tp_guess, args, xtol=1e-8, maxfev=100, full_output=True)
                
                
                
                # Desnormalizando as concentrações [0,1] -> % #
                self.y_m[:-5,0] = self.y_m[:-5,0]*100
                self.y_rec[:-5,0] = self.y_rec[:-5,0]*100
                # Convertendo [K] -> [°C]
                self.y_m2[:2,0] = self.y_m2[:2,0] - 273
                Tp = Tp - 273  
                self.Tp = Tp.reshape((-1,1))
                
                #---------------------------------------------------------#
                # Análise de bias:
                #---------------------------------------------------------#
                # DR error analysis: median[sqrt(Fobj)]
                # Bias - erro grosseiro sistemático
                # self.bias = np.median(np.abs(self.y_m - self.y_rec), axis=1)/self.dp
                #---------------------------------------------------------#
                
                
                #---------------------------------------------------------#
                # Análise de outliers:
                #---------------------------------------------------------#
                # self.F_sum, self.F_mean, self.F_median, self.MADn_Fobj = DR.DataAnalysis(self.y_m, self.y_rec, TJ=2)
                #---------------------------------------------------------#
                
                
                self.n += 1
                self.n2 += 1
            else:
            
            ###############################################################################
            #                     JANELA CUMULATIVA - 0<H<H_MAX                           #
            ###############################################################################
            
                if self.n < TamanhoMaximoJanela:
                    
                    y_m_agora = y_m_agora.reshape((-1,1))
                    y_m2_agora = y_m2.reshape((-1,1))
                    y_u_agora = y_u_agora.reshape((-1,1))
                    ts_instantaneo = self.now
                    
                    # Estimativa inicial de y (var medida) e u (var não medida) #    
                    y = y_m_agora[:,0]
                    u = y_u_agora[:,0]     
                    
                    ''' Reconciliação de Dados'''
                    # # Instancia classe #
                    # Reconciliacao_obj = Reconciliacao(Nvm, Nvu, nt)
                    # Resolve classe #
                    
                    y_rec_agora, u_est_agora, Et, Erec, EBG_rec, flag = DR.Reconciliation(y, u, self.V)
                    
                    y_rec_agora = y_rec_agora.reshape((-1,1))
                    u_est_agora = u_est_agora.reshape((-1,1))
                    
                    
                    ''' Balanço de Energia '''
                        # Criando a estimativa inicial da variável não medida (temperatura do permeado):
                    if np.isnan(self.Tp[-1][-1]) == True:
                        Tp_guess = 37.0 + 273   # Convertendo [°C] -> [K]
                    else:
                        Tp_guess = self.Tp[-1][-1] + 273   # Convertendo [°C] -> [K]
                    # print('BED inicio', Tp_guess-273)
                    args = args_BE(y_rec_agora, u_est_agora, y_m2_agora)
                    Tp_agora, info, Et2, _ = fsolve(BE, Tp_guess, args, xtol=1e-8, maxfev=100, full_output=True)
                    
                    
                    # Desnormalizando as concentrações [0,1] -> % #
                    y_m_agora[:-5] = y_m_agora[:-5]*100
                    y_rec_agora[:-5] = y_rec_agora[:-5]*100
                    # Convertendo [K] -> [°C]
                    y_m2_agora[:2] = y_m2_agora[:2] - 273
                    Tp_agora = Tp_agora - 273  
                    Tp_agora = Tp_agora.reshape((-1,1))
                    
                    # Concatenando os dados:
                    print('#--------------------------------------------------------#')
                    print('JANELA CUMULATIVA - 0<H<H_MAX')
                    print('self.n', self.n)
                    print('y_m.shape[1]', self.y_m.shape[1])
                    print('len(self.ts2)', len(self.ts2))
                    print('#--------------------------------------------------------#')
                    self.y_m = np.hstack((self.y_m, y_m_agora))
                    self.y_rec = np.hstack((self.y_rec, y_rec_agora))
                    self.u_est = np.hstack((self.u_est, u_est_agora))
                    
                    self.y_m2 = np.hstack((self.y_m2, y_m2_agora))
                    self.Tp = np.hstack((self.Tp, Tp_agora))
                    
                    self.ts_deque.append(ts_instantaneo)
                    self.ts2 = pd.DatetimeIndex(self.ts_deque) 
                    
                    print('y_m.shape[1]', self.y_m.shape[1])
                    print('len(self.ts2)', len(self.ts2))
                    print('#--------------------------------------------------------#\n')
                    
                    
                    
                    #---------------------------------------------------------#
                    # Análise de bias:
                    #---------------------------------------------------------#
                    # print("Bias")
                    # print("Flag:", self.flag)
                    if self.n < 30:
                        TJ = self.n+1
                    else:
                        TJ = 30
                    # Desvio-padrão das variáveis reconciliadas # 
                    # self.dp_rec = np.nanstd(self.y_rec[:,-TJ:], axis=1)
                    self.dp_rec = DR.Variance(self.y_rec, TJ=TJ, method='median', ddof=1)[2]
                    # Bias - erro grosseiro sistemático
                    self.bias = np.nanmedian(np.abs(self.y_m - self.y_rec), axis=1)/self.dp_rec
                    # self.bias = np.nanmedian(np.abs(self.y_m - self.y_rec), axis=1)/self.dp
                    #---------------------------------------------------------#
                    
                    #---------------------------------------------------------#
                    # Análise de outliers:
                    #---------------------------------------------------------#
                    # print("Outliers")
                    # print("Flag:", self.flag)
                    self.F_sum, self.F_mean, self.F_median, self.MADn_Fobj = DR.DataAnalysis(self.y_m, self.y_rec, TJ=TJ)
                    
                    # Analise de Outliers e Fobj
                    self.nt = len(self.ts2)
                    self.out_x = np.argwhere(self.F_sum >= self.F_median+3*self.MADn_Fobj).ravel()
                    self.Outliers = np.zeros(len(self.out_x))
                    for j in range(len(self.out_x)):
                        for i in range(self.nt):
                            if self.out_x[j]==i:
                                self.Outliers[j] = self.F_sum[i]
                                # print('i', i)
                                # print('i', i)
                                # print('self.Outliers[j]', self.Outliers[j])
                                # print('self.F_sum[i]', self.F_sum[i])
                    #---------------------------------------------------------#
                    
                    self.n += 1
                    self.n2 += 1
                else:
                    
            ###############################################################################
            #                     JANELA DESLIZANDE - H=H_MAX                             #
            ###############################################################################
                    
                    y_m_agora = y_m_agora.reshape((-1,1))
                    y_m2_agora = y_m2.reshape((-1,1))
                    y_u_agora = y_u_agora.reshape((-1,1))
                    ts_instantaneo = self.now
                    
                    # Estimativa inicial de y (var medida) e u (var não medida) #    
                    y = y_m_agora[:,0]
                    u = y_u_agora[:,0]
                    
                    ''' Reconciliação de Dados'''
                    # # Instancia classe #
                    # Reconciliacao_obj = Reconciliacao(Nvm, Nvu, nt)
                    # Resolve classe #
                    y_rec_agora, u_est_agora, Et, Erec, EBG_rec, flag = DR.Reconciliation(y, u, self.V)
                    
                    y_rec_agora = y_rec_agora.reshape((-1,1))
                    u_est_agora = u_est_agora.reshape((-1,1))
                    
                    
                    ''' Balanço de Energia '''
                    # Criando a estimativa inicial da variável não medida (temperatura do permeado):
                    if np.isnan(self.Tp[-1][-1]) == True:
                        Tp_guess = 37.0 + 273   # Convertendo [°C] -> [K]
                    else:
                        Tp_guess = self.Tp[-1][-1] + 273   # Convertendo [°C] -> [K]
                    args = args_BE(y_rec_agora, u_est_agora, y_m2_agora)
                    Tp_agora, info, Et2, _ = fsolve(BE, Tp_guess, args, xtol=1e-8, maxfev=100, full_output=True)
                    
                    
                    
                    # Desnormalizando as concentrações [0,1] -> % #
                    y_m_agora[:-5] = y_m_agora[:-5]*100
                    y_rec_agora[:-5] = y_rec_agora[:-5]*100
                    # Convertendo [K] -> [°C]
                    y_m2_agora[:2] = y_m2_agora[:2] - 273
                    Tp_agora = Tp_agora - 273  
                    Tp_agora = Tp_agora.reshape((-1,1))
                    
                    # Concatenando os dados para Janela Móvel:
                    print('#--------------------------------------------------------#')
                    print('JANELA DESLIZANDE - H=H_MAX')
                    print('self.n', self.n)
                    print('y_m.shape[1]', self.y_m.shape[1])
                    print('len(self.ts2)', len(self.ts2))
                    print('#--------------------------------------------------------#')
                    self.y_m = np.hstack((self.y_m[:,1:], y_m_agora))
                    self.y_rec = np.hstack((self.y_rec[:,1:], y_rec_agora))
                    self.u_est = np.hstack((self.u_est[:,1:], u_est_agora))
                    
                    self.y_m2 = np.hstack((self.y_m2[:,1:], y_m2_agora))
                    self.Tp = np.hstack((self.Tp[:,1:], Tp_agora))
                    
                    self.ts_deque.popleft()
                    self.ts_deque.append(ts_instantaneo)
                    self.ts2 = pd.DatetimeIndex(self.ts_deque)
                    
                    print('y_m.shape[1]', self.y_m.shape[1])
                    print('len(self.ts2)', len(self.ts2))
                    print('#--------------------------------------------------------#\n')
                    
                    
                    
                    #---------------------------------------------------------#
                    # Análise de bias:
                    #---------------------------------------------------------#
                        # Desvio-padrão das variáveis reconciliadas com spectro de var  # 
                    self.dp_rec = DR.Variance(self.y_rec, TJ=30, method='median', ddof=1)[2]
                        # Bias - erro grosseiro sistemático
                    self.bias = np.nanmedian(np.abs(self.y_m - self.y_rec), axis=1)/self.dp_rec
                    # self.bias = np.nanmedian(np.abs(self.y_m - self.y_rec), axis=1)/self.dp
                    #---------------------------------------------------------#
                    
                    
                    
                    #---------------------------------------------------------#
                    # Análise de outliers:
                    #---------------------------------------------------------#
                    self.F_sum, self.F_mean, self.F_median, self.MADn_Fobj = DR.DataAnalysis(self.y_m, self.y_rec, TJ=30)
                    
                    # Analise de Outliers e Fobj
                    self.nt = len(self.ts2)
                    self.out_x = np.argwhere(self.F_sum >= self.F_median+3*self.MADn_Fobj).ravel()
                    self.Outliers = np.zeros(len(self.out_x))
                    for j in range(len(self.out_x)):
                        for i in range(self.nt):
                            if self.out_x[j]==i:
                                self.Outliers[j]=self.F_sum[i]
                    
                    # print('self.F_sum', self.F_sum)
                    # print('self.F_mean', self.F_mean)
                    # print('self.out_x', self.out_x)
                    # print('len(self.out_x)', len(self.out_x))
                    # print('self.Outliers', self.Outliers)
                    # print('len(self.Outliers)', len(self.Outliers))
                    # print('self.nt', self.nt)
                    # print('len(self.F_sum)', len(self.F_sum))
                    #---------------------------------------------------------#
                    
                    
                    self.n += 1   
                    self.n2 += 1
            #---------------------------------------------------------------------------#
        
        
        
        ###############################################################################
        #              PROTEÇÃO CONTRA PARADA/PARTIDA DE OPERAÇÃO                     #
        ###############################################################################
        
        elif self.flag2 == False:
            
            
            if self.n == 0:  # primeiro ponto
                
                self.y_m = y_m_agora = y_m_agora.reshape((-1,1))
                self.y_m2 = y_m2_agora = y_m2.reshape((-1,1))
                
                self.ts_deque.append(self.now)
                self.ts2 = pd.DatetimeIndex(self.ts_deque)
                
                # Desnormalizando as concentrações [0,1] -> % #
                self.y_m[:-5,0] = self.y_m[:-5,0]*100
                # Convertendo [K] -> [°C]
                self.y_m2[:2,0] = self.y_m2[:2,0] - 273
                
                # Add NaN nas váriáveis não calculadas
                self.y_rec = np.empty((y_m_agora.shape[0],1))*np.nan
                self.u_est = np.empty((1,1))*np.nan
                self.Tp = np.empty((1,1))*np.nan
                
                
                
                self.n += 1
                self.n2 += 1
            else:
                
                if self.n < TamanhoMaximoJanela:
                    
                    y_m_agora = y_m_agora.reshape((-1,1))
                    y_m2_agora = y_m2.reshape((-1,1))
                    
                    ts_instantaneo = self.now
                    
                    
                    # Desnormalizando as concentrações [0,1] -> % #
                    y_m_agora[:-5] = y_m_agora[:-5]*100
                    # Convertendo [K] -> [°C]
                    y_m2_agora[:2] = y_m2_agora[:2] - 273
                    
                    # Add NaN nas váriáveis não calculadas
                    y_rec_agora = np.empty((y_m_agora.shape[0],1))*np.nan
                    u_est_agora = np.empty((1,1))*np.nan
                    Tp_agora = np.empty((1,1))*np.nan
                    
                    
                    # Concatenando os dados:
                    self.y_m = np.hstack((self.y_m, y_m_agora))
                    self.y_rec = np.hstack((self.y_rec, y_rec_agora))
                    self.u_est = np.hstack((self.u_est, u_est_agora))
                    
                    self.y_m2 = np.hstack((self.y_m2, y_m2_agora))
                    self.Tp = np.hstack((self.Tp, Tp_agora))
                    
                    self.ts_deque.append(ts_instantaneo)
                    self.ts2 = pd.DatetimeIndex(self.ts_deque) 
                    
                    print('y_m.shape[1]', self.y_m.shape[1])
                    print('len(self.ts2)', len(self.ts2))
                    
                    self.n += 1
                    self.n2 += 1
                else:
                    
                    y_m_agora = y_m_agora.reshape((-1,1))
                    y_m2_agora = y_m2.reshape((-1,1))
                    
                    ts_instantaneo = self.now
                    
                    
                    # Desnormalizando as concentrações [0,1] -> % #
                    y_m_agora[:-5] = y_m_agora[:-5]*100
                    # Convertendo [K] -> [°C]
                    y_m2_agora[:2] = y_m2_agora[:2] - 273
                    
                    # Add NaN nas váriáveis não calculadas
                    y_rec_agora = np.empty((y_m_agora.shape[0],1))*np.nan
                    u_est_agora = np.empty((1,1))*np.nan
                    Tp_agora = np.empty((1,1))*np.nan
                    
                    
                    # Concatenando os dados para Janela Móvel:
                    self.y_m = np.hstack((self.y_m[:,1:], y_m_agora))
                    self.y_rec = np.hstack((self.y_rec[:,1:], y_rec_agora))
                    self.u_est = np.hstack((self.u_est[:,1:], u_est_agora))
                    
                    self.y_m2 = np.hstack((self.y_m2[:,1:], y_m2_agora))
                    self.Tp = np.hstack((self.Tp[:,1:], Tp_agora))
                    
                    self.ts_deque.popleft()
                    self.ts_deque.append(ts_instantaneo)
                    self.ts2 = pd.DatetimeIndex(self.ts_deque)
                    
                    print('y_m.shape[1]', self.y_m.shape[1])
                    print('len(self.ts2)', len(self.ts2))
                    
                    self.n += 1
                    self.n2 += 1
            
        
        ###############################################################################
        #                   SALVANDO OS DADOS POR CONCATENAÇÃO                        #
        ###############################################################################
        global df_rec
        if df < 4:
            try:
                data = np.hstack((self.y_m[:,-1].T, self.y_rec[:,-1].T, self.u_est[:,-1].T, self.y_m2[:,-1].T, self.Tp[:,-1].T))
                df_rec = pd.DataFrame(data = data.reshape(1,-1), index = [self.now], columns=self.label)
                # Save the data
                df_rec.to_hdf('Membranas_DR_v0.4_teste('+self.start_date+').h5', key='df_RD', mode='a', format='table', append=True)
            except Exception as e:
                print(e)
        else:
            try:
                data = np.hstack((self.y_m[:,-1].T, self.y_rec[:,-1].T, self.u_est[:,-1].T, self.y_m2[:,-1].T, self.Tp[:,-1].T))
                df_rec = pd.DataFrame(data = data.reshape(1,-1), index = [self.now], columns=self.label)
                # Save the data
                df_rec.to_hdf('Membranas_DR_v0.4_teste('+self.start_date+').h5', key='df_RD', mode='a', format='table', append=True)
            except Exception as e:
                print(e)
        
        
        self.flag = True
            
        return self.y_rec, self.u_est, self.ts2, self.bias
    
#%%
###############################################################################
#                     AJUSTANDO LABELS PARA O DASH                            #
###############################################################################
            
# Labels para plots:
label = list(range(Nvm+1))
# label = main_var + ['Vazão permeado jusante as membranas de remoção de CO2']

# Reduzindo o texto do label y #
for i in range(Nvm-5):
    if i < 12:
        # main_var[i][0:25]
        label[i] =  'Feed - ' + main_var[i][-3:] + ' - [%]'    
    elif i < 24:
        # main_var[i][0:21]
        label[i] =  'Residue - ' + main_var[i][-3:] + ' - [%]'   
    elif i >= 24:
        # main_var[i][0:22]
        label[i] =  'Permeate - ' + main_var[i][-3:] + ' - [%]'      
label[-6] = 'Feed flow [kNm³/h]'
label[-5] = 'Residue flow [kNm³/h]'
label[-4] = 'Residue flow - A [kNm³/h]'
label[-3] = 'Residue flow - B [kNm³/h]'
label[-2] = 'Residue flow - C [kNm³/h]'
label[-1] = 'Permeate flow [kNm³/h]'

label2 = label
# for i in range(Nvm-5):
#     label2[i] = label2[i][0:-6] 

label3 = ['Feed flow temperature [°C]', 
        'Residue flow temperature [°C]', 
        'Residue flow pressure [bar]', 
        'Permeate flow pressure [bar]', 
        'Feed flow pressure [bar]']

label4 = label2[:-1] + label2[:-1] + [label2[-1]] + label3 + ['Permeate flow temperature [°C]']

#%%
###########################################################################
#               Dash DR - Monitoring and Analysis                         #
###########################################################################

# SETANDO O MONITORAMENTO:
TamanhoJanelaAquisicao = 12*5 # Janela de aquisição de dados de 5h (feq 5min - 12/h): n_amostragem/hora * hora
TamanhoMaximoJanela = int(12*24*1) # n_amostragem/hora * hora/dia * dia


# SETANDO O DASH:
sleep_time = 0.6    # Tempo de espera para atualizar dados (s)
# Reconciliação de Dados:
GL1 = 15             # Grau de liberdade: Nvm - (Nvm + Nvu - Ner)
chi2_u1 = chi2.ppf(0.995, GL1)       # Chi^2(99.5%,GL)
chi2_l1 = chi2.ppf(0.005, GL1)       # Chi^2(0.5%,GL)
# Estimação de Parâmetros:
GL2 = 14             # Grau de liberdade: NY-NP (nº de var avaliadas na Fobj - (nº var de entrada + nº de parâmetros))
chi2_u2 = chi2.ppf(0.995, GL2)       # Chi^2(99.5%,GL)
chi2_l2 = chi2.ppf(0.005, GL2)       # Chi^2(0.5%,GL)


# Para teste e debug fora da Petrobras -> Descomentar #
#---------------------------------------------------------------------------------------#
Sampling_min = 1/60*sleep_time
AmostragemSegundos = Sampling_min*60 + sleep_time
#---------------------------------------------------------------------------------------#

# Para teste e debug fora da Petrobras -> Comentar #
#---------------------------------------------------------------------------------------# 
# AmostragemSegundos = 5*60 + sleep_time # 5*60 (5 min freq amostral do processo)
#---------------------------------------------------------------------------------------#


# Eliminar mensagens no console de atualização do html - Dash (POST e GET)
logging.getLogger('werkzeug').setLevel(logging.ERROR)


# INSTANCIANDO A CLASSE MONITORAMENTO:
Dados = Monitoramento(TamanhoMaximoJanela, TamanhoJanelaAquisicao, label4, dados)
Dados.AtualizaDados()


# INSTANCIANDO O APP DASH:
external_scripts=['https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-MML-AM_CHTML']
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# external_stylesheets = ['https://codepen.io/juliepark/pen/odrjom.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, external_scripts=external_scripts)
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# Layout Style - background and color text:
#--------------------------------------------------------#
# default:
# colors = {'background': '#ffffff', 'color': '#000000'}

# custom clean:
# colors = {'background': '#ffffff', 'color': '#52575e'}
# colors = {'background': '#ffffff', 'color': '#3d424a'}

# colors = {'background': '#f5f5f5', 'color': '#52575e'}
# colors = {'background': '#f5f5f5', 'color': '#3d424a'}
# colors = {'background': '#f5f5f5', 'color': '#000000'}

# colors = {'background': '#fafafa', 'color': '#3d424a'}
colors = {'background': '#fafafa', 'color': '#52575e'}
# colors = {'background': '#fafafa', 'color': '#000000'}

# Custom dark (habilitar cores de grid):
# colors = {'background': '#414345', 'color': '#fafafa'}
# colors = {'background': '#414345', 'color': '#f5f5f5'}
# colors = {'background': '#414345', 'color': '#ffffff'}
#--------------------------------------------------------#


# GERANDO O LAYOUT HTML:
# Divisões, botões, gráficos e intervalos de atualizações da página:
app.layout = html.Div(style={'textAlign': 'center', 'color': colors['color'], 'background': colors['background']},
    children=[
        
        html.H2(children='FPSO CSP - Monitoring and Analysis'),
        
        html.H6(children='Membrane separation process: CO2 removal from natural gas'),
        
        html.Div(children='Web-app for Monitoring by Data Reconciliation and Parameters Estimation'),
        
        html.Button('Start', id='get-data-button', style = dict(color= '#028c00', backgroundColor= '#d4d4d4')),
        
        html.Div(id='output', children='Waiting for the start'),
        
        dcc.Tabs([
            
            # Tab de monitoramento:
            dcc.Tab(label='Monitoring', children=[
                
                html.Div(children=[
                    html.H6(children='Choose the variable for visualization:')]),
                
                html.Div([
                    html.Div([
                        dcc.Dropdown(
                            id='yaxis-column',
                            options=[{'label': label2[i], 'value': i} for i in range(len(label2[:-1]))],
                            value=len(label2[:-1])-5
                                ),
                            ],
                            style={'width': '20%', 'display': 'inline-block'})]),
                
                dcc.Graph(id='variables-graphic'),
        
                html.Div(children=[
                    html.H6(children='Soft-sensor - variable estimated by DR:')]),
        
                dcc.Graph(id='variables-graphic2'),
                
                html.Div(children=[
                    html.H6(children='Pressure and Temperature Monitoring:')]),
                
                html.Div([
                    html.Div([
                        dcc.Dropdown(
                            id='yaxis-column2',
                            options=[{'label': label3[i], 'value': i} for i in range(len(label3))],
                            value=0
                                ),
                            ],
                            style={'width': '20%', 'display': 'inline-block'})]),
                
                dcc.Graph(id='variables-graphic3'),
                
                dcc.Graph(id='variables-graphic4')
                
            ]),
            
            # Tab de análise de dados:
            dcc.Tab(label='Data Analysis', children=[
                
                html.Div(children=[
                    html.H6(children='Analysis of systematic gross errors - bias:')]),
                
                dcc.Graph(id='variables-graphic5'),
                
                html.Div(children=[
                    html.H6(children='Analysis of spurious gross errors - outliers:')]),
                
                dcc.Graph(id='variables-graphic6')
            ])
        ]),
        
        # Intervalos de atualizações do gráfico e dos dados:
        dcc.Interval(id='graph-update',
                        interval = sleep_time*1000,
                        max_intervals = 0,
                        n_intervals = 0),
        
        dcc.Interval(id='data-update',
                        interval = AmostragemSegundos*1000,
                        max_intervals = 0,
                        n_intervals = 0)
    ])



# CHAMADAS DE INTERAÇÕES ENTRE O LAYOUT HTML E AÇÕES DE CLIK DO MOUSE:
# Altera as cores do botão com os cliks no botão:
#-----------------------------------------------------------------------------#
@app.callback(Output('get-data-button', 'style'),
                [Input('get-data-button', 'n_clicks')])
def get_stylebutton(n_clicks):
    try:
        if (n_clicks % 2) == 0:
            style = dict(color = '#028c00', backgroundColor = '#d4d4d4')
        else:
            style = dict(color = '#ed3434', backgroundColor = '#dedede')
    except TypeError:
        style = dict(color = '#028c00', backgroundColor = '#d4d4d4')
    return style
#-----------------------------------------------------------------------------#


# Altera o nome do botão com os cliks no botão:
#-----------------------------------------------------------------------------#
@app.callback(Output('get-data-button', 'children'),
                [Input('get-data-button', 'n_clicks')])
def get_textbutton(n_clicks):
    try:
        if (n_clicks % 2) == 0:
            children = 'Start'
        else:
            children = 'Stop'
    except TypeError:
        children = 'Start'
    return children
#-----------------------------------------------------------------------------#


# Liga/desliga as atualizações dos dados com os cliks no botão:
#-----------------------------------------------------------------------------#
@app.callback(Output('data-update', 'max_intervals'),
                [Input('get-data-button', 'n_clicks')])
def start1(n_clicks):
    try:
        if (n_clicks % 2) == 0:
            max_intervals = 0
        else:
            max_intervals = -1
    except TypeError:
        max_intervals = 0
        
    return max_intervals
#-----------------------------------------------------------------------------#


# Liga/desliga as atualizações dos gráficos com os cliks no botão:
#-----------------------------------------------------------------------------#
@app.callback(Output('graph-update', 'max_intervals'),
                [Input('get-data-button', 'n_clicks')])
def start2(n_clicks):
    try:
        if (n_clicks % 2) == 0:
            max_intervals = 0
        else:
            max_intervals = -1
    except TypeError:
        max_intervals = 0
        
    return max_intervals
#-----------------------------------------------------------------------------#


# Liga, desliga e temporiza as atualizações dos dados:
#-----------------------------------------------------------------------------#
@app.callback(Output('output', 'children'),
                [Input('data-update', 'n_intervals'),
                Input('get-data-button', 'n_clicks')])
def data_graph(n, n_clicks):
    try:
        if (n_clicks % 2) == 0:
            children = 'Data Reconciliation stopped'
        else:
            if Dados.flag == True:
                Dados.AtualizaDados()
                time.sleep(sleep_time)
                children = 'Last data in: {} - Next data in: {}'.format(Dados.ts2[-1], Dados.ts2[-1]+datetime.timedelta(5/(24*60)))     
            elif Dados.flag == False:
                children = 'Waiting for the next sampling (+%dmin). The code is optimizing the data yet.'%(Sampling_min)
    except TypeError:
        children = 'Waiting for the start'
        
    return children
#-----------------------------------------------------------------------------#



# GERANDO OS GRÁFICOS NO LAYOUT HTML:
# Graphs 1 - Measured and Reconciled:
#-----------------------------------------------------------------------------#
@app.callback(Output('variables-graphic', 'figure'),
                [Input('graph-update', 'n_intervals'),
                Input('yaxis-column', 'value') ,
                Input('get-data-button', 'n_clicks')])
def update_graph(n, var_number, n_clicks):
    
    if n_clicks == None:
        y_m = np.zeros((Nvm,1))
        y_rec = np.zeros((Nvm,1))
        Datetime = []
    else:
        y_m = Dados.y_m
        y_rec = Dados.y_rec
        Datetime = Dados.ts2
        
    trace1 = go.Scatter(x = Datetime, y = y_m[var_number], name='Measured',
                        mode='markers', marker={'size': 9,
                                                'opacity': 0.85,
                                                'line': {'width': 0.5, 'color': 'white'}})
    trace2 = go.Scatter(x = Datetime, y = y_rec[var_number], name='Reconciled',
                        mode='markers', marker={'size': 6,
                                                'opacity': 0.85,
                                                'line': {'width': 0.5, 'color': 'white'}})
    layout = go.Layout(title='Monitoring by Data Reconciliation',
                        yaxis={'title': {
                                    'text': label[var_number],
                                    'font': {'color': colors['color'], 'size': 14}
                                    },
                                'tickfont': {'color': colors['color']}},
                        showlegend=True,
                        margin=dict(l=200, r=200, b=50, t=50, pad=4),
                        legend=dict(x=0, y=1.1),
                        legend_orientation='h',
                        font={'color': colors['color']},
                        # colorway= ['#0042d1', '#e87e0c'],
                        plot_bgcolor= colors['background'],
                        paper_bgcolor= colors['background'],
                        hovermode= 'closest')
    
    # if Dados.flag2 == True:
    #     traces = [trace1, trace2]
    # elif Dados.flag2 == False:
    #     traces = [trace1]
    
    traces = [trace1, trace2]
    
    return {'data': traces, 'layout': layout}
#-----------------------------------------------------------------------------#


# Graphs 2 - Estimated:
#-----------------------------------------------------------------------------#
@app.callback(Output('variables-graphic2', 'figure'),
                [Input('graph-update', 'n_intervals'),
                Input('get-data-button', 'n_clicks')])
def update_graph2(n, n_clicks):

    if n_clicks == None:
        u_est = []
        Datetime = []
    else:
        u_est = Dados.u_est.ravel()
        Datetime = Dados.ts2
    
    traces = go.Scatter(x = Datetime, y = u_est, name='Estimated',
                        mode='markers', marker={'size': 6,
                                                'opacity': 0.85,
                                                'color': 'green',
                                                'line': {'width': 0.5, 'color': 'white'}})
    layout = go.Layout(title='Soft-sensor - Permeate flow',
                        yaxis={'title': {
                                    'text': label2[-1],
                                    'font': {'color': colors['color'], 'size': 14}
                                    },
                                'tickfont': {'color': colors['color']}},
                        showlegend=True,
                        margin=dict(l=200, r=200, b=50, t=50, pad=4),
                        legend=dict(x=0, y=1.1),
                        legend_orientation='h',
                        font={'color': colors['color']},
                        colorway= ['#6be0fa', '#ed3434'],
                        plot_bgcolor= colors['background'],
                        paper_bgcolor= colors['background'],
                        hovermode= 'closest')
    
    
    return {'data': [traces], 'layout': layout}
#-----------------------------------------------------------------------------#


# Graphs 3 - Pressure and Temperature Measured:
#-----------------------------------------------------------------------------#
@app.callback(Output('variables-graphic3', 'figure'),
                [Input('graph-update', 'n_intervals'),
                Input('yaxis-column2', 'value') ,
                Input('get-data-button', 'n_clicks')])
def update_graph3(n, var_number, n_clicks):

    if n_clicks == None:
        y_m2 = np.zeros((Nvm2,1))
        Datetime = []
    else:
        y_m2 = Dados.y_m2
        Datetime = Dados.ts2
        
    traces = go.Scatter(x = Datetime, y = y_m2[var_number], name='Measured',
                        mode='markers', marker={'size': 9,
                                                'opacity': 0.85,
                                                'line': {'width': 0.5, 'color': 'white'}})
    layout = go.Layout(title='Pressure and Temperature Measured',
                        yaxis={'title': {
                                    'text': label3[var_number],
                                    'font': {'color': colors['color'], 'size': 14}
                                    },
                                'tickfont': {'color': colors['color']}},
                        showlegend=True,
                        margin=dict(l=200, r=200, b=50, t=50, pad=4),
                        legend=dict(x=0, y=1.1),
                        legend_orientation='h',
                        font={'color': colors['color']},
                        plot_bgcolor= colors['background'],
                        paper_bgcolor= colors['background'],
                        hovermode= 'closest')
    
    return {'data': [traces], 'layout': layout}
#-----------------------------------------------------------------------------#


# Graphs 4 - Soft-sensor - Permeation flow temperature:
#-----------------------------------------------------------------------------#
@app.callback(Output('variables-graphic4', 'figure'),
                [Input('graph-update', 'n_intervals'),
                Input('get-data-button', 'n_clicks')])
def update_graph4(n, n_clicks):

    if n_clicks == None:
        Tp = []
        Datetime = []
    else:
        Tp = Dados.Tp.ravel()
        Datetime = Dados.ts2
    
    traces = go.Scatter(x = Datetime, y = Tp, name='Calculated',
                        mode='markers', marker={'size': 6,
                                                'opacity': 0.85,
                                                'color': '#d15000',
                                                'line': {'width': 0.5, 'color': 'white'}})
    layout = go.Layout(title='Soft-sensor - Permeation flow temperature',
                        yaxis={'title': {
                                    'text': label4[-1],
                                    'font': {'color': colors['color'], 'size': 14}
                                    },
                                'tickfont': {'color': colors['color']}},
                        showlegend=True,
                        margin=dict(l=200, r=200, b=50, t=50, pad=4),
                        legend=dict(x=0, y=1.1),
                        legend_orientation='h',
                        plot_bgcolor= colors['background'],
                        paper_bgcolor= colors['background'],
                        font={'color': colors['color']},
                        hovermode= 'closest')
    
    return {'data': [traces], 'layout': layout}
#-----------------------------------------------------------------------------#


# Graphs 5 - Analysis of systematic gross errors - bias:
#-----------------------------------------------------------------------------#
@app.callback(Output('variables-graphic5', 'figure'),
                [Input('graph-update', 'n_intervals'),
                Input('get-data-button', 'n_clicks')])
def update_graph5(n, n_clicks):

    if n_clicks == None:
        bias = []
    else:
        bias = Dados.bias

    traces1 = go.Bar(x = label2[0:-1], y = bias, name = 'Bias (median)')
    traces2 = go.Scatter(x = label2[0:-1], y = 3*np.ones(Nvm), name='Confidence region of 99.7%',
                            line = dict(width=1, dash='dash'), mode='lines')
    layout = go.Layout(title='DR Error Analysis',
                        colorway= ['SkyBlue', 'red'], 
                        hovermode= 'closest',
                        plot_bgcolor= colors['background'],
                        paper_bgcolor= colors['background'],
                        font={'color': colors['color']},
                        margin=dict(l=150, r=150, b=80, t=80, pad=4),
                        legend=dict(x=0, y=1.1),
                        legend_orientation='h',
                        xaxis= {'title': {
                                    'text': "Variables",
                                    'font': {'color': colors['color'], 'size': 14}
                                    },
                                'tickfont': {'size': 9, 'color': colors['color']}},
                        yaxis= {'title': {
                                    'text': "Magnitude of bias error",
                                    'font': {'color': colors['color'], 'size': 14}
                                    },
                                'tickfont': {'color': colors['color']},
                                # 'gridcolor': '#bfbfbf',
                                # 'zerolinecolor': '#a3a3a3'
                                })
    
    return {'data': [traces1, traces2], 'layout': layout}
#-----------------------------------------------------------------------------#


# Graphs 6 - Analysis of spurious gross errors - outliers:
#-----------------------------------------------------------------------------#
@app.callback(Output('variables-graphic6', 'figure'),
                [Input('graph-update', 'n_intervals'),
                Input('get-data-button', 'n_clicks')])
def update_graph6(n, n_clicks):

    if n_clicks == None:
        traces1 = []
        traces2 = []
        traces3 = []
        traces4 = []
        traces5 = []
        traces6 = []
        traces7 = []
    else:
        traces1 = []
        traces2 = []
        traces3 = []
        traces4 = []
        traces5 = []
        traces6 = []
        traces7 = []
        if Dados.n >=2:
            F_sum = Dados.F_sum
            F_mean = Dados.F_mean
            F_median = Dados.F_median
            MADn_Fobj = Dados.MADn_Fobj
            out_x = Dados.out_x
            Outliers = Dados.Outliers
            Datetime = Dados.ts2
            nt = Dados.nt
            

            traces1 = go.Scatter(x = Datetime, y = F_sum, name='OF = WLS',
                                mode='markers', marker={'size': 9, 'opacity': 0.85, 'line': {'width': 0.5, 'color': 'white'}})
            traces2 = go.Scatter(x = Datetime, y = chi2_u1*np.ones(nt), name=f'χ²(99,5%,{GL1}) = {round(chi2_u1, 2)}',
                                    line = dict(width=1, dash='dash', color='green'), mode='lines')
            traces3 = go.Scatter(x = Datetime, y = chi2_l1*np.ones(nt), name=f'χ²(0,5%,{GL1}) = {round(chi2_l1, 2)}',
                                    line = dict(width=1, dash='dash', color='green'), mode='lines')
            traces4 = go.Scatter(x = Datetime, y = F_mean*np.ones(nt), name=f'Mean ={round(F_mean, 2)}',
                                    line = dict(width=2, dash='dash', color='gray'), mode='lines')
            traces5 = go.Scatter(x = Datetime, y = F_median*np.ones(nt), name=f'Median = {round(F_median, 2)}',
                                    line = dict(width=2, dash='dash', color='black'), mode='lines')
            traces6 = go.Scatter(x = Datetime, y = (F_median+3*MADn_Fobj)*np.ones(nt), name=f'Median + 3σ = {round(3*MADn_Fobj+F_median, 2)}',
                                    line = dict(width=1, dash='dash', color='red'), mode='lines')
            traces7 = go.Scatter(x = Datetime[out_x], y = Outliers, name=f'Outliers/Faults',
                                mode='markers', marker={'size': 6, 'opacity': 0.85, 'color': 'red', 'line': {'width': 0.5, 'color': 'white'}})
    layout = go.Layout(title='DR performance analysis',
                        xaxis= {'title': {
                                    'text': 'Samplings (frequency = 5min)',
                                    'font': {'color': colors['color'], 'size': 14}
                                    },
                                'tickfont': {'size': 9, 'color': colors['color']}},
                        yaxis={'title': {
                                    'text': 'Objective Function (OF)',
                                    'font': {'color': colors['color'], 'size': 14},
                                    }, 
                                'tickfont': {'color': colors['color']}},
                        showlegend=True,
                        margin=dict(l=150, r=150, b=80, t=80, pad=4),
                        legend=dict(x=0, y=1.1),
                        legend_orientation='h',
                        font={'color': colors['color']},
                        plot_bgcolor= colors['background'],
                        paper_bgcolor= colors['background'],
                        hovermode= 'closest')
    
    return {'data': [traces1, traces2, traces3, traces4, traces5, traces6, traces7], 'layout': layout}
#-----------------------------------------------------------------------------#


#%%
# Rodar
    

# Para teste e debug fora da Petrobras -> Comentar #
#---------------------------------------------------------------------------------------#
# host = socket.gethostbyname(socket.gethostname())
# 
# if __name__ == '__main__':
#     app.run(debug=False, host=host, port = 8080)
#---------------------------------------------------------------------------------------#


# Para teste e debug fora da Petrobras -> Descomentar #
#---------------------------------------------------------------------------------------# 
if __name__ == '__main__':
    app.run(debug=False, port=8100, host='127.0.0.1')
#---------------------------------------------------------------------------------------#