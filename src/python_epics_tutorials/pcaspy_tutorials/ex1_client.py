from epics import caget
import time

while True:
    time.sleep(0.5)
    print(caget("MTEST:RAND"))



