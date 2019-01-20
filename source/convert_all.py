"""""
#################################################################################################################
Script for quickly converting all the custom .dat files in directories of this file into ASCII.txt files using
the binary reader

Author: Matthew Turnock, matthew.turnock@protonmail.com
#################################################################################################################
"""

import os
from glob import glob

#################################################################################################################
# CAN CHANGE THESE 

# IF THE BINARY READER IS NOT IN DIRECTORY 1 ABOVE THE DIRECTORY CONTAINING FOLDERS
RELEASE_dir_loc = "./binary_reader/GraceReadSW_L1_2010-03-31"

# If the raw data folder is not where the python file is
RAWDATA_loc = "./GRACE_L1B_data"

#################################################################################################################
# SHOULDNT NEED TO CHANGE THE FOLLOWING

# Location of the script
bin2ascii_script = os.path.join(RELEASE_dir_loc, "RELEASE_2010-03-31/Bin2AsciiLevel1.e")

# Arguments for bin2ascii, template. First specify the program, then the binfile (.bin), next specify the savefile (.txt)
bin2ascii_args = "%s -binfile %s | tee %s"

# List of all directories to go through
RAWDATA_dirs = os.listdir(os.path.join(RAWDATA_loc)) 
for directory in RAWDATA_dirs:
	if os.path.isfile(directory): RAWDATA_dirs.remove(directory)

# For loop to do conversions for each directory in raw_GRACE_data
for directory in RAWDATA_dirs:
	# Make a list of all .dat files in the directory
	RAWFILES_list = glob(os.path.join(
		RAWDATA_loc, 
		directory, 
		"*.dat"))

	# For loop to do conversion for each .dat file in the directory and save to same directory
	for datpath in RAWFILES_list:
		# Make the save path identiacal to the datpath but with .txt extension instead of .dat
		savepath = datpath[0:-4] + ".txt"
		
		# Create arguments string to execute in terminal
		current_args = bin2ascii_args %(bin2ascii_script, datpath, savepath)
		
		# Run the conversion command in terminal
		os.system(current_args)

		# Print something to let us know whats going on
		"Converting: \n%s to \n%s\n" %(datpath, savepath)









