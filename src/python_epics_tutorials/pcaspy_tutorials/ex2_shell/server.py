"""Server for Example 2 of pcaspy."""

import shlex
import subprocess
import sys
from pcaspy import Driver, SimpleServer
import threading
import time

prefix = "MTEST:"

pvdb = {
    "COMMAND": {
        "type": "string",
    },
    "OUTPUT": {
        "type": "string",
    },
    "STATUS": {
        "type": "enum",
        "enums": ["DONE", "BUSY"],
    },
    "ERROR": {
        "type": "string",
    },
}


class MyDriver(Driver):
    """pcaspy driver for running shell commands."""

    def __init__(self):
        """MyDriver class init."""
        super(MyDriver, self).__init__()
        self.tid = None

    def write(self, reason, value):
        """Overwrite write of parent Driver class."""
        status = True
        if reason == "COMMAND":
            print(f"Running command: {value}")

            if not self.tid:
                command = value
                self.tid = threading.Thread(target=self.run_shell, args=(command,))
                self.tid.start()
            else:
                status = False
        else:
            status = False

        if status:
            self.setParam(reason, value)

        return status

    def run_shell(self, command):
        """Run shell command on subprocess."""
        print("DEBUG: Run ", command)

        # set status to BUSY
        self.setParam("STATUS", 1)  # 0 = DONE, 1 = BUSY
        self.updatePVs()

        # run shell command
        try:
            time.sleep(0.1)
            proc = subprocess.Popen(
                shlex.split(command),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            proc.wait()
        except OSError:
            self.setParam("ERROR", str(sys.exc_info()[1]))
            self.setParam("OUTPUT", "")
        else:
            self.setParam("ERROR", str(proc.stderr.read().rstrip()))
            self.setParam("OUTPUT", str(proc.stdout.read().rstrip()))
        self.callbackPV("COMMAND")

        # set status DONE
        self.setParam("STATUS", 0)
        self.updatePVs()
        self.tid = None

        print("DEBUG: Finish ", command)


if __name__ == "__main__":
    server = SimpleServer()
    server.createPV(prefix, pvdb)
    driver = MyDriver()

    while True:
        server.process(0.1)
