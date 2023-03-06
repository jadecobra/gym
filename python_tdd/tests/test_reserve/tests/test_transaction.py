import unittest
import transaction
import math
import random

def random_quantity():
    return random.random()

def random_unit_cost():
    return random.paretovariate(math.log(5, 4))


class TestTransaction(unittest.TestCase):

    def test_transaction_is_not_valid_when_unit_cost_less_than_or_equal_to_zero(self):
        self.assertFalse(
            transaction.Transaction(
                quantity=random_quantity(),
                unit_cost=-1
            ).is_valid()
        )
        self.assertFalse(
            transaction.Transaction(
                quantity=random_quantity(),
                unit_cost=0
            ).is_valid()
        )

    def test_transaction_is_not_valid_when_quantity_less_than_or_equal_to_zero(self):
        self.assertFalse(
            transaction.Transaction(
                quantity=-1, unit_cost=1
            ).is_valid()
        )
        self.assertFalse(
            transaction.Transaction(
                quantity=0, unit_cost=1
            ).is_valid()
        )

    def test_transaction_is_not_affordable_when_cost_greater_than_budget(self):
        quantity = random_quantity()
        unit_cost = random_unit_cost()

        self.assertFalse(
            transaction.Transaction(
                quantity=quantity,
                unit_cost=unit_cost
            ).is_affordable(
                quantity * unit_cost - 1,
            )
        )

    def test_transaction_is_affordable_when__cost_less_than_or_equal_budget(self):
        quantity = random_quantity()
        unit_cost = random_unit_cost()

        self.assertTrue(
            transaction.Transaction(
                quantity=quantity,
                unit_cost=unit_cost
            ).is_affordable(
                quantity * unit_cost + 1
            )
        )

    def test_transaction_is_not_valid_sale_when_total_quantity_is_less_than_sale_quantity(self):
        quantity = random_quantity()
        unit_cost = random_unit_cost()

        self.assertTrue(
            transaction.Transaction(
                quantity=quantity,
                unit_cost=unit_cost
            ).is_valid_sale(
                quantity + 1
            )
        )