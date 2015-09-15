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
        #TODO: The reset procedure needs to be refactored
                
        if not self.fdmexec.run_ic():
            return False
        
        if not self.fdmexec.run():
            return False
        
        running = True
        while running and self.fdmexec.get_sim_time() < 0.1:
            self.fdmexec.process_message()
            self.fdmexec.check_incremental_hold()

            running = self.fdmexec.run()
            
        if running:
            return self.fdmexec.trim()
        else:
            return False