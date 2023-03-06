import unittest
import portfolio
import math
import random

def random_quantity():
    return random.random()

def random_unit_cost():
    return random.paretovariate(math.log(5, 4))


class TestPortfolio(unittest.TestCase):

    def test_total_quantity_at_start(self):
        reality = portfolio.Value()
        self.assertEqual(reality.total_quantity, 0)
        self.assertEqual(reality.total_cost, 0)

    def test_get_unit_cost(self):
        reality = portfolio.Value(budget=1)
        self.assertEqual(reality.get_current_unit_cost(), 0)

    def test_buy(
        self,
        buy_quantity=random_quantity(),
        buy_unit_cost=random_unit_cost()
    ):
        transaction_cost = buy_quantity * buy_unit_cost
        reality = portfolio.Value(transaction_cost + 1)
        original_cost = reality.total_cost
        original_quantity = reality.total_quantity

        reality.buy(
            quantity=buy_quantity, unit_cost=buy_unit_cost
        )

        self.assertEqual(
            reality.total_cost,
            original_cost - (buy_quantity * buy_unit_cost)
        )
        self.assertEqual(
            reality.total_quantity,
            original_quantity + buy_quantity
        )
        self.assertEqual(
            reality.get_current_unit_cost(),
            reality.total_quantity / reality.total_cost
        )

    def test_invalid_buy_raises_value_error(
        self,
        buy_quantity=-random_quantity(),
        buy_unit_cost=random_unit_cost()
    ):
        reality = portfolio.Value()
        original_cost = reality.total_cost
        original_quantity = reality.total_quantity
        original_unit_cost = reality.get_current_unit_cost()

        self.assertEqual(original_unit_cost, 0)

        with self.assertRaises(ValueError):
            reality.buy(
                quantity=buy_quantity, unit_cost=buy_unit_cost
            )

        self.assertEqual(
            reality.total_cost, original_cost
        )
        self.assertEqual(
            reality.total_quantity, original_quantity
        )
        self.assertEqual(
            reality.get_current_unit_cost(), original_unit_cost
        )

    def test_invalid_sales_raise_value_error(
        self,
        sell_quantity=random_quantity(),
        sell_unit_cost=random_unit_cost()
    ):
        reality = portfolio.Value()
        original_cost = reality.total_cost
        original_quantity = reality.total_quantity
        original_unit_cost = reality.get_current_unit_cost()

        self.assertEqual(original_unit_cost, 0)

        with self.assertRaises(ValueError):
            reality.sell(
                quantity=sell_quantity, unit_cost=sell_unit_cost
            )

        self.assertEqual(reality.total_cost, original_cost)
        self.assertEqual(
            reality.total_quantity, original_quantity
        )
        self.assertEqual(
            reality.get_current_unit_cost(), original_unit_cost
        )

    def test_buying_then_selling(
        self,
        buy_quantity=random_quantity(),
        buy_unit_cost=random_unit_cost(),
        sell_quantity=random_quantity() - 0.01,
        sell_unit_cost=random_unit_cost(),
    ):
        buy_total_cost = buy_quantity * buy_unit_cost
        sell_total_cost = sell_quantity * sell_unit_cost

        reality = portfolio.Value(buy_total_cost + 1)
        original_total_cost = reality.total_cost
        original_quantity = reality.total_quantity

        reality.buy(
            quantity=buy_quantity, unit_cost=buy_unit_cost
        )
        self.assertEqual(
            reality.total_quantity,
            original_quantity + buy_quantity
        )
        self.assertEqual(
            reality.total_cost,
            original_total_cost - buy_total_cost
        )
        self.assertEqual(
            reality.get_current_unit_cost(),
            reality.total_quantity / reality.total_cost
        )

        if sell_quantity <= reality.total_quantity:
            reality.sell(
                quantity=sell_quantity, unit_cost=sell_unit_cost
            )
            self.assertEqual(
                reality.total_quantity,
                original_quantity + buy_quantity - sell_quantity
            )
            self.assertEqual(
                reality.total_cost,
                original_total_cost - buy_total_cost + sell_total_cost
            )

    def test_get_current_balance(self):
        buy_quantity = random_quantity()
        buy_unit_cost = random_unit_cost()
        sell_quantity = buy_quantity - 0.01
        sell_unit_cost = random_unit_cost()
        budget = (buy_quantity * buy_unit_cost) + 1

        reality = portfolio.Value(budget)
        original_quantity = reality.total_quantity
        original_total_cost = reality.total_cost

        buy = reality.buy(
            quantity=buy_quantity,
            unit_cost=buy_unit_cost
        )
        self.assertEqual(
            buy.cost(),
            buy_quantity * buy_unit_cost
        )
        self.assertTrue(buy.is_affordable(budget))
        self.assertEqual(reality.total_cost, -buy.cost())
        self.assertEqual(reality.get_current_balance(), budget + (-buy.cost()))

        sell = reality.sell(
            quantity=sell_quantity,
            unit_cost=sell_unit_cost
        )
        self.assertEqual(
            sell.cost(),
            sell_quantity * sell_unit_cost
        )
        self.assertEqual(
            reality.total_quantity,
            original_quantity + buy_quantity - sell_quantity
        )
        self.assertEqual(
            reality.total_cost,
            original_total_cost - buy.cost() + sell.cost()
        )
        self.assertEqual(
            reality.get_current_balance(),
            budget + reality.total_cost
        )

    # @unittest.skip
    def test_random_price(self):
        self.maxDiff = None
        self.assertEqual(
            [random_unit_cost() for i in range(100)],
            # [
            #     2.808880848305486,
            #     1.4517444293093482,
            #     1.030487242276511,
            #     3.5316634927065538,
            #     1.1198973369599636,
            #     1.0462846075530385,
            #     1.0180923195328762,
            #     12.757105808535648,
            #     1.5977842528553734,
            #     3.6972435863332933
            # ]
            []
        )