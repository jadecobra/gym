import transaction


class Value(object):

    zero = 0.0

    def __init__(self, budget:float=None):
        self.budget = budget if budget else self.zero
        self.total_cost = self.zero
        self.total_quantity = self.zero

    def get_current_unit_cost(self):
        try:
            return self.total_quantity / self.total_cost
        except ZeroDivisionError:
            return self.zero

    def display_report(self, transaction_cost):
        print(
            f'\ttotal_quantity: {self.total_quantity}',
            f'\tcurrent_unit_cost: {self.get_current_unit_cost()}',
            f'\ttransaction_cost: {transaction_cost}\n'
            f'\tbudget: {self.budget}',
            f'\ttotal_spent: {self.total_cost}',
            f'\tbalance: {self.get_current_balance()}',
        )
        print('-'*80)

    def update_total_quantity(self, quantity):
        self.total_quantity += quantity

    def update_total_cost(self, transaction_cost:float=0.0):
        self.total_cost += transaction_cost

    def update_values(self, quantity:float=None, cost:float=None):
        self.update_total_quantity(quantity)
        self.update_total_cost(cost)
        self.display_report(cost)

    def buy(self, quantity:float=None, unit_cost:float=None):
        event = transaction.Transaction(
            quantity=quantity,
            unit_cost=unit_cost
        )
        if event.is_affordable(self.budget):
            print(f'\tbuy(quantity:{quantity}, unit_cost:{unit_cost})')
            self.update_values(
                quantity=quantity,
                cost=-event.cost()
            )
        else:
            raise ValueError(f'transaction_cost: {event.cost()} > budget:{self.budget}')
        return event

    def sell(self, quantity:float=None, unit_cost:float=None):
        event = transaction.Transaction(
            quantity=quantity,
            unit_cost=unit_cost
        )
        if event.is_valid_sale(self.total_quantity):
            print(f'\tsell(quantity:{quantity}, unit_cost:{unit_cost})')
            self.update_values(
                quantity=-quantity,
                cost=event.cost()
            )
        else:
            raise ValueError(f'sell_quantity: {quantity} > total_quantity: {self.total_quantity}')
        return event

    def get_current_balance(self):
        return self.budget + self.total_cost

def divider():
    return 12

def portions():
    return (
        number * quantity()  / divider()
        for number in range(1, divider() + 1)
    )

def value():
    return 1

def value_after_correction(original_cost=None, correction_cost=None, correction_quantity=None, original_quantity=None):
    return 2

def under_value():
    return 0.5

def at_value():
    return 1

def over_value():
    return 2