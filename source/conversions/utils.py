#!/usr/bin/env python

"""
utils.py: Some utilities for GRACE coordinate conversions
"""
__author__      = "Matthew Turnock"
__email__ = "matthew.turnock@protonmail.com"
__version__ = "1.0"

#######################################################################################################################

from os.path import join
import numpy as np
import pandas as pd

from astropy.coordinates import cartesian_to_spherical, spherical_to_cartesian
from astropy import units as u
from astropy import time


#######################################################################################################################
def cartesian_to_spherical_custom(x, y, z, withUnits=False, returnColat=False):
    """
    Function to convert from cartesian to spherical. Uses astropy converter but provides option to output with units or
    not. Can take inputs with or without units
    :param x: x-coordinate [m]
    :param y: y-coordinate [m]
    :param z: z-coordinate [m]
    :param withUnits: boolean to return with or without astropy units
    :return: the radius, latitude and longitude for spherical. Or colatitude if requested
    """
    r, lat, lon = cartesian_to_spherical(x, y, z)
    if not withUnits:
        r = r.value
        lat = lat.value
        lon=lon.value

    if returnColat:
        colat = np.pi/2 - lat
        return r, colat, lon
    else:
        return r, lat, lon

def spherical_to_cartesian_custom(r, latIn, lon, withUnits=False, inputColat=False):
    """
    Function to convert from spherical to cartesian. Uses astropy converter but provides option to output with units or
    not. Can take inputs with or without units
    :param r: radius from Earth
    :param latIn: latitude [rad]. Can use colatitude if inputColat is True
    :param lon: longitude [rad]
    :param withUnits: boolean to return with or without astropy units
    :param inputColat: boolean to determin if latIn is latitude or colatitude
    :return: cartesian coordinates x,y,z
    """
    if inputColat:
        lat = np.pi/2 - latIn
    else:
        lat = latIn

    x, y, z = spherical_to_cartesian(r, lat, lon)

    if not withUnits:
        x = x.value
        y = y.value
        z = z.value

    return x, y, z

def add_spherical_dataframe(GRACE_dataFrame, returnColat=False):
    """
    Function to append spherical coordinates to the GNV dataframe provided by GRACE data. Can append either latitudes or
    colatitudes along with radius and longitude
    :param GRACE_dataFrame: The GRACE dataframe for GNV constructed using the GRACE_data class
    :param returnColat: Boolean to determine if column should be latitude or colatitude
    :return:
    """
    if returnColat:
        latColHeader = "Colatitudes [rad]"
    else:
        latColHeader = "Latitudes [rad]"

    GRACE_dataFrameSpherical = pd.DataFrame.copy(GRACE_dataFrame)
    spherical = np.zeros((len(GRACE_dataFrameSpherical), 3))

    xs = np.array(GRACE_dataFrameSpherical.loc[:]["xpos [m]"])
    ys = np.array(GRACE_dataFrameSpherical.loc[:]["ypos [m]"])
    zs = np.array(GRACE_dataFrameSpherical.loc[:]["zpos [m]"])

    for i in range(len(spherical)):
        spherical[i] = cartesian_to_spherical_custom(xs[i], ys[i], zs[i], withUnits=False, returnColat=returnColat)

    radii = spherical[:,0]
    lats = spherical[:,1]
    lons = spherical[:,2]

    GRACE_dataFrameSpherical["Orbit radius [m]"] = radii
    GRACE_dataFrameSpherical[latColHeader] = lats
    GRACE_dataFrameSpherical["Longitudes [rad]"] = lons

    return GRACE_dataFrameSpherical


def add_mjd_dataframe(GRACE_dataFrame):
    GRACE_dataFrameMJD = pd.DataFrame.copy(GRACE_dataFrame)

    times = GRACE_dataFrameMJD.loc[:]["gps_time [s]"]
    times = time.Time(times, format='gps')
    timesMJD = times.mjd
    GRACE_dataFrameMJD["mjd_time [days]"] = timesMJD

    return GRACE_dataFrameMJD

