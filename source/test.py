import numpy as np
import cdflib
import matplotlib.pyplot as plt
from chaosmagpy import load_CHAOS_matfile
from chaosmagpy.coordinate_utils import mjd2000, transform_points
from chaosmagpy.model_utils import synth_values
from chaosmagpy.data_utils import rsme
from utils import GRACE_data