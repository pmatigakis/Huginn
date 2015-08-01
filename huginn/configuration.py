class InterfacesCatalog(object):
    def __init__(self):
        self.interfaces = {}
        
    def is_address_available(self, address, port):
        used_addresses = [(self.get_interface_host(interface), 
                           self.get_interface_port(interface))
                          for interface in self.interfaces]
    
        return (address, port) not in used_addresses
    
    def get_interface_host(self, interface):
        return self.interfaces[interface]["host"]
    
    def get_interface_port(self, interface):
        return self.interfaces[interface]["port"]
    
    def add(self, interface, address, port):
        self.interfaces[interface] = {"host": address, "port": port}
    
    def get(self, interface):
        return self.interfaces[interface]
    
    def delete(self, interface):
        del self.interfaces[interface]
        
    def contains(self, interface):
        return interface in self.interfaces