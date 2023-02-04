import sys
import os
os.chdir("documentation")
print(os.system("sphinx-apidoc -f -o ../documentation/source ../src/logic"))
print(os.system("make html"))