""" CSC148 Summer 2021 Term Test 1
Q1: Object Oriented Programming [25 marks]
-----------------------------------------------------------------

Create class definitions for the following two classes:
- [20 marks] RetailFranchise
    A RetailFranchise has an address, name, promoted line, and catalogue.
    The address **MUST** be an instance of class Address.

    Required methods:
      - record_customer
      - checkout

- [5 marks] Address
    An Address has a street number, street name, city, province, postal code,
    and country. The default country must be set with the DEFAULT_COUNTRY
    constant that has been defined for you.

Refer to the __main__ block for usage of these classes. In particular, a
RetailFranchise **MUST** checkout customers in a FIFO Queue order.

You may choose any reasonable way to store the necessary data, that permits the
code in the __main__ block to run. You may add imports from the typing module,
but do NOT add any other imports.

You are not graded on style for Q1. You are not required to write docstrings.
"""

from __future__ import annotations
from typing import Dict

DEFAULT_COUNTRY = "Canada"

class Address():
    def __init__(self, strt_num, strt_name, city, prvnc, pst_code):
        self.street_num = strt_num
        self.street_name = strt_name
        self.city = city
        self.province = prvnc
        self.postal_code = pst_code
        self.country = DEFAULT_COUNTRY

class RetailFranchise:
    def __init__(self, address: Address, name, promoted_line, catalogue):
        self.address = address
        self.name = name
        self.promoted_line = promoted_line
        self.catalogue = catalogue
        self.customer = []

    def record_customer(self, customer):
        self.customer.append(customer)

    def checkout(self, tax_rates) -> tuple:
        cost = 0
        for item_ in self.customer[0]:
            if item_ in self.catalogue:
                cost += self.catalogue[item_] * self.customer[0][item_]

        cost_tax = cost + tax_rates[self.address.province]

        return (cost, cost_tax)



if __name__ == "__main__":
    uniqlo_catalogue = {
        "leggings pants": 20.00,
        "cotton t-shirt": 20.00,
        "socks": 5.00,
        "hat": 10.00
    }

    uniqlo_address = Address(
        220, "Yonge St.", "Toronto", "ON", "M5B 2H1"
    )

    uniqlo = RetailFranchise(
        uniqlo_address,
        "UNIQLO",
        "Airism",
        uniqlo_catalogue
    )

    tax_rates = {
        "ON": 0.13, "QC": 0.15, "AB": 0.05,
        "BC": 0.12, "MB": 0.12, "NB": 0.15,
        "NL": 0.15, "NT": 0.05, "NS": 0.15,
        "NU": 0.05, "PE": 0.15, "SK": 0.11,
        "YT": 0.05
    }

    # baskets are given as a dictionary where the keys are the item,
    # with the corresponding value as the quantity of that item
    customer_basket_1 = {
        "leggings pants": 2,
        "socks": 1
    }

    customer_basket_2 = {
        "hat": 1,
        "cotton t-shirt": 3
    }

    customers = [customer_basket_1, customer_basket_2]
    for customer in customers:
        uniqlo.record_customer(customer)

    print("Welcome to", uniqlo.name)
    print("Have you checked out our", uniqlo.promoted_line, "products?")
    for i in range(len(customers)):
        print("--- Processing customer #" + str(i + 1), "---")

        # !!!! HINT: RetailFranchise.checkout() should return
        #            a two-element tuple of the
        #            (total before tax, total after tax)

        subtotal, total = uniqlo.checkout(tax_rates)
        print("Subtotal:", subtotal)
        print("Total after tax:", total)
        print("!! Order", i + 1, "is ready.")
