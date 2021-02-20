class User:
    def __init__(self, name, owes=None, owed_by=None):
        self.name = name if name else 'Unknown'
        self.owes = owes if owes else {}
        self.owed_by = owed_by if owed_by else {}
        self.balance = self.total_owed_by - self.total_owes

    @property
    def total_owed_by(self):
        if self.owed_by:
            return float(sum(self.owed_by.values()))
        return 0.0

    @property
    def total_owes(self):
        if self.owes:
            return float(sum(self.owes.values()))
        return 0.0

    def del_relationship(self, user_name):
        owes = self.owes.get(user_name, None)
        owed = self.owed_by.get(user_name, None)
        if owes:
            del self.owes[user_name]
        if owed:
            del self.owed_by[user_name]

    def lend(self, borrower, amount):
        owes_borrower = self.owes.get(borrower.name, 0)
        owed_by_borrower = self.owed_by.get(borrower.name, 0)
        final_sum = owed_by_borrower - owes_borrower + amount

        if final_sum == 0:
            self.del_relationship(borrower.name)
            borrower.del_relationship(self.name)
        elif final_sum > 0:
            self.del_relationship(borrower.name)
            borrower.del_relationship(self.name)
            self.owed_by[borrower.name] = final_sum
            borrower.owes[self.name] = final_sum
        else:
            self.del_relationship(borrower.name)
            borrower.del_relationship(self.name)
            self.owes[borrower.name] = abs(final_sum)
            borrower.owed_by[self.name] = abs(final_sum)

        self.recalculate_balance()
        borrower.recalculate_balance()

    def recalculate_balance(self):
        self.balance = self.total_owed_by - self.total_owes

    def __repr__(self):
        return str({
            'name': self.name,
            'owes': self.owes,
            'owed_by': self.owed_by,
            'balance': self.balance
        })

    def __gt__(self, other):
        return self.name > other.name
