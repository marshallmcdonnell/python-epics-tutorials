"""Server for Example 1 of pcaspy."""

from pcaspy import Driver, SimpleServer
import random

prefix = "MTEST:"

pvdb = {
    "RAND": {
        "prec": 3,
        "scan": 1,
        "count": 10,
        "asyn": True,
    }
}


class MyDriver(Driver):
    """pcaspy driver for random numbers."""

    def __init__(self):
        """MyDriver class init."""
        super(MyDriver, self).__init__()

    def read(self, reason):
        """Overwrite read of parent Driver class."""
        if reason == "RAND":
            value = [random.random() for i in range(10)]
        else:
            value = self.getParam(reason)
        print(value)
        return value


if __name__ == "__main__":
    server = SimpleServer()
    server.createPV(prefix, pvdb)
    driver = MyDriver()

    while True:
        server.process(0.1)
