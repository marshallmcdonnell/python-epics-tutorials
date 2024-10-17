from pcaspy import Driver, SimpleServer
import random

prefix = "MTEST:"

pvdb = {
    "RAND": {
        "prec": 3,
        "scan": 1,
    }
}

class myDriver(Driver):
    def __init__(self):
        super(myDriver, self).__init__()

    def read(self, reason):
        print(reason)
        if reason == "RAND":
            value = random.random()
        else:
            value = self.getParam(reason)
        print(value)
        return value


if __name__ == "__main__":
    server = SimpleServer()
    server.createPV(prefix, pvdb)
    driver = myDriver()

    while True:
        server.process(0.1)
