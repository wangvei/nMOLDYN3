#!/home/cs/pellegrini/python/bin/python
################################################################
# This is an automatically generated python-nMOLDYN run script #
################################################################

import os
import unittest

from Scientific import N
from Scientific.IO.NetCDF import NetCDFFile

from MMTK import *
from nMOLDYN.GlobalVariables import GVAR
from nMOLDYN.Analysis.Templates import *

serial =  os.path.join("serial.nc")
parallel =  os.path.join("parallel.nc")

parameters = {}

parameters['version'] = "3.0.5"
parameters['estimate'] = "no"

parameters['trajectory'] = os.path.join(GVAR['nmoldyn_trajs'],"BPTI.nc")

parameters['differentiation'] = 1
parameters['resolution'] = 10.0
parameters['group'] = "all"
parameters['projection'] = "no"
parameters['referenceframe'] = 1
parameters['stepwiserbt'] = "no"
parameters['timeinfo'] = "1:400:10"

parameters['pyroserver'] = "monoprocessor"
parameters['output'] = serial
analysis = AngularDensityOfStates_serial(parameters)
analysis.runAnalysis()

parameters['pyroserver'] = "multiprocessor:2"
parameters['output'] = parallel
analysis = AngularDensityOfStates_parallel(parameters)
analysis.runAnalysis()

class Test_Serial_vs_Parallel(unittest.TestCase):
    
    def check_var(self, varName, sValues, pValues):
                                
        errorMax = max(abs(N.ravel(sValues - pValues)))
        self.assertAlmostEqual(errorMax, 0.0, 6)
                
# Open the NetCDF output file for the serial run.
serialOutput = NetCDFFile(serial, 'r')

# Open the NetCDF output file for the parallel run.
parallelOutput = NetCDFFile(parallel, 'r')

# Loop over the NetCDF variables.
for varName in serialOutput.variables.keys():
            
    # Tests only numeric variables.
    if serialOutput.variables[varName].typecode() != 'c':

        # The corresponding values for the serial run.
        serialValues = serialOutput.variables[varName].getValue()
                
        # The corresponding values for the parallel run.
        parallelValues = parallelOutput.variables[varName].getValue()
        
        def testvar(varName, serialValues, parallelValues):
            return lambda self : self.check_var(varName, serialValues, parallelValues)
        
        setattr(Test_Serial_vs_Parallel, "test_%s" % varName, testvar(varName, serialValues, parallelValues))
        
serialOutput.close()

parallelOutput.close()
                        
def suite():
    loader = unittest.TestLoader()
    s = unittest.TestSuite()
    s.addTest(loader.loadTestsFromTestCase(Test_Serial_vs_Parallel))
            
    return s
            
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
    
