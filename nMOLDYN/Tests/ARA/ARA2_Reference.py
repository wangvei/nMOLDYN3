import os
import tempfile
from nMOLDYN.GlobalVariables import GVAR

units_length = 1.0
title = 'Autoregressive Model'
trajectory = [os.path.join(GVAR['nmoldyn_trajs'],'TrajectoryTest1.nc')]
ar_precision = None
time_steps = None
frequency_points = None
log_file = 'logfile.log'
units_frequency = 1.0
projection_vector = None
output_files = {'ara': os.path.join(tempfile.gettempdir(),'test.plot')}
deuter = None
ar_order = 10
atoms = {'Protein.0': ['BackBone']}
weights = 'none'
time_info = (0, 49, 4)
