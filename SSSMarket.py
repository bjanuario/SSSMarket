import datetime

EXCHANGE_TABLE_DATA = {
    "TEA": {
        "type": "Common",
        "last_dividend": 0,
        "fixed_dividend": None,
        "value": 100,
    }, "POP": {
        "type": "Common",
        "last_dividend": 8,
        "fixed_dividend": None,
        "value": 100,
    }, "ALE": {
        "type": "Common",
        "last_dividend": 23,
        "fixed_dividend": None,
        "value": 60,
    }, "GIN": {
        "type": "Preferred",
        "last_dividend": 8,
        "fixed_dividend": 0.02,
        "value": 100,
    }, "JOE": {
        "type": "Common",
        "last_dividend": 13,
        "fixed_dividend": None,
        "value": 250,
    },
}

# Mem data
TRADES = {}


def calculate_dividend(symbol, price):
    """
    Calculate dividend.

    :param str symbol:
    :param float price:
    :return:
    """

    rule = EXCHANGE_TABLE_DATA[symbol]

    if rule["type"] == "Common":
        dividend = rule["last_dividend"] / price
    else:
        dividend = rule["last_dividend"] * rule["value"] / price

    return dividend


def calculate_pe_ration(symbol, price):
    """
    Calculate P/E Ratio.

    :param str symbol:
    :param float price:
    :return:
    """

    return price / calculate_dividend(symbol=symbol, price=price)


def calculate_volume_weighted(symbol):
    """
    Calculate volume weighted.

    :param str symbol:
    :return:
    """

    last_fifteen_minutes = int(datetime.datetime.now() + datetime.timedelta(minutes=15).strftime("%s"))
    total = 0
    quantities = 0

    for trade in TRADES.keys():
        if trade >= last_fifteen_minutes and trade["symbol"] == symbol:
            total = TRADES[trade]["quantity"] * TRADES[trade]["price"]
            quantities += TRADES[trade]["quantity"]

    return total / quantities


def calculate_gbce():
    """
    Calculate GBCE

    :return:
    """

    return sum([trade["price"] for trade in TRADES])


def add_record(symbol, quantity, buy=False):
    """
    Add record to the mem data.

    :param str symbol:
    :param float quantity:
    :param bool buy:
    :return:
    """

    timestamp = datetime.datetime.now().strftime("%s")
    TRADES[int(timestamp)] = {
        "symbol": symbol,
        "action": "buy" if buy else "sell",
        "quantity": quantity,
        "price": EXCHANGE_TABLE_DATA[symbol]["value"]
    }

    print("Add with success! \n")


def validate_symbol(symbol):
    """
    Validate if the given symbol is present in the table data.

    :param str symbol:
    :return:
    """

    if symbol not in EXCHANGE_TABLE_DATA:
        raise ValueError("Symbol %s does not exist in table")

    return symbol


def convert_to_float(value):
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
    print("6 - Leave\n")
    print("---------------------------\n")


if __name__ == "__main__":
    running = True
    # Loop through the menu
    while running:
        menu()
        option = input("Select option: \n")

        try:
            if option == "1" or option == "2" or option == "3" or option == "4":
                symbol = input("Select a symbol: ")
                symbol = validate_symbol(symbol)

            if option == "1" or option == "2":
                price = input("Select a price: ")
                price = convert_to_float(price)

            if option == "1":
                print("Dividend --> %s\n" % calculate_dividend(symbol=symbol, price=price))
            elif option == "2":
                print("P/E Ration --> %s\n" % calculate_pe_ration(symbol=symbol, price=price))
            elif option == "3":
                quantity = input("Select a quantity: ")
                quantity = convert_to_float(quantity)
                buy = input("Is to buy? Yes(y) or No(n)")
                buy = True if buy == "y" else False

                add_record(symbol=symbol, quantity=quantity, buy=buy)
            elif option == "4":
                print("Volume --> %s\n" % calculate_volume_weighted(symbol=symbol))
            elif option == "5":
                print("GBCE of all shares --> %s\n" % calculate_gbce())
            elif option == "6":
                running = False
                print("Leaving\n")
            else:
                print("Invalid option\n")
        except (KeyError, ValueError, Exception) as error:
            print("Something went wrong. Error: %s", error)