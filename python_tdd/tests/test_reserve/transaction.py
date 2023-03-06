class Transaction(object):

    def __init__(
        self,
        quantity:float=None,
        unit_cost:float=None,
    ):
        self.quantity = quantity
        self.unit_cost = unit_cost

    def cost(self):
        return self.quantity * self.unit_cost

    @staticmethod
    def is_greater_than_zero(value):
        return value > 0

    def is_valid(self):
        return self.is_greater_than_zero(self.quantity) and self.is_greater_than_zero(self.unit_cost)

    def is_affordable(self, budget:float=None):
        return self.is_valid() and budget >= self.cost()

    def is_valid_sale(self, total_quantity):
        return self.is_valid() and self.quantity <= total_quantity