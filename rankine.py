# Sam Rankine Cycle

import numpy as np  # for some numerical methods
import pandas as pd # for data analysis tools like dataframes
import math         # duh
import matplotlib   # for pretty pictures
matplotlib.use('Agg') # to get matplotlib to save figures to a file instead of using X windows
import matplotlib.pyplot as plt

# Given properties

# these pressures must exist in the saturation table
# ... later add function to create new record of interpolated data in between
# pressure points if the user selects a pressure that isn't in the saturation table
p_lo = 0.008 # low pressure, in MPa (condenser pressure)
p_hi = 8.0 # high pressure, in MPa (boiler pressure)

# read in table values
h2o_psat = pd.read_csv('H2O_PresSat.csv')
h2o_psat = h2o_psat.dropna(axis=1) #remove last NaN column
#print h2o_psat
h2o_tsat = pd.read_csv('H2O_TempSat.csv')
h2o_tsat = h2o_tsat.dropna(axis=1) #remove last NaN column
#print h2o_tsat
# merge the psat and tsat tables into one saturated table
h2o_sat = pd.concat([h2o_psat,h2o_tsat], axis=0, join='outer', join_axes=None, ignore_index=True,
                    keys=None, levels=None, names=None, verify_integrity=False)

h2o_sat = h2o_sat.sort('P')
h2o_comp = pd.read_csv('H2O_Compressed.csv')
h2o_comp = h2o_comp.dropna(axis=1) #remove last NaN column
#print h2o_comp

# begin computing processess for rankine cycle
fig = plt.figure(1)
plt.figure(1).suptitle("Rankine Cycle T-s Diagram \n Blue = adiabatic \n Green = isentropic")
plt.xlabel("Entropy (kJ/kg.K)")
plt.ylabel("Temperature (deg C)")

# State 1, saturated vapor at high pressure
# assume that this isn't a superheated rankine cycle, so state 2 is saturated vapor at pressure p_hi
s1 = h2o_sat[h2o_sat['P']==p_hi]['sg'].values[0]
h1 = h2o_sat[h2o_sat['P']==p_hi]['hg'].values[0]

# State 2, two-phase at low pressure
s2 = s1  # ideal rankine cycle
# find h_3 from s_2 and p_lo. first get the quality x_3
sf =  h2o_sat[h2o_sat['P']==p_lo]['sf'].values[0]
sg =  h2o_sat[h2o_sat['P']==p_lo]['sg'].values[0]
x2 = (s2 - sf)/(sg - sf) # quality at state 3
hf =  h2o_sat[h2o_sat['P']==p_lo]['hf'].values[0]
hg =  h2o_sat[h2o_sat['P']==p_lo]['hg'].values[0]
h2 = x2 * (hg - hf) + hf

# State 3, saturated liquid at low pressure
s3 =  h2o_sat[h2o_sat['P']==p_lo]['sf'].values[0]
h3 =  h2o_sat[h2o_sat['P']==p_lo]['hf'].values[0]

# State 4, sub-cooled liquid at high pressure
s4 = s3 # ideal rankine cycle
# assuming incompressible isentropic pump operation, let W/m = v*dp with v4 = v3
v3 = h2o_sat[h2o_sat['P']==p_lo]['vf'].values[0]
wp = v3*(p_hi - p_lo)*(10**3) # convert MPa to kPa
h4 = h3 + wp

# Find work and heat for each process
wt = h1 - h2
qb = h1 - h4
wnet = wt - wp
qnet = wnet
qc = qnet - qb

# Find thermal efficiency for cycle
eta = wnet / qb

# Find back work ratio
bwr = wp / wt

# print values to screen
print('h1 = {:.2f}'.format(h1))
print('h2 = {:.2f}'.format(h2))
print('h3 = {:.2f}'.format(h3))
print('v3 = {:.2f}'.format(v3))
print('h4 = {:.2f}'.format(h4))
print('wt = {:.2f}'.format(wt))
print('wp = {:.2f}'.format(wp))
print('qb = {:.2f}'.format(qb))
print('qc = {:.2f}'.format(qc))
print('eta = {:.2f}'.format(eta))
print('bwr = {:.2f}'.format(bwr))

# save figure to directory
# fig.savefig("graph.png")