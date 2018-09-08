import datetime


class Accounting(object):
    """
    Accounting class.

    This class contains two main attributes:
    trades -> memcache "like" for the trades
    exchange_table_data -> stock values
    """

    __slots__ = ["trades", "exchange_table_data"]

    def __init__(self):
        self.trades = {}
        self.exchange_table_data = {
            "TEA": {
                "type": "Common",
                "last_dividend": 0,
                "fixed_dividend": None,
                "value": 100,
            },
            "POP": {
                "type": "Common",
                "last_dividend": 8,
                "fixed_dividend": None,
                "value": 100,
            },
            "ALE": {
                "type": "Common",
                "last_dividend": 23,
                "fixed_dividend": None,
                "value": 60,
            },
            "GIN": {
                "type": "Preferred",
                "last_dividend": 8,
                "fixed_dividend": 0.02,
                "value": 100,
            },
            "JOE": {
                "type": "Common",
                "last_dividend": 13,
                "fixed_dividend": None,
                "value": 250,
            },
        }

    def calculate_dividend(self, symbol, price):
        """
        Calculate dividend.

        :param str symbol:
        :param float price:
        :return:
        """

        rule = self.exchange_table_data[symbol]

        if rule["type"] == "Common":
            dividend = rule["last_dividend"] / price
        else:
            dividend = rule["last_dividend"] * rule["value"] / price

        return dividend

    def calculate_pe_ration(self, symbol, price):
        """
        Calculate P/E Ratio.

        :param str symbol:
        :param float price:
        :return:
        """

        return price / self.calculate_dividend(symbol=symbol, price=price)

    def calculate_volume_weighted(self, symbol):
        """
        Calculate volume weighted.

        :param str symbol:
        :return:
        """

        last_fifteen_minutes = int((datetime.datetime.now() - datetime.timedelta(minutes=15)).strftime("%s"))
        total = 0
        quantities = 0

        for trade in self.trades.keys():
            if trade >= last_fifteen_minutes and self.trades[trade]["symbol"] == symbol:
                total = self.trades[trade]["quantity"] * self.trades[trade]["price"]
                quantities += self.trades[trade]["quantity"]

        quantities = 1 if quantities == 0 else quantities

        return total / quantities

    def calculate_gbce(self):
        """
        Calculate GBCE

        :return:
        """

        return sum([trade["price"] for trade in self.trades.values()])

    def add_record(self, symbol, quantity, buy=False):
        """
        Add record to the mem data.

        :param str symbol:
        :param float quantity:
        :param bool buy:
        :return:
        """

        timestamp = datetime.datetime.now().strftime("%s")
        self.trades[int(timestamp)] = {
            "symbol": symbol,
            "action": "buy" if buy else "sell",
            "quantity": quantity,
            "price": self.exchange_table_data[symbol]["value"]
        }

        print("Add with success! \n")

    def validate_symbol(self, symbol):
        """
        Validate if the given symbol is present in the table data.

        :param str symbol:
        :return:
        """

        if symbol not in self.exchange_table_data:
            raise ValueError("Symbol %s does not exist in table")

        return symbol

    def convert_to_float(self, value):
        """
        Convert value to float.

        :param str value:
        :return:
        """

        try:
            value = float(value)
        except ValueError:
            raise ValueError("Value is not correct")

        return value


class UnitTests(object):
    """
    Unit tests class regarding Accounting methods.

    Existing test calculate_dividend for Common and Preferred
    values

    Main attributes:
    quantity -> quantity for the stocks
    symbol -> stock symbol
    price -> stock price
    accounting -> Accounting object
    """

    __slots__ = ["quantity", "symbol", "price", "accounting"]

    def __init__(self, **kwargs):
        self.quantity = kwargs.get("quantity", 1)
        self.symbol = kwargs.get("symbol", "JOE")
        self.price = kwargs.get("quantity", 10)
        self.accounting = Accounting()

    def calculate_dividend(self, expected=1.3):
        """
        Test calculate value for Common stocks which use
        the last dividend.

        :param float expected:
        :return:
        """

        print("Running calculate_dividend(%s, %s) for Common -> Expected: %s" % (self.symbol, self.price, expected))

        assert self.accounting.calculate_dividend(self.symbol, self.price) == expected

    def calculate_dividend_fixed_dividend(self, expected=80):
        """
        Test calculate value for Preferred stocks which use
        the fixed dividend.

        :param float expected:
        :return:
        """

        print("Running calculate_dividend('GIN', %s) for Preferred -> Expected: %s" % (self.price, expected))

        assert self.accounting.calculate_dividend("GIN", self.price) == expected

    def run_all(self):
        """
        Run all the tests using default and expected values.

        :return:
        """

        try:
            self.calculate_dividend()
            self.calculate_dividend_fixed_dividend()

            print("Results tests -> OK")
        except AssertionError as err:
            print("Tests fail: %s" % err)


def menu():
    """
    Menu screen.

    :return:
    """

    print("---------------------------\n")
    print("1 - Calculate dividend\n")
    print("2 - Calculate P/E Ratio\n")
    print("3 - Add trade\n")
    print("4 - Calculate volume weighted stock for the past 15 minutes\n")
    print("5 - Calculate GBCE of all shares\n")
    print("6 - Run Unit Tests\n")
    print("7 - Leave\n")
    print("---------------------------\n")


if __name__ == "__main__":
    running = True
    accounting = Accounting()
    unit_tests = UnitTests()

    # Loop through the menu
    while running:
        menu()
        option = input("Select option: \n")

        try:
            if option == "1" or option == "2" or option == "3" or option == "4":
                symbol = input("Select a symbol: ")
                symbol = accounting.validate_symbol(symbol)

            if option == "1" or option == "2":
                price = input("Select a price: ")
                price = accounting.convert_to_float(price)

            if option == "1":
                print("Dividend --> %s\n" % accounting.calculate_dividend(symbol=symbol, price=price))
            elif option == "2":
                print("P/E Ration --> %s\n" % accounting.calculate_pe_ration(symbol=symbol, price=price))
            elif option == "3":
                quantity = input("Select a quantity: ")
                quantity = accounting.convert_to_float(quantity)
                buy = input("Is to buy? Yes(y) or No(n)")
                buy = True if buy == "y" else False

                accounting.add_record(symbol=symbol, quantity=quantity, buy=buy)
            elif option == "4":
                print("Volume --> %s\n" % accounting.calculate_volume_weighted(symbol=symbol))
            elif option == "5":
                print("GBCE of all shares --> %s\n" % accounting.calculate_gbce())
            elif option == "6":
                unit_tests.run_all()
            elif option == "7":
                running = False
                print("Leaving\n")
            else:
                print("Invalid option\n")
        except (KeyError, ValueError, Exception) as error:
            print("Something went wrong. Error: %s", error)