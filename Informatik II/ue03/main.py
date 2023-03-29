class BankAccount:
    # Internal state of the account - cannot be modified from outside
    __holder: str
    __balance: float

    # Constructor
    def __init__(self, holder: str):
        """Eröffnet ein neues Bankkonto."""

        self.__holder = holder
        self.__balance = 0.0
        print(f"Bankkonto für {holder} angelegt")

    # Destructor
    def __del__(self):
        """Schließt das Bankkonto."""

        print(
            f"Bankkonto für {self.__holder} geschlossen "
            + f"(Letzter Kontostand: {self.__balance})"
        )

    # String representation
    def __str__(self):
        return (
            f"Kontoinformation - Inhaber: {self.__holder}, "
            + f"Kontostand: {self.__balance}"
        )

    # Public read-only access to the internal state
    def get_holder(self):
        return self.__holder

    def get_balance(self):
        return self.__balance

    def deposit(self, amount: float) -> bool:
        """Einzahlung auf das Konto."""

        if amount <= 0:
            # Only positive amounts are allowed
            print(f"Ungültige Einzahlung von {self.__holder}: {amount}")
            return False

        print(f"{self.__holder} hat {amount} eingezahlt")
        self.__balance += amount
        return True

    def withdraw(self, amount: float) -> bool:
        """Abhebung vom Konto."""

        if amount < 0:
            # Only positive amounts are allowed
            print(f"Ungültige Abhebung von {self.__holder}: {amount}")
            return False

        if amount > self.__balance:
            # Cannot withdraw more than the current balance
            print(f"Ungültige Abhebung von {self.__holder}: {amount}")
            return False

        print(f"{self.__holder} hat {amount} abgehoben")
        self.__balance -= amount
        return True

    def transfer(self, target: "BankAccount", amount: float) -> bool:
        """Überweisung auf ein anderes Konto (kostet 50c)."""

        transfer_fee = 0.5
        withdraw_amount = amount + transfer_fee
        deposit_amount = amount

        withdraw_success = self.withdraw(withdraw_amount)
        if not withdraw_success:
            # Note that we already got an error message from the `withdraw` method,
            # which doesn't show up in the example output. A correct implementation
            # would not print messages, but raise an Error object that could be caught here.
            print(
                f"Überweisung über {amount} von {self.__holder} "
                + f"nach {target.__holder} fehlgeschlagen"
            )
            return False

        deposit_success = target.deposit(deposit_amount)
        if not deposit_success:
            print(
                f"Überweisung über {amount} von {self.__holder} "
                + f"nach {target.__holder} fehlgeschlagen"
            )
            # Rollback the withdrawal
            self.deposit(withdraw_amount)
            return False

        print(
            f"Überweisung über {amount} von {self.__holder} "
            + f"nach {target.__holder} erfolgreich"
        )
        return True


# Test code
if __name__ == "__main__":
    account1 = BankAccount("Bender")
    print(account1)
    account1.withdraw(100)
    account1.deposit(1000)
    account1.withdraw(100)
    print(account1)
    account2 = BankAccount("Marvin")
    account1.transfer(account2, 1000)
    account1.transfer(account2, 500)
    account2.deposit(-500)
    print(account1)
    del account1
    print(account2)
