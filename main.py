from data import MENU, machine_resources


resources = machine_resources


def format_report(resources_data):
    """Returns printable format of report."""
    water_qty = f"{resources_data["water"]}ml"
    milk_qty = f"{resources_data["milk"]}ml"
    coffee_qty = f"{resources_data["coffee"]}g"
    if "profit" in resources_data:
        money_qty = f"${resources_data["profit"]}"
    else:
        money_qty = "$0"
    return f"Water: {water_qty} \nMilk: {milk_qty} \nCoffee: {coffee_qty} \nProfit: {money_qty}"


def check_enough_resources(product, menu, current_resources):
    """Returns TRUE if are enough resources to make the ordered drink or False otherwise."""
    product_ingredients = menu[product]["ingredients"]
    for ingredient in product_ingredients:
        if current_resources[ingredient] - product_ingredients[ingredient] < 0:
            print(f"Sorry there is not enough {ingredient}.")
            return False
    return True


def process_input_coins():
    """Calculates the total input coins in $ and returns the result."""
    quarters = int(input("How many quarters?: "))
    dimes = int(input("How many dimes?: "))
    nickles = int(input("How many nickles?: "))
    pennies = int(input("How many pennies?: "))

    """
    Coin Operated
    Quarter -> 25 cents -> $0.25
    Dime -> 10 cents -> $0.10
    Nickel -> 5 cents -> $0.05
    Penny -> 1 cent -> $0.01
    """

    return 0.25 * quarters + 0.1 * dimes + 0.05 * nickles + 0.01 * pennies


def make_coffee(menu, current_resources, product):
    """Calculates the new quantity of resources that the machine has
    after order and print feedback to user."""
    menu_ingredients = menu[product]["ingredients"]
    for resource in current_resources:
        if resource in menu_ingredients:
            current_resources[resource] -= menu_ingredients[resource]
        else:
            current_resources[resource] = current_resources[resource]
    print(f"Here is your {product} ☕. Enjoy!")


def print_menu(menu):
    """Prints the menu products with its cost and ingredients."""

    for product in menu:
        print(f"{product.capitalize()}: ${menu[product]["cost"]}")
        ingredients = menu[product]["ingredients"]
        print("  Ingredients:")
        for ingredient in ingredients:
            if product == "coffee":
                print(f"    {ingredient.capitalize()}: {ingredients[ingredient]}g")
            else:
                print(f"    {ingredient.capitalize()}: {ingredients[ingredient]}ml")
        print("-----------------------")


def check_enough_funds(product_price, user_payment):
    """If user has enough funds returns True and calculates the change for user,
    otherwise returns False.
    In both cases, user receives a feedback  with the status of order."""
    if product_price > user_payment:
        print("Sorry that's not enough money. Money refunded. ")
        return False
    else:
        change = user_payment - product_price
        print(f"Here is ${round(change, 2)} dollars in change.")
        return True


def order_coffee():
    global resources
    turn_off = False
    while not turn_off:
        user_choice = input("What would you like? (espresso/latte/cappuccino/menu): ").lower()

        if user_choice == "off":
            turn_off = True
        elif user_choice == "report":
            print(format_report(resources))
        elif user_choice in MENU:
            enough_resources = check_enough_resources(user_choice, MENU, resources)

            if enough_resources:
                print("Please insert coins.")
                payment = process_input_coins()
                product_cost = MENU[user_choice]["cost"]

                enough_funds = check_enough_funds(product_cost, payment)
                if enough_funds:
                    if "profit" not in resources:
                        resources["profit"] = product_cost
                    else:
                        resources["profit"] += product_cost

                    make_coffee(MENU, resources, user_choice)
        elif user_choice == 'menu':
            print_menu(MENU)
        else:
            print("Invalid choice. Choose a product from MENU.")


order_coffee()
