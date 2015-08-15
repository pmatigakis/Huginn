from twisted.web.xmlrpc import XMLRPC

class FlightSimulatorRPC(XMLRPC):
    def __init__(self, fdmexec):
        XMLRPC.__init__(self)

        self.fdmexec = fdmexec
        
    def xmlrpc_pause(self):
        self.fdmexec.hold()

        return True

    def xmlrpc_resume(self):
        self.fdmexec.resume()

        return True

    def xmlrpc_reset(self):
        return self.fdmexec.run_ic()