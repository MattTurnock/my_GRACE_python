from conversions.utils import GRACE_data, spherical_to_cartesian_custom, cartesian_to_spherical_custom
from pathlib import Path
import os, sys
from os.path import join
import pandas as pd


from astropy import units as u

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


x = np.array(GNV_dataFrame.loc[:]["xpos [m]"])


# GNV_ex_time = GNV_dataFrame.loc[0]
# x,y,z = np.array(GNV_ex_time.loc[:]["xpos [m]":"zpos [m]"])*u.m
print(x)
#
# r, colat, lon = cartesian_to_spherical_custom(x, y, z, withUnits=False, returnColat=True)
# print(r, colat, lon)











