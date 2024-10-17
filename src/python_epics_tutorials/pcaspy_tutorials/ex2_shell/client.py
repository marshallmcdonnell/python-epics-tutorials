"""Client for Example 2 of pcaspy."""

from epics import caput, caget
import time

status_code = caput("MTEST:COMMAND", "ls")

# let PV get updated before we read it...
time.sleep(1.0)

output = caget("MTEST:OUTPUT")
print(f"code: {status_code} output: {output}")
