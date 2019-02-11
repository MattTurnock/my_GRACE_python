from conversions.utils import GRACE_data, spherical_to_cartesian_custom, cartesian_to_spherical_custom, add_spherical_dataframe, add_mjd_dataframe
from pathlib import Path
import os, sys
from os.path import join
import pandas as pd


from astropy import units as u
from astropy import time

import numpy as np
import cdflib
import matplotlib.pyplot as plt
from chaosmagpy import load_CHAOS_matfile
from chaosmagpy.coordinate_utils import mjd2000, transform_points
from chaosmagpy.model_utils import synth_values
from chaosmagpy.data_utils import rsme


projectdir = Path().resolve().parent.parent
dataDir = join(projectdir, "source", "GRACE_L1B_data", "grace_1B_2014-01-15_02")

# header1 = GRACE_data(dataDir=dataDir, dataFileName="SCA1B_2014-01-15_B_02.txt")
# # print(header1.dataFileName)
# # print(header1.getColumnHeaders(returnDataType=True))
# print(header1.colHeaders)
baseDataFilename = "%s1B_2014-01-15_B_02.txt"

exampleDataClasses = {"GPS":None, "GNV":None, "MAG":None, "SCA":None}
exampleDataClasses = {"GNV":None}

for dataType in exampleDataClasses:
    dataFileName = baseDataFilename %dataType
    exampleDataClasses[dataType] = (GRACE_data(dataDir=dataDir, dataFileName=dataFileName))



GNV_dataClass = exampleDataClasses["GNV"]
GNV_dataFrame = GNV_dataClass.dataFrame
GNV_dataFrame = add_spherical_dataframe(GNV_dataFrame, returnColat=True)
# print(GNV_dataFrame.loc[0])

# NEED TO CONVERT TIMES TO MJD



GNV_dataFrame = add_mjd_dataframe(GNV_dataFrame)
print(GNV_dataFrame)
print(GNV_dataFrame.loc[0])
print(GNV_dataFrame.loc[0]["mjd_time [days]"])
print(type(GNV_dataFrame.loc[0]["mjd_time [days]"]))

#####################################################################################################################
# Testing of application to CHAOS

FILEPATH_CHAOS = join(projectdir, "source", "chaosmagpy_package", "data", "CHAOS-6-x7.mat")

R_REF = 6371.2


# give inputs
theta = np.array([55.676, 51.507, 64.133])  # colat in deg
phi = np.array([12.568, 0.1275, -21.933])  # longitude in deg
radius = np.array([0.0, 0.0, 500.0]) + R_REF  # radius from altitude in km
time = np.array([3652.0, 5113.0, 5287.5])  # time in mjd2000

# load the CHAOS model
model = load_CHAOS_matfile(FILEPATH_CHAOS)
print(model)

print('Computing core field.')
coeffs = model.synth_tdep_field(time)
B_core = synth_values(coeffs, radius, theta, phi)

print('Computing crustal field up to degree 110.')
coeffs = model.synth_static_field(nmax=110)
B_crust = synth_values(coeffs, radius, theta, phi)

# complete internal contribution
B_radius_int = B_core[0] + B_crust[0]
B_theta_int = B_core[1] + B_crust[1]
B_phi_int = B_core[2] + B_crust[2]

print('Computing field due to external sources, incl. induced field: GSM.')
coeffs_ext = model.synth_gsm_field(time, source='external')  # inducing
coeffs_int = model.synth_gsm_field(time, source='internal')  # induced

B_ext_gsm = synth_values(coeffs_ext, radius, theta, phi, source='external')
B_int_gsm = synth_values(coeffs_int, radius, theta, phi, source='internal')

print('Computing field due to external sources, incl. induced field: SM.')
coeffs_ext = model.synth_sm_field(time, source='external')  # inducing
coeffs_int = model.synth_sm_field(time, source='internal')  # induced

B_ext_sm = synth_values(coeffs_ext, radius, theta, phi, source='external')
B_int_sm = synth_values(coeffs_int, radius, theta, phi, source='internal')

# complete external field contribution
B_radius_ext = B_ext_gsm[0] + B_int_gsm[0] + B_ext_sm[0] + B_int_sm[0]
B_theta_ext = B_ext_gsm[1] + B_int_gsm[1] + B_ext_sm[1] + B_int_sm[1]
B_phi_ext = B_ext_gsm[2] + B_int_gsm[2] + B_ext_sm[2] + B_int_sm[2]

# complete forward computation
B_radius = B_radius_int + B_radius_ext
B_theta = B_theta_int + B_theta_ext
B_phi = B_phi_int + B_phi_ext

# save to output file
data_CHAOS = np.stack([time, radius, theta, phi,
                       B_radius, B_theta, B_phi], axis=-1)

print(data_CHAOS)

# header = ('  t (mjd2000)    r (km) theta (deg)   phi (deg)       B_r   '
#           'B_theta     B_phi       B_r   B_theta     B_phi       B_r   '
#           'B_theta     B_phi\n'
#           '                                                           '
#           'model total                  model internal                '
#           'model external')
# np.savetxt('example1_output.txt', data_CHAOS, delimiter=' ', header=header,
#            fmt=['%15.8f', '%9.3f', '%11.5f', '%11.5f'] + 9*['%9.2f'])

# print('Saved output to example1_output.txt.')









