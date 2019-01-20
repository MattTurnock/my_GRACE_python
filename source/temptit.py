"""""
#################################################################################################################
INSERT TITLE AND BRIEF DESCRIPTION
Currently just doing for one folder eh

Author: Matthew Turnock
Email:  matthew.turnock@protonmail.com
#################################################################################################################
"""

import numpy as np
import os
import pandas as pd

#################################################################################################################
# CAN CHANGE THESE

# Directory of file to grab
ORBDATA_loc = "./GRACE_L1B_data/grace_1B_2014-01-15_02"

#################################################################################################################

# Specify File
ORBDATA_file = os.path.join(ORBDATA_loc, "GNV1B_2014-01-15_B_02.txt")

# Load data into panda dataframe, and specify column names
colnames = ["gps_time",
            "GRACE_id",
            "coord_ref",
            "xpos",
            "ypos",
            "zpos",
            "xpos_err",
            "ypos_err",
            "zpos_err",
            "xvel",
            "yvel",
            "zvel",
            "xvel_err",
            "yvel_err",
            "zvel_err",
            "qualfig"]

ORB_data = pd.read_csv(ORBDATA_file, skiprows=26, delim_whitespace=True, names=colnames)

