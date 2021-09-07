import unittest
from banking_pkg.account import Customer
import app


class TestCustomer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("setupClass")

    @classmethod
    def tearDownClass(cls):
        print("teardownClass")

    def setUp(self):
        self.c_01 = Customer("Jonathan","0917")
        self.c_02 = Customer("Jovan","0911")
        self.c_03 = Customer("Steven","0531")
        
    def tearDown(self):
        pass

    def test_is_amount_valid(self):
        self.assertTrue(Customer.is_amount_valid("100"))
        self.assertTrue(Customer.is_amount_valid("12.75"))
        self.assertTrue(Customer.is_amount_valid("250",500))
        self.assertTrue(Customer.is_amount_valid("67.50",500))
        self.assertFalse(Customer.is_amount_valid('fifty'))
        self.assertFalse(Customer.is_amount_valid("-20"))
        self.assertFalse(Customer.is_amount_valid("0"))
        self.assertFalse(Customer.is_amount_valid("1000",500))


class TestApp(unittest.TestCase):
    def test_create_username(self):
        pass