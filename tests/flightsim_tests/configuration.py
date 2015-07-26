from unittest import TestCase

from flightsim.configuration import InterfacesCatalog

class InterfacesCatalogTests(TestCase):
    def test_return_true_when_address_is_available(self):
        interfaces_catalog = InterfacesCatalog()
        
        self.assertTrue(interfaces_catalog.is_address_available("127.0.0.1", 1000))
        
    def test_return_false_when_address_is_not_available(self):
        interfaces_catalog = InterfacesCatalog()
        
        interfaces_catalog.add("http", "127.0.0.1", 8080)
        
        self.assertFalse(interfaces_catalog.is_address_available("127.0.0.1", 8080))
        