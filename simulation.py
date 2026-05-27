#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Laser simulation with parameters from Zhiqiang oscillating solitons

@author: khan
"""

import time
from pyqtgraph.Qt import QtWidgets
app = QtWidgets.QApplication([])
import pyqtgraph as pg
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from addict import Dict
from scipy.signal import find_peaks, peak_widths 

plt.close('all')

class LaserSim:
    
    c = 299792458                 # Speed of light [m/s]
    
    def __init__(self):
        ''' Set parameters '''
        self.wavelength0 = 1960            # Center wavelength [nm]
        self.deltaf = 350                   # Bandwidth of the simulation [THz]
        self.Nt     = 2**12                    # Number of points of the time and frequency arrays
        self.deltaw = ((self.wavelength0**2)/self.c)*self.deltaf*1e3
        # Architecture
        self.architecture = [['SMF',2.8], ['WG', 1e-3]]
            
        # Single-mode fiber parameters
        self.SMF = Dict()
        self.SMF.n = 1.46                 # Linear index
        self.SMF.n2 = 25                  # Nonlinear index [e-21 m^2/W]
        self.SMF.alpha = -0.0             # Attenuation [dB/m] /!\ to be checked
        self.SMF.D = 17.9                 # Dispersion [ps/nm/km]
        self.SMF.b3 = 0 #0.07             # Third order dispersion [ps/nm^2/km]
        self.SMF.MFD = 10                 # Mode field diameter [µm]
    
        # Waveguide
        self.WG = Dict()
        self.WG.n = 3.5                   # Linear index
        self.WG.n2 = 9.8e3                # Nonlinear index [e-21 m^2/W]
        self.WG.alpha = -0.0              # Attenuation [dB/m] /!\ to be checked
        self.WG.D   = 4                     # Dispersion [ps/nm/km]
        self.WG.b3  = 0 #0.07              # Third order dispersion [ps/nm^2/km]
        self.WG.b4  = 0 #0.07              # 4 order dispersion 
        self.WG.b5  = 0 #0.07              # 5 order dispersion 
        self.WG.b6  = 0 #0.07              # 6 order dispersion 
        self.WG.b7  = 0 #0.07              # 7 order dispersion 
        self.WG.b8  = 0 #0.07              # 8 order dispersion 
        self.WG.b9  = 0 #0.07              # 9 order dispersion 
        self.WG.b10 = 0 #0.07             # 10 order dispersion 
        self.WG.MFD = 0.50                # Need to check from comsol where the field becomes half in the waveguide, that width is our MFD    

        # Dispersion compensation fiber
        self.DCF = Dict()
        self.DCF.n = 1.46                 # Linear index=3;
        self.DCF.n2 = 25                  # Nonlinear index [e-21 m^2/W]
        self.DCF.alpha = -0.6             # Attenuation [dB/m]
        self.DCF.D = -44                  # Dispersion [ps/nm/km]
        self.DCF.b3 = -0.45               # Third order dispersion [ps/nm^2/km]
        self.DCF.MFD = 7.5                  # Effective area [µm]
            
        # Gain medium parameters
        self.EDF = Dict()
        self.EDF.Esat = 120               # Saturation energy [pJ]
        self.EDF.g0 = 15                  # Small signal gain [m^{-1}]
        self.EDF.wgc = 5*2*np.pi          # Gain curve bandwidth [THz]
        self.EDF.n = 1.46                 # Linear index
        self.EDF.n2 = 25                  # Nonlinear index of the doped fiber
        self.EDF.alpha = -0.0             # Attenuation [dB/m] /!\ to be checked
        self.EDF.D = -11                  # Dispersion of the doped fiber [ps/nm/km]
        self.EDF.b3 = 0                   # Third order dispersion [ps/nm^2/km] /!\
        self.EDF.MFD = 8.7                # Mode field diameter [µm]

        # Saturable absorber parameters
        self.Sat = Dict()
        self.Sat.T0 = 1 - 0.43             # Transmission of the saturable absorber (High power)
        self.Sat.deltaT = 0.19             # Modulation depth of the saturable absorber
        self.Sat.Psat = 100                # Saturation power [W]
        
        # Filter parameters
        self.Filter = Dict()
        self.Filter.deltaLambda = 10       # Width of the band-pass filter [nm]
        self.Filter.m_gaussian = 1         # Order of the gaussian filter
        
        # Laser architecture parameters
        self.spliceTrans = 0.9             # Transmission for each splice or connector
        self.couplerTrans = 0.1            # Loss for the output coupler
        
        # Simulation parameters
        self.varEmax = 1e-10               # If the variation of energy between 2 successive round-trips is below varEmax, simulation stops
        self.RTmax = 1                     # Max number of simulated round-trips
        self.dur0  = 4.4                   # Estimation of the shortest pulse [ps]
        #self.amp  = 0.5e3                  # power in [w]
        #self.N    = 1                     # Soliton number
        self.amp   = 2.0e3                   # power in [w]
        self.Ndz   = 150                   # Number of step in on typical length
        self.nplot = 10                    # Graph is updated every nplot round-trips
        self.nsave = 10                    # State is saved to a file every nsave round-trips
        self.nPlot = 1                     # Plot every nPlot round-trips

        # Initialize maps
        self.mapU = np.zeros((self.Nt, self.RTmax+1), dtype=np.cdouble)  # Initialization of arrays for storing results 
        self.mapV = np.zeros((self.Nt, self.RTmax+1), dtype=np.cdouble)  # dtype cdouble is double preciession for 'c' complex no.
        
    def processParameters(self):
        ''' Processing parameters '''
        # Frequency
        self.freq0 = self.c/(self.wavelength0*1e-9)/1e12        # Center frequency [THz]
        self.df = self.deltaf/self.Nt                           # Frequency increment [THz]
        self.dt = 1/(self.df*self.Nt)                           # Time increment [ps]
        self.dw = self.deltaw/self.Nt
        self.tt = np.arange(-self.Nt/2, self.Nt/2)*self.dt      # Time array [ps]
        self.ff = np.arange(-self.Nt/2, self.Nt/2)*self.df      # Frequency array [THz]
        # self.wavelength = self.c/(self.freq0 + self.ff)/1e3     # Wavelengths array [nm]
        self.wavelength = np.arange(-self.Nt/2,self.Nt/2)*self.dw + self.wavelength0
        self.om = 2*np.pi*self.ff             # Omega array relative to center omega [rad/ps]
        self.om2 = self.om**2                 # Omega^2 array (for dispersion calculations)
        self.om3 = self.om**3                 # Omega^3 array (for third order dispersion)
        self.om4 = self.om**4
        self.om5 = self.om**5 
        self.om6 = self.om**6 
        self.om7 = self.om**7 
        self.om8 = self.om**8 
        self.om9 = self.om**9 
        self.om10 = self.om**10 
    
        # Single-mode fiber
        self.SMF.Aeff = np.pi*(self.SMF.MFD/2)**2                              # Effective area [µm^2]   
        self.SMF.gamma = 2*np.pi*self.SMF.n2/(self.wavelength0*self.SMF.Aeff)  # Effective nonlinearity [/W/m]
        self.SMF.alpha = 0 #self.SMF.alpha*np.log(10)/10000                    # Linear loss  m^{-1}
        self.SMF.beta2 = -(self.wavelength0)**2*self.SMF.D/(2*np.pi*self.c)    # Second order dispersion
        self.SMF.beta3 = 1000*(self.wavelength0**2/(2*np.pi*self.c))**2*(self.SMF.b3+2*self.SMF.D/self.wavelength0)   # Third order dispersion [ps^3/m]
        
        # Waveguide
        self.WG.Aeff = np.pi*(self.WG.MFD/2)**2            # Effective area [µm^2]   
        self.WG.gamma = 2*np.pi*self.WG.n2/(self.wavelength0*self.WG.Aeff)  # Effective nonlinearity [/W/m]
        self.WG.alpha = 0 #self.SMF.alpha*np.log(10)/10000     # Linear loss  m^{-1}
        self.WG.beta2 = -(self.wavelength0)**2*self.WG.D/(2*np.pi*self.c)    # Second order dispersion
        self.WG.beta3 = 1000*(self.wavelength0**2/(2*np.pi*self.c))**2*(self.WG.b3+2*self.WG.D/self.wavelength0)   # Third order dispersion [ps^3/m]   
        self.WG.beta4 = -1e6 * (self.wavelength0**2 / (2 * np.pi * self.c))**3 * ( self.WG.b4 + 6 * self.WG.b3 / self.wavelength0 + 6 * self.WG.D / self.wavelength0**2)

        self.WG.beta5 = 1e9 * (self.wavelength0**2 / (2 * np.pi * self.c))**4 * ( self.WG.b5 + 8 * self.WG.b4 / self.wavelength0 + 24 * self.WG.b3 / self.wavelength0**2 + 24 * self.WG.D / self.wavelength0**3)

        self.WG.beta6 = -1e12 * (self.wavelength0**2 / (2 * np.pi * self.c))**5 * ( self.WG.b6 + 10 * self.WG.b5 / self.wavelength0 + 40 * self.WG.b4 / self.wavelength0**2 +120 * self.WG.b3 / self.wavelength0**3 + 120 * self.WG.D / self.wavelength0**4)

        self.WG.beta7 = 1e15 * (self.wavelength0**2 / (2 * np.pi * self.c))**6 * ( self.WG.b7 + 12 * self.WG.b6 / self.wavelength0 + 60 * self.WG.b5 / self.wavelength0**2 + 240 * self.WG.b4 / self.wavelength0**3 + 720 * self.WG.b3 / self.wavelength0**4 + 720 * self.WG.D / self.wavelength0**5)

        self.WG.beta8 = -1e18 * (self.wavelength0**2 / (2 * np.pi * self.c))**7 * ( self.WG.b8 + 14 * self.WG.b7 / self.wavelength0 + 84 * self.WG.b6 / self.wavelength0**2 + 420 * self.WG.b5 / self.wavelength0**3 + 1680 * self.WG.b4 / self.wavelength0**4 + 5040 * self.WG.b3 / self.wavelength0**5 + 5040 * self.WG.D / self.wavelength0**6)

        self.WG.beta9 = 1e21 * (self.wavelength0**2 / (2 * np.pi * self.c))**8 * ( self.WG.b9 + 16 * self.WG.b8 / self.wavelength0 + 112 * self.WG.b7 / self.wavelength0**2 + 672 * self.WG.b6 / self.wavelength0**3 + 3024 * self.WG.b5 / self.wavelength0**4 + 10080 * self.WG.b4 / self.wavelength0**5 + 25200 * self.WG.b3 / self.wavelength0**6 + 25200 * self.WG.D / self.wavelength0**7)

        self.WG.beta10 = -1e24 * (self.wavelength0**2 / (2 * np.pi * self.c))**9 * ( self.WG.b10 + 18 * self.WG.b9 / self.wavelength0 + 144 * self.WG.b8 / self.wavelength0**2 + 1008 * self.WG.b7 / self.wavelength0**3 + 5544 * self.WG.b6 / self.wavelength0**4 + 23760 * self.WG.b5 / self.wavelength0**5 + 79380 * self.WG.b4 / self.wavelength0**6 + 198000 * self.WG.b3 / self.wavelength0**7 + 198000 * self.WG.D / self.wavelength0**8)
        
       ## I can use this type of configuration in case the above does not work ##
# =============================================================================
#         # β3 [ps^3/m]
#         term = (self.wavelength0**2 / (2 * np.pi * self.c))
#         self.WG.beta3 = (term**2) * (2 * self.WG.D / self.wavelength0 + self.WG.b3)  # [s^3/m]
# 
#         # β4 [ps^4/m]
#         self.WG.beta4 = - (term**3) * (6 * self.WG.D / self.wavelength0**2 + 6 * self.WG.b3 / self.wavelength0 + self.WG.b4)
# 
#         # β5 [ps^5/m]
#         self.WG.beta5 = (term**4) * (24 * self.WG.D / self.wavelength0**3 + 36 * self.WG.b3 / self.wavelength0**2 + 12 * self.WG.b4 / self.wavelength0 + self.WG.b5)
# =============================================================================
       
        # Dispersion compensation fiber
        self.DCF.Aeff = np.pi*(self.DCF.MFD/2)**2            # Effective area [µm^2]
        self.DCF.gamma = 2*np.pi*self.DCF.n2/(self.wavelength0*self.DCF.Aeff)  # Effective nonlinearity [/W/m]
        self.DCF.alpha = self.DCF.alpha*np.log(10)/10000    # Linear loss  m^{-1}
        self.DCF.beta2 = -(self.wavelength0)**2*self.DCF.D/(2*np.pi*self.c)    # Second order dispersion
        self.DCF.beta3 = 1000*(self.wavelength0**2/(2*np.pi*3e8))**2*(self.DCF.b3+2*self.DCF.D/self.wavelength0)   # Third order dispersion [ps^3/m]
        
        # Gain fiber
        self.EDF.Aeff = np.pi*(self.EDF.MFD/2)**2            # Effective area [µm^2]
        self.EDF.gamma = 2*np.pi*self.EDF.n2/(self.wavelength0*self.EDF.Aeff)  # Effective nonlinearity [/W/m]
        self.EDF.alpha = self.EDF.alpha*np.log(10)/10000    # Linear loss  m^{-1}
        self.EDF.beta2 = -(self.wavelength0)**2*self.EDF.D/(2*np.pi*self.c)    # Second order dispersion
        self.EDF.beta3 = 1000*(self.wavelength0**2/(2*np.pi*3e8))**2*(self.EDF.b3+2*self.EDF.D/self.wavelength0)   # Third order dispersion [ps^3/m]
        
        # Filter 
        self.Filter.deltaFreq0 = self.freq0*self.Filter.deltaLambda/self.wavelength0 # Spectral width [THz]
        self.Filter.deltaOmega0 = self.Filter.deltaFreq0*np.pi*2
        self.Filter.wgmc = (2/np.log(2))*(self.Filter.deltaOmega0/2)**(2*self.Filter.m_gaussian)
        self.Filter.trans = np.exp(-(self.om**(2*self.Filter.m_gaussian))/self.Filter.wgmc)
        
        # Laser architecture
        self.alphagCoup = np.sqrt(self.couplerTrans)
        self.alphagRac = np.sqrt(self.spliceTrans)
        
        # Calculation of the FSR and overall dispersion of the cavity
        self.RTtime = 0                          # Round-trip [ns]
        self.netD = 0                            # Dispersion coeff.
        self.netBeta2 = 0                        # GVD
        print('Preparing simulation for:\n')
        for element in self.architecture:
            if element[0] == 'SMF':
                self.RTtime += 1e9*self.SMF.n*element[1]/self.c
                self.netD += self.SMF.D*element[1]
                self.netBeta2 += self.SMF.beta2*element[1]
                print(f'{element[1]:.2f} m of SMF with β₂={1000*self.SMF.beta2:.2f} ps²/km and γ={self.SMF.gamma:.3e} /W/m\n')
            elif element[0] == 'DCF':
                self.RTtime += 1e9*self.DCF.n*element[1]/self.c
                self.netD += self.DCF.D*element[1]
                self.netBeta2 += self.DCF.beta2*element[1]
                print(f'{element[1]:.2f} m of DCF with β₂={1000*self.DCF.beta2:.2f} ps²/km and γ={self.DCF.gamma:.3e} /W/m\n')
            elif element[0] == 'EDF':
                self.RTtime += 1e9*self.EDF.n*element[1]/self.c
                self.netD += self.EDF.D*element[1]
                self.netBeta2 += self.EDF.beta2*element[1]
                print(f'{element[1]:.2f} m of EDF with β₂={1000*self.EDF.beta2:.2f} ps²/km and γ={self.EDF.gamma:.3e} /W/m\n')
            elif element[0] == 'WG':
                self.RTtime += 1e9*self.WG.n*element[1]/self.c
                self.netD += self.WG.D*element[1]
                self.netBeta2 += self.WG.beta2*element[1]
                print(f'{element[1]:.2f} m of WG with β₂={1000*self.WG.beta2:.2f} ps²/km and γ={self.WG.gamma:.3e} /W/m\n')
        self.FSR = 1e3/self.RTtime                # Free spectral range [MHz]
        
        print("FSR = %.1f MHz, Net GVD = %.1e, Net Beta2 = %.1e"%(self.FSR, self.netD, self.netBeta2))
            
    def initialCondition(self):
        ''' Initial field in the cavity '''
        self.Init = Dict()
        # self.Init.noiseLevel = 10**(-18/10)          # Noise level [W]
        # self.Init.pulseAmp = 0.05                    # Amplitude of the initial pulse (0 if starting from noise) [sqrt(W)]
        # self.Init.pulseDur = 4                       # Duration of the intial pulse [ps]
        
        # # Create array
        # self.Init.xr = np.random.rand(self.Nt)            # Noise for the amplitude
        # self.Init.xi = np.random.rand(self.Nt)            # Noise for the phase
        # self.Init.U1 = self.Init.noiseLevel*np.sqrt(-np.log(self.Init.xr))*np.exp(2*1j*np.pi*self.Init.xi) \
        #     + self.Init.pulseAmp*np.exp(-np.log(2)*(2*self.tt/self.Init.pulseDur)**2)        # Array of the first time-domain signal
        
        # # Soliton
        solitonAmp =  np.sqrt(self.amp)/np.cosh(self.tt/self.dur0)
        self.Init.U1 = solitonAmp
        
        # Put initial condition into U
        self.Init.V1 = np.fft.fftshift(np.fft.fft(self.Init.U1))
        self.U = self.Init.U1
        self.V = self.Init.V1
        
    def loopInitialization(self):
        ''' Initialize the arrays that will store the cavity state at each round trip '''
        self.E0 = 1e-10                                             # Stores the energy of the previous round-trip
        self.E = np.trapz(np.abs(self.U*np.conj(self.U)), self.tt)       # Energy of current round-trip [pJ]
        self.Etab = np.array([self.E])            # Array to store the energy of each round-trip
        self.nRT = 0                         # Current number of round-trip
        self.mapU = np.zeros((self.Nt, self.RTmax+1), dtype=np.cdouble)  # Initialization of arrays for storing results
        self.mapV = np.zeros((self.Nt, self.RTmax+1), dtype=np.cdouble)
        self.mapU[:,0] = self.U
        self.mapV[:,0] = np.fft.fftshift(np.fft.fft(self.U))
        self.initGraph()

    def loop(self):
        ''' Actual simulation '''
        while self.nRT < self.RTmax: #(np.abs(self.E-self.E0)/self.E0 > self.varEmax and self.nRT < self.RTmax):
            self.nRT += 1                         # Increment round-trip number
            self.E0 = self.E                      # Energy of previous round-trip
            self.vec_z = []
            self.matU = []
            self.matV = []
            for element in self.architecture:
                if element[0] == 'SMF':
                    self.propagSMF(element[1])
                    # self.U = self.U*self.alphagRac  # One splice with loss
                if element[0] == 'WG':
                    self.propagWG(element[1])
                if element[0] == 'DCF':
                    self.propagDCF(element[1])
                    self.U = self.U*self.alphagRac  # One splice with loss
                if element[0] == 'EDF':
                    self.propagEDF(element[1])
                    self.U = self.U*self.alphagRac  # One splice with loss
                if element[0] == 'Sat':
                    self.transSatAbs()
                    self.U = self.U*self.alphagRac  # One splice with loss
                if element[0] == 'Filt':
                    self.transFilter()
                    self.U = self.U*self.alphagRac  # One splice with loss
                if element[0] == 'Coupl':
                    self.U = self.U*self.alphagCoup # Through the output coupler
                    self.U = self.U*self.alphagRac  # One splice with loss

            self.V = np.fft.fftshift(np.fft.fft(self.U))
            self.E = np.trapz(np.abs(self.U*np.conj(self.U)), self.tt)
            self.Etab = np.append(self.Etab, self.E)
            self.mapU[:,self.nRT] = self.U
            self.mapV[:,self.nRT] = self.V

            if self.nRT%self.nPlot == 0:
                self.updateGraph()

        # End of loop plotting with matplotlib
        # win.close()
        # self.endPlot()
        # self.plotPcolor()
        
    def propagSMF(self, length):
        ''' Solve propagation equation in the SMF fiber '''
        # Calculate the step dz
        Pp = np.abs(np.max(self.U*np.conj(self.U)))             # Peak power
        L_NL = 1/(self.SMF.gamma*Pp)                            # Nonlinear length
        L_D = self.dur0**2/np.abs(self.SMF.beta2)               # Dispersion length
        Lmin = np.min([L_NL, L_D])
        dz = length/np.ceil(self.Ndz*length/Lmin)               # Simulation step
        z = 0
        
        # Propagation with NLSE solving and split-step Fourier
        while z <= length:
            linop = np.exp(dz*1j*self.SMF.beta2*self.om2/2 +        # Linear operator with 2nd order dispersion...
                       dz*1j*self.SMF.beta3*self.om3/6 +        # third order dispersion...
                       dz*self.SMF.alpha/2)                     # linear loss
            linops = np.fft.fftshift(linop)                         # so that we don't have to do fftshifts in the loop
            self.U = self.U*np.exp(1j*dz*self.SMF.gamma*self.U*np.conj(self.U))    # Nonlinear step
            self.V = np.fft.fft(self.U)*linops                            # Linear step in Fourier
            self.U = np.fft.ifft(self.V)                                  # Back to time domain
            self.matU.append(self.U)                                      # Matrix to save the change in U (Pulse shape)
            self.matV.append(np.fft.fftshift(self.V))                     # Matrix to save the change in V (Spectrum)
            self.vec_z.append(z)
            z += dz
        
    def propagWG(self, length):
        ''' Solve propagation equation in the WG fiber '''
        # Calculate the step dz
        Pp = np.abs(np.max(self.U*np.conj(self.U)))            # Peak power
        L_NL = 1/(self.WG.gamma*Pp)                            # Nonlinear length
        L_D = self.dur0**2/np.abs(self.WG.beta2)               # Dispersion length
        dz = length/np.ceil(self.Ndz)               # Simulation step
        z = 0
        
        
        # Propagation with NLSE solving and split-step Fourier
        while z <= length:
            linop = np.exp(dz*1j*self.WG.beta2*self.om2/2 +        # Linear operator with 2nd order dispersion...
                       dz*1j*self.WG.beta3*self.om3/6 +            # third order dispersion...
# =============================================================================
#                        dz*1j*self.WG.beta4*self.om4/24 +
#                        dz*1j*self.WG.beta5*self.om5/120 +
#                        dz*1j*self.WG.beta6*self.om6/720 +
#                        dz*1j*self.WG.beta7*self.om7/5040 +
#                        dz*1j*self.WG.beta8*self.om8/40320 +
#                        dz*1j*self.WG.beta9*self.om9/362880 +
#                        dz*1j*self.WG.beta10*self.om10/3628800 +
# =============================================================================
                       dz*self.WG.alpha/2)                         # linear loss
            linops = np.fft.fftshift(linop)                        # so that we don't have to do fftshifts in the loop
            self.U = self.U*np.exp(1j*dz*self.WG.gamma*self.U*np.conj(self.U))    # Nonlinear step
            self.V = np.fft.fft(self.U)*linops                            # Linear step in Fourier
            self.U = np.fft.ifft(self.V)                                  # Back to time domain
            
            self.matU.append(self.U)                                      # Matrix to save the change in U (Pulse shape)
            self.matV.append(np.fft.fftshift(self.V))                     # Matrix to save the change in V (Spectrum)
            self.vec_z.append(z)
            z += dz 

    def propagEDF(self, length):
        ''' Solves the propagation equation in the EDF fiber (with gain) '''
        # Calculate the step dz
        Pp = np.max(np.abs(self.U*np.conj(self.U)))             # Peak power
        L_NL = 1/(self.EDF.gamma*Pp)                            # Nonlinear length
        L_D = self.dur0**2/np.abs(self.EDF.beta2)               # Dispersion length
        Lmin = np.min([L_NL, L_D])
        dz = length/np.ceil(self.Ndz*length/Lmin)               # Simulation step
        z = 0
        
        # Propagation with NLSE solving and split-step Fourier
        while z <= length:
            P = np.abs(self.U*np.conj(self.U))
            E = np.trapz(P, self.tt)
            g = self.EDF.g0*np.exp(-E/self.EDF.Esat)*(np.ones((self.Nt)) - self.om2/self.EDF.wgc**2)
            linop = np.exp(dz*1j*self.EDF.beta2*self.om2/2 +        # Linear operator with 2nd order dispersion...
                           dz*1j*self.EDF.beta3*self.om3/6 +        # Third order dispersion...
                           dz*(self.EDF.alpha + g)/2)               # Linear loss and gain
            linops = np.fft.fftshift(linop)                 # so that we don't have to do fftshifts in the loop
            self.U = self.U*np.exp(1j*dz*self.EDF.gamma*P)  # Nonlinear step
            self.V = np.fft.fft(self.U)*linops              # Linear step in Fourier
            self.U = np.fft.ifft(self.V)                    # Back to time domain
            z += dz
        
    def propagDCF(self, length):
        ''' Solves the propagation equation in the DCF fiber '''
        # Calculate the step dz
        Pp = np.abs(np.max(self.U*np.conj(self.U)))         # Peak power
        L_NL = 1/(self.DCF.gamma*Pp)                        # Nonlinear length
        L_D = self.dur0**2/np.abs(self.DCF.beta2)           # Dispersion length
        Lmin = np.min([L_NL, L_D])
        dz = length/np.ceil(self.Ndz*length/Lmin)           # Simulation step
        
        linop = np.exp(dz*1j*self.DCF.beta2*self.om2/2 +    # Linear operator with 2nd order dispersion...
                       dz*1j*self.DCF.beta3*self.om3/6 +    # third order dispersion...
                       dz*self.DCF.alpha/2)                 # linear loss
        linops = np.fft.fftshift(linop)                     # so that we don't have to do fftshifts in the loop
        z = 0
        
        # Propagation with NLSE solving and split-step Fourier
        while z <= length:
            self.U = self.U*np.exp(1j*dz*self.DCF.gamma*self.U*np.conj(self.U))    # Nonlinear step
            self.V = np.fft.fft(self.U)*linops                            # Linear step in Fourier
            self.U = np.fft.ifft(self.V)                                  # Back to time domain
            z += dz

    def transFilter(self):
        ''' Applies the transmission of the filter '''
        self.V = np.fft.fft(self.U)
        self.V = self.V*np.fft.fftshift(self.Filter.trans)
        self.U = np.fft.ifft(self.V)

    def transSatAbs(self):
        ''' Calculate and applies the transfer function of the saturable absorber
        '''
        P = self.U*np.conj(self.U)                        # Power 
        T = self.Sat.T0 - self.Sat.deltaT/(1 + P/self.Sat.Psat)  # Saturable absorber transfer function
        self.U = self.U*np.sqrt(T)

    def initGraph(self):
        ''' Initialize the graphical window '''
        self.app = QtWidgets.QApplication([])
        pg.setConfigOptions(antialias=True, background='w', foreground='k')
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        self.win = pg.GraphicsLayoutWidget(show=True, title="Laser cavity simulation")

        self.win.resize(1000, 600)
        self.win.setWindowTitle("Laser cavity simulation")
        
        self.win.activateWindow()        # Bring on top
        
        # First plot: time intensity
        self.p1 = self.win.addPlot(title="Intensity [W]")
        self.curve1 = self.p1.plot(self.tt, np.abs(self.Init.U1)**2, pen=(78, 121, 167))
        self.p1.setLabel('left', 'Intensity [W]')
        self.p1.setLabel('bottom', 'Time [ps]')
        self.p1.setLimits(xMin=np.min(self.tt), xMax=np.max(self.tt), yMin=0)
        
        # Second plot: time phase
        self.p2 = self.win.addPlot(title="Phase")
        self.curve2 = self.p2.plot(self.tt, np.angle(self.Init.U1), pen=(242, 142, 43))
        self.p2.setLabel('left', 'Phase')
        self.p2.setLabel('bottom', 'Time [ps]')
        self.p2.setLimits(xMin=np.min(self.tt), xMax=np.max(self.tt), yMin=-np.pi, yMax=np.pi)
        
        # Third plot: spectrum intensity
        self.win.nextRow()
        self.p3 = self.win.addPlot(title="Spectrum [dB]")
        self.curve3 = self.p3.plot(self.ff, 10*np.log10(np.abs(np.fft.fftshift(np.fft.fft(self.Init.U1)*self.dt))**2), pen=(225,87,89)) # dt is for normalization of the FFT
        self.p3.setLabel('left', 'Spectrum [dB]')
        self.p3.setLabel('bottom', 'Frequency [THz]')
        self.p3.setLimits(xMin=0.5*np.min(self.ff), xMax=0.5*np.max(self.ff))
        # p3.setLimits(xMin=np.min(self.ff), xMax=np.max(self.ff), yMin=-50, yMax=50)
        self.p3.setYRange(-50, 30)
        self.p3.enableAutoRange('xy', False)
        
        # Fourth plot: energy evolution with round-trips
        self.p4 = self.win.addPlot(title="Energy [pJ]")
        self.curve4 = self.p4.plot(np.array([0]), np.array([np.trapz(np.abs(self.Init.U1*np.conj(self.Init.U1)), self.tt)]), pen=(118, 183, 178))
        self.p4.setLabel('left', 'Energy [pJ]')
        self.p4.setLabel('bottom', 'Round-trip')
        self.p4.setLimits(xMin=0)

    def updateGraph(self):
        ''' Updates the plotting '''
        self.curve1.setData(self.tt, np.abs(self.U*np.conj(self.U)))
        self.curve2.setData(self.tt, np.angle(self.U))
        spectrum = 10*np.log10(np.abs(self.V*self.dt*np.conj(self.V*self.dt)))
        spectrum[spectrum == -np.inf] = -100
        self.curve3.setData(self.ff, spectrum)
        self.curve4.setData(np.arange(self.nRT+1), self.Etab)
        pg.QtWidgets.QApplication.processEvents()
        
    def endPlot(self):
        ''' Plots the results with matplotlib, for interactivity '''
        # Center time-domain array
        barycenter = np.round(np.sum(np.abs(self.U)**2*np.arange(self.Nt))/np.sum(np.abs(self.U)**2))
        U1 = np.roll(self.U, int(self.Nt/2-barycenter))

        # Setup plot
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
        
        ax1.set_xlim(np.min(self.tt), np.max(self.tt))
        ax1.set_ylim(auto=True)
        ax1.set_xlabel("Time [ps]")
        ax1.set_ylabel("P [W]")
        line1, = ax1.plot(self.tt, np.abs(U1)**2, 'C0')
        
        ax2.set_xlim(np.min(self.tt), np.max(self.tt))
        ax2.set_ylim(-np.pi, np.pi)
        ax2.set_xlabel("Time [ps]")
        ax2.set_ylabel("Phase")
        line2, = ax2.plot(self.tt, np.angle(U1), 'C1')
        
        ax3.set_xlim(np.min(self.ff)/3, np.max(self.ff)/3)
        ax3.set_ylim(-50, 50)
        ax3.set_xlabel("Frequency [THz]")
        ax3.set_ylabel("Power [dB]")
        line3, = ax3.plot(self.ff, 10*np.log10(np.abs(self.V*self.dt)**2), 'C2')
        
        ax4.set_xlabel("Round-trip number")
        ax4.set_ylabel("Energy [pJ]")
        line4, = ax4.plot(np.arange(self.Etab.shape[0])*self.nPlot, self.Etab, 'C3')
        
        plt.tight_layout()
        plt.draw()
        
    def plotPcolor(self):
        ''' Pcolor graph of the evolution of U and V '''
        
        fig, axs = plt.subplots(1, 2, figsize=(11,6))
        # c1 = axs[0].pcolorfast(self.tt, np.arange(0, self.RTmax), 10*np.log10(np.abs(self.mapU.T*np.conj(self.mapU.T))))
        c1 = axs[0].pcolorfast(self.tt, np.arange(0, self.RTmax), np.abs(self.mapU.T*np.conj(self.mapU.T)))
        axs[0].set_xlabel('Time [ps]'), axs[0].set_ylabel('Round-trip')
        axs[0].set_ylim(0, self.RTmax), #axs[0].set_xlim(np.min(self.tt)/2, np.max(self.tt/2))
        
        c3 = axs[1].pcolorfast(self.ff, np.arange(0, self.RTmax), 10*np.log10(np.abs(self.mapV.T*self.dt)**2), vmin=0)
        axs[1].set_xlabel('Frequency [THz]'), axs[1].set_ylabel('Round-trip')
        axs[1].set_ylim(0, self.RTmax), axs[1].set_xlim(np.min(self.ff), np.max(self.ff))
        plt.show()
        
# Actually doing some stuff


laser = LaserSim()
laser.processParameters()
laser.initialCondition()
laser.loopInitialization()
laser.loop()

#%%

plt.figure()
plt.plot(laser.tt, np.abs(laser.Init.U1)**2)
plt.plot(laser.tt, np.abs(laser.U)**2)


#%% calculate the pulse duration 
I_in  = abs(laser.Init.U1)**2
I_out = abs(laser.U)**2
#input pulse duration
peaks, _     = find_peaks(I_in, height=0)
results_half = peak_widths(I_in, peaks, rel_height=0.5)
tFWHM_in     = max(results_half[0])*laser.dt
#output pulse duration
peaks, _     = find_peaks(I_out, height=0)
results_half = peak_widths(I_out, peaks, rel_height=0.5)
tFWHM_out     = max(results_half[0])*laser.dt
# result for each dz 
                                    
It_dz = np.abs(laser.matU)**2
Iwl_dz = 10*np.log10(np.abs(laser.matV)**2)
# easy to recall
vec_z = np.array(laser.vec_z)
t = laser.tt
wl = laser.wavelength
#%% plt intial vs finale pulse shape
fig , axs = plt.subplots(1,2,figsize=(10, 5))

axs[0].plot(laser.tt, I_in,'k',label='Intial pulse')
axs[0].plot(laser.tt,I_out,'r',label='Output pulse')
#axs[0].set_xlim(-1,1)
axs[0].set_ylabel('Power [W]') ; axs[0].set_xlabel('Time [ps]')
axs[0].text(0.35,max(I_in)/2, f't_in = {tFWHM_in*1e3 :.1f} fs')
axs[0].text(0.35,max(I_out)/2, f't_out = {tFWHM_out*1e3 :.1f} fs')
axs[0].set_title('Evolution of Pulse')
axs[0].legend()

axs[1].plot(laser.wavelength, 10*np.log10(abs(laser.Init.V1)**2),'k',label='Intial pulse')
axs[1].plot(laser.wavelength, 10*np.log10(abs(laser.V)**2),'r',label='output pulse')
# axs[1].set_xlim(laser.wavelength0-50,laser.wavelength0+50)
axs[1].set_ylim(0,100) ; axs[1].set_ylabel('Power [dB]') ; axs[1].set_xlabel('Wavelength [nm]')
axs[1].set_title('Spectal Evolution')
axs[1].legend()

#%% plt pulse during the propagation along the waveguide 

# Waveguide propagation

# =============================================================================
# fig, axs = plt.subplots(1, 2, figsize=(12, 6)) 
# 
# pc0 = axs[0].pcolorfast(t*1e3, vec_z*1e3, It_dz, cmap='jet')
# axs[0].set_xlim(-500, 500)
# axs[0].set_ylabel('Waveguide length [mm]')
# axs[0].set_xlabel('Time [fs]')
# axs[0].set_title('Evolution of Pulse propagating in Waveguide')
# cbar0 = fig.colorbar(pc0, ax=axs[0])
# cbar0.set_label('Pulse amplitude')
# 
# pc1 = axs[1].pcolorfast(wl, vec_z*1e3, Iwl_dz, cmap='jet')
# axs[1].set_ylabel('Waveguide length [mm]')
# axs[1].set_xlabel('Wavelength [nm]')
# axs[1].set_title('Spectral Evolution')
# cbar1 = fig.colorbar(pc1, ax=axs[1])
# cbar1.set_label('Intensity [dB]')  
# 
# =============================================================================

#%%

# SMF propagation

fig, axs = plt.subplots(1, 2, figsize=(12, 6)) 

pc0 = axs[0].pcolorfast(t*1e3, vec_z, It_dz, cmap='jet')
#axs[0].set_xlim(-500, 500)
axs[0].set_ylabel('SMF length [m]')
axs[0].set_xlabel('Time [fs]')
axs[0].set_title('Evolution of Pulse propagating in Fiber')
cbar0 = fig.colorbar(pc0, ax=axs[0])
cbar0.set_label('Pulse amplitude')

pc1 = axs[1].pcolorfast(wl, vec_z, Iwl_dz, cmap='jet')
axs[1].set_ylabel('SMF length [m]')
axs[1].set_xlabel('Wavelength [nm]')
axs[1].set_title('Spectral Evolution')
cbar1 = fig.colorbar(pc1, ax=axs[1])
cbar1.set_label('Intensity [dB]')  

#%%
