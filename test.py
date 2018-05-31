import os
#files = [x[0] for x in os.walk('.')]
files = [f for f in os.listdir('.')]
for f in files:
    print f