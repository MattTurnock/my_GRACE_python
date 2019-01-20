###############################################################################
Some notes for making sure the environment is set up properly
The following notes represent the easiest way to do it on a unix system
###############################################################################

1) Ensure anaconda is installed, conda will be used because cartopy can be a pain to install otherwise

2) Create a conda virtual environment called "my_GRACE_python"
    --> I did this with pycharm, but it can also be done from terminal

3) Install the required packages:
    a) Make sure correct conda env is being used by running "source activate my_GRACE_python"
    b) Install package dependencies with "conda install python numpy scipy pandas cython cartopy matplotlib=2"
    c) Install pip with "conda install pip"
    d) Install cdflib with "pip install cdflib"

4) Install the chaos package with "pip install chaosmagpy-x.x.tar.gz" (replace 'x' with version) in directory of the tar file.

5) Done! Run example programs to check functionality

6) chaos package can be upgraded by simply reinstalling the new one as described above


NOTE: Use anaconda-navigator command to bring up some useful stuff
      Also use source activate my_GRACE_python to activate


