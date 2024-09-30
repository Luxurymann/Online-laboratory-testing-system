import subprocess
from subprocess import Popen
result=subprocess.run(["python","../Testing/input/code.py"],capture_output=True,text=True,input="1\n2\n3")
print(result.stdout)