"""Client for Example 1 of pcaspy."""

from epics import caget
import time

while True:
    time.sleep(1)
    print(caget("MTEST:RAND"))
