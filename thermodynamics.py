# Create Python class for a thermodynamic state

#import pandas as pd.... never mind, just use CoolProp for the fluid data
import CoolProp.CoolProp as CP  #must have CoolProp library installed

# def class fluid_props(subcooled_csv, saturated_csv, superheated_csv):
#     ''' This class is a pandas panel of three data frames that define the fluid properties. The inputs are the filenames of the .csv's that contain the fluid data. The saturated_csv can be one filename or a list of filenames (such as saturated data listed by pressure or by temperature) that will be combined into one dataframe'''
#     # how do I structure this pandas panel of three data frames?
    # idea: use MultiIndex to index the subcooled and superheated data frames by both pressure and temperature



class State(object):
    ''' This is a class that can be used to define a thermodynamic state for a given fluid. The user must enter the fluid string to select in CoolProp and then 2 independent named variables for the state to be properly defined. All variables are specific, in that they are valued per unit mass. Optional variables and their default units are:
        T = temperature, (deg C)
        p = pressure, (MPa)
        v = specific volume (m^3/kg)
        d = density (kg/m^3)
        u = internal energy (kJ/kg)
        h = enthalpy (kJ/kg)
        s = entropy (kJ/kg.K)
        x, Q = quality (real number between 0 and 1 inclusive)
        velocity = velocity (m/s) for kinetic energy
        z = relative height (m) for potential energy
    '''
    def __init__(self,fluid,**kwargs):
        self.fluid = fluid
        state_vars = ['T','P','D','V','U','H','S','X','Q']
        # note that 'x' and 'Q' both represent two-phase quality
        key1 = '', value1 = '', key2 = '', value2 = ''
        for key, value in kwargs.items():
            if key = 'name':
                self.__name = value # 1, 2, 2s, 3, 4, 4s, 4b, etc.
            key.upper() #convert to uppercase
            if key in state_vars:
                if key == 'X':
                    key = 'Q'  # for CoolProp
                if key == 'V':
                    key = 'D'
                    value = 1/value  # use denisty for CoolProp
                if key1 != '':
                    key1 = key
                    value1 = value
                    continue
                if key2 != '':
                    key2 = key
                    value2 = value
                    continue
        if 'velocity' not in kwargs.keys():
            velocity = 0
        if 'z' not in kwargs.keys():
            z = 0
        # set state properties
        self.__T = CP.PropSI('T',key1,value1,key2,value2,fluid)
        self.__p = CP.PropSI('P',key1,value1,key2,value2,fluid)
        self.__v = 1 / CP.PropSI('D',key1,value1,key2,value2,fluid)
        self.__d = CP.PropSI('D',key1,value1,key2,value2,fluid)
        self.__u = CP.PropSI('U',key1,value1,key2,value2,fluid)
        self.__h = CP.PropSI('H',key1,value1,key2,value2,fluid)
        self.__s = CP.PropSI('S',key1,value1,key2,value2,fluid)
        self.__x = CP.PropSI('Q',key1,value1,key2,value2,fluid)
        self.__vel = velocity
        self.__height = z     #height

    def temp(self):
        return self.__T

    def temperature(self):
        return self.__T

    def pressure(self):
        return self.__p

    def volume(self):
        return self.__v

    def density(self):
        return self.__d

    def energy(self):
        return self.__u

    def enthalpy(self):
        return self.__h

    def entropy(self):
        return self.__s

    def quality(self):
        return self.__x

    def velocity(self):
        return self.__vel

    def z(self):
        return self.__height

    def name(self):
        return self.__name

    def __str__():
        return self.__name

class Process(State):
    '''A class that defines values for a process based on a
    state in and a state out. It should inherit the methods for class state.'''

#     ''' A class that defines values for a process: w, q, delta u, etc.
#     It should inherit the methods for class state.
#     Units are by default on a per mass flow rate basis.
#     Assumes process is steady state with one inlet and one outlet
#         heat (kW/kg)
#         work (kW/kg)
#     '''
    def __init__(self,heat=0,work=0,state_in,state_out,*name=""):
        self.heat = heat
        self.work = work
        self.in = state_in  # these are of child class State
        self.out = state_out
        self.name = name


#   work = 0
#  heat = 0

        #     def __init__(self,state_in,state_out,**kwargs):

#         self.__heat =
