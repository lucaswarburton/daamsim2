import scipy.io

def testframework(matlabfilename, jsonfilename):
    matlab_data = loadmatlabfile(matlabfilename)
    print(matlab_data)

def loadmatlabfile(filename) -> dict: 
    dictionary = dict()
    scipy.io.loadmat(file_name=filename, mdict=dictionary)
    return dictionary

def loadjsonfile(filename):
   return 
    
    
if __name__ == "__main__":
    testframework("test.mat", "")