def mjd_mjd2000_converter(time, inFormat='mjd'):
    """
    Function to convert between mjd and mjd200. inFormat is 'mjd' for mjd->mjd200, and 'mjd2000' for inverse
    :param time: Input time
    :param inFormat: Input time format ('mjd' or 'mjd2000')
    :return newtime: The new time after conversion
    """
    diff = 51544.5
    if inFormat == 'mjd':
        newtime = time - diff
    if inFormat == 'mjd2000':
        newtime = time + diff

    return newtime

#######################################################################################################################

class GRACE_data:
    """
    Class defining data for GRACE L1B data, from the data handbook. GIven a file the class will contain the pandas
    datframe, along with a numpy array and other characteristics of the data
    Currently implemented data types are:
    6.4: GPS1B
    6.5: GNV1B
    6.8: MAG1B
    6.10: SCA1B
    NOT 6.15: VGN1B, VGO1B, VGB1B, VCM1B, VKB1B, VSL1B
    """

    def __init__(self, dataDir="no_directory_given", dataFileName="no_filename_given"):
        """
        Initialisation of the class
        :param dataDir: Absolute or relative directory to the GRACE data
        :param dataFileName: Name of the file to be accessed
        """
        self.dataFileName = dataFileName
        self.dataDir = dataDir
        self.dataPath = join(dataDir, dataFileName)
        self.dataType = self.getDataType()
        self.colHeaders, self.colDTypes = self.getColumnHeaders()
        self.dataArray = self.getDataArray()
        self.dataFrame = self.getDataFrame()


    #******* Define column header names here *************

    # Misc common cols
    GRACE_id = "GRACE_id [-]"
    qualflg = "qualflg [-]"
    gps_time = "gps_time [s]"
    revtime_intg = "revtime_intg [s]"
    revtime_frac = "revtime_frac [micro s]"
    time_intg = "time_intg [s]"
    time_frac = "time_frac [-]"
    time_ref = "time_ref [-]"

    # GNV  cols
    coord_ref = "coord_ref [-]"
    xpos = "xpos [m]"
    ypos = "ypos [m]"
    zpos = "zpos [m]"
    xpos_err = "xpos_err [m]"
    ypos_err = "ypos_err [m]"
    zpos_err = "zpos_err [m]"
    xvel = "xvel [m]"
    yvel = "yvel [m]"
    zvel = "zvel [m]"
    xvel_err = "xvel_err [m]"
    yvel_err = "yvel_err [m]"
    zvel_err = "zvel_err [m]"

    # GPS cols
    prn_id = "prn_id [-]"
    ant_id = "ant_id [-]"
    prod_flag = "prod_flag [-]"
    CA_range = "CA_range [m]"
    L1_range = "L1_range [m]"
    L2_range = "L2_range [m]"
    CA_phase = "CA_phase [m]"
    L1_phase = "L1_phase [m]"
    L2_phase = "L2_phase [m]"
    CA_SNR = "CA_SNR [V/V]"
    L1_SNR = "L1_SNR [V/V]"
    L2_SNR = "L2_SNR [V/V]"
    CA_chan = "CA_chan  [V/V]"
    L1_chan = "L1_chan  [V/V]"
    L2_chan = "L2_chan  [V/V]"

    # Magnetometer (and magnetorquer) cols
    MfvX_RAW = "MfvX_RAW [micro T]"
    MfvY_RAW = "MfvY_RAW [micro T]"
    MfvZ_RAW = "MfvZ_RAW [micro T]"
    torque1A = "torque1A [mA]"
    torque2A = "torque2A [mA]"
    torque3A = "torque3A [mA]"
    torque1B = "torque1B [mA]"
    torque2B = "torque2B [mA]"
    torque3B = "torque3B [mA]"
    MF_BCalX = "MF_BCalX [-]"
    MF_BCalY = "MF_BCalY [-]"
    MF_BCalZ = "MF_BCalZ [-]"
    torque_cal = "torque_cal [-]"

    # Star Camera Data Cols
    sca_id = "sca_id [-]"
    quatangle = "quatangle [-]"
    quaticoeff = "quaticoeff [-]"
    quatjcoeff = "quatjcoeff [-]"
    quatkcoeff = "quatkcoeff [-]"

    # # Vector orientation data format record cols
    # mag = "mag [m]"
    # cosx = "cosx [-]"
    # cosy = "cosy [-]"
    # cosz = "cosz [-]"

    # Quarternion related cols
    qual_rss = "qual_rss [-]"


    cols_GPS = [revtime_intg, revtime_frac, GRACE_id, prn_id, ant_id, prod_flag, qualflg, CA_range, L1_range, L2_range,
                CA_phase, L1_phase, L2_phase, CA_SNR, L1_SNR, L2_SNR, CA_chan, L1_chan, L2_chan]
    colDTypes_GPS = [int, int, str, str, str, str, str, float, float, float, float, float, float, float, float, float,
                     float, float, float]

    cols_GNV = [gps_time, GRACE_id, coord_ref, xpos, ypos, zpos, xpos_err, ypos_err, zpos_err, xvel, yvel, zvel,
                xvel_err, yvel_err, zvel_err, qualflg]
    colDTypes_GNV = [int, str, str, float, float, float, float, float, float, float, float, float, float, float, float,
                     str]

    cols_MAG = [time_intg, time_frac, time_ref, GRACE_id, MfvX_RAW, MfvY_RAW, MfvZ_RAW, torque1A, torque2A,  torque3A,
                torque1B, torque2B, torque3B, MF_BCalX, MF_BCalY, MF_BCalZ, torque_cal, qualflg]
    colDTypes_MAG = [int, int, str, str, float, float, float, float, float, float, float, float, float, float, float,
                     float, float, str]

    cols_SCA = [gps_time, GRACE_id, sca_id, quatangle, quaticoeff, quatjcoeff, quatkcoeff, qual_rss, qualflg]
    colDTypes_SCA = [int, str, str, float, float, float, float, float, str]

    # cols_VG = [gps_time, GRACE_id, mag, cosx, cosy, cosz, qualflg]

    def getColumnHeaders(self):
        """
        Function to assign the column header names to a list, depending on type of data accessed
        :return self.colHeaders: List of used column headers
        """
        if self.dataType == "GPS1B":
            self.colHeaders = self.cols_GPS
            self.colDTypes = self.colDTypes_GPS
        elif self.dataType == "GNV1B":
            self.colHeaders = self.cols_GNV
            self.colDTypes = self.colDTypes_GNV
        elif self.dataType == "MAG1B":
            self.colHeaders = self.cols_MAG
            self.colDTypes = self.colDTypes_MAG
        elif self.dataType == "SCA1B":
            self.colHeaders = self.cols_SCA
            self.colDTypes = self.colDTypes_SCA
        else:
            self.colHeaders = None
            self.colDTypes = None
            print("Unknown data type used")

        return self.colHeaders, self.colDTypes

    def getDataArray(self):
        """
        Function to create the numpy data array. Accounts for skipping header lines
        :return self.dataArray:
        """
        with open(self.dataPath) as f:
            lines = f.read().splitlines()

        for lineIndex in range(len(lines)):
            line = lines[lineIndex]
            if "END OF HEADER" in line:
                skip_header = lineIndex + 1


        self.dataArray = np.genfromtxt(self.dataPath, skip_header=skip_header, dtype=str)
        return self.dataArray

    def getDataFrame(self):
        """
        Function to generate the pandas dataframe from the numpy array, and set dtypes according to those specified
        :return self.dataFrame: The pandas dataFrame
        """
        self.dataFrame = pd.DataFrame(data=self.dataArray, columns=self.colHeaders)
        for i in range(len(self.colHeaders)):
            self.dataFrame = self.dataFrame.astype({self.colHeaders[i]: self.colDTypes[i]})

        return self.dataFrame

    def getDataType(self):
        """
        Function to determine the data type from the filename
        :return self.dataType:  The dataType (eg MAG or ACC)
        """
        self.dataType = self.dataFileName.split("_")[0]
        return self.dataType


