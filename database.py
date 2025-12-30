from product import Product
from member import Member, SilverMember, GoldMember, PlatinumMember
from coupon import Coupon, PercentDiscountCoupon, FixedDiscountCoupon
from datetime import datetime
import csv


class ProductDatabase:
    SAVE_PATH = "db-data/updated_inventory.csv"

    def __init__(self, inventory_path):
        self.products = {}
        with open(inventory_path, 'r') as f:
            lines = f.readlines()
            for line in lines[1:]:
                line = line.strip()
                if line:
                    parts = [x.strip() for x in line.split(',')]
                    barcode, name, price, quantity = parts
                    product = Product(barcode, name, float(price), int(quantity))
                    self.products[barcode] = product

    def get_product(self, numeric_barcode: str) -> Product:
        """Given a barcode, return the Product object associated with that\
        barcode.

        Args:
            numeric_barcode (str): 12 digit numeric barcode
        Returns:
            Product with barcode (None if not found)
        """
        return self.products.get(numeric_barcode)
        pass

    def decrement_inventory(self, numeric_barcode: str, quantity: int):
        """Given a barcode and a quantity to decrease by, decrement the inventory of the product associated with that barcode by the quantity.

        Args:
            numeric_barcode (str): _description_
            quantity (int): _description_
        """
        product = self.get_product(numeric_barcode)
        if product is not None:
            product.decrease_quantity(quantity)
        else:
            pass

    def save_inventory(self):
        """Save the inventory to a CSV file"""
        with open(self.SAVE_PATH, 'w') as f:
            f.write("barcode,name,price,quantity\n")
            for product in self.products.values():
                f.write(f"{product.get_barcode()},{product.get_name()},{product.get_price()},{product.get_quantity()}\n")

class MemberDatabase:
    SAVE_PATH = "db-data/updated_memberships.csv"

    def __init__(self, membership_path: str):
        self.memberships = {}
        with open(membership_path, 'r') as f:
            lines = f.readlines()
            for line_num, line in enumerate(lines[1:], start=2):
                line = line.strip()
                if line:
                    parts = [x.strip() for x in line.split(',')]
                    if len(parts) != 4:
                        print(f"WARNING: Skipping malformed line {line_num}: {line}")
                        continue

                    barcode, name, tier, points = parts
                    points = float(points)  # Use float

                    if tier == 'Silver':
                        member = SilverMember(barcode, name, points)
                    elif tier == 'Gold':
                        member = GoldMember(barcode, name, points)
                    elif tier == 'Platinum':
                        member = PlatinumMember(barcode, name, points)
                    elif tier == 'Member':
                        member = Member(barcode, name, points)
                    else:
                        print(f"WARNING: Unknown tier '{tier}' on line {line_num} for barcode {barcode}. Skipping.")
                        continue

                    self.memberships[barcode] = member

    def save_inventory(self):
        """Save the inventory to a CSV file"""
        with open(self.SAVE_PATH, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["barcode", "name", "price", "quantity"])
            for product in self.products.values():
                writer.writerow(["barcode", "name", "price", "quantity"])
                for product in self.products.values():
                    writer.writerow([
                    product.get_barcode(),
                    product.get_name(),
                    product.get_price(),
                    product.get_quantity()
                ])  

        pass

    def get_member(self, numeric_barcode: str) -> Member:
        """Given a barcode, assert that the member is registered, and if so, return the Member object associated with that barcode.
        Args:
            numeric_barcode (str): The barcode of the member to check.

        Returns:
            Member: The Member object associated with the barcode. (None if not associated with a member)
        """
        return self.memberships.get(numeric_barcode)

    def add_points(self, numeric_barcode: str, points: int):
        """Given a barcode, add the specified number of points to the member associated with that barcode.

        Args:
            numeric_barcode (str): The barcode of the member to add points to.
            points (int): The number of points to add.
        """
        member = self.get_member(numeric_barcode)
        if member:
            member.add_points(points)
        pass

    def save_memberships(self):
        with open(self.SAVE_PATH, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["barcode", "name", "tier", "points"])
            for member in self.memberships.values():
                if isinstance(member, SilverMember):
                    tier = 'Silver'
                elif isinstance(member, GoldMember):
                    tier = 'Gold'
                elif isinstance(member, PlatinumMember):
                    tier = 'Platinum'
                else:
                    tier = 'Member'
                writer.writerow([
                    member.get_barcode(),
                    member.get_name(),
                    tier,       
                    member.get_points()
                ])

class CouponDatabase:

    def __init__(self, coupon_path):
        self.coupons = {}
        with open(coupon_path, 'r') as f:
            lines = f.readlines()
            for line in lines[1:]:
                line = line.strip()
                if line:
                    parts = [x.strip() for x in line.split(',')]
                    barcode, expiration, discount_type, discount_value, min_purchase, description = parts
                    expiration = datetime.strptime(expiration, '%Y-%m-%d')
                    discount_value = float(discount_value)
                    min_purchase = float(min_purchase)
                    if discount_type == 'percent':
                        coupon = PercentDiscountCoupon(barcode, expiration, min_purchase, description, discount_value)
                    elif discount_type == 'fixed':
                        coupon = FixedDiscountCoupon(barcode, expiration, min_purchase, description, discount_value)
                    self.coupons[barcode] = coupon

        pass

    def get_coupon(self, numeric_barcode: str) -> Coupon:
        """Given a barcode, return the Coupon object associated with that barcode."""
        return self.coupons.get(numeric_barcode)
        pass


def product_database_doctests():
    """Function to run the doctests for the ProductDatabase class.

    Note that you should run this doctest at the root folder of the project
    (same level as main.py)

    It's recommended that you add additional doctests

    >>> pdb = ProductDatabase('db-data/inventory.csv')
    >>> milk_barcode = '012345678905'
    >>> milk = pdb.get_product(milk_barcode)
    >>> milk.get_quantity() == 150
    True
    >>> pdb.decrement_inventory(milk_barcode, 10)
    >>> milk.get_quantity() == 140
    True
    >>> pdb.save_inventory()
    >>> pdb2 = ProductDatabase('db-data/inventory.csv')
    >>> milk2 = pdb2.get_product(milk_barcode)
    >>> milk2.get_quantity() == 150
    True
    >>> pdb3 = ProductDatabase('db-data/updated_inventory.csv')
    >>> milk3 = pdb3.get_product(milk_barcode)
    >>> milk3.get_quantity() == 140
    True
    """


def member_database_doctests():
    """Function to run the doctests for the MemberDatabase class.

    Note that you should run this doctest at the root folder of the project
    (same level as main.py)

    It's recommended that you add additional doctests

    >>> mdb = MemberDatabase('db-data/memberships.csv')
    >>> jane_barcode = '257274767454'
    >>> jane = mdb.get_member(jane_barcode)
    >>> jane.get_points() == 1200
    True
    >>> mdb.add_points(jane_barcode, 100)
    >>> jane.get_points() == 1300
    True
    >>> mdb.save_memberships()
    >>> file_exists = None
    >>> try:
    ...     f = open('db-data/updated_memberships.csv')
    ...     f.close()
    ...     file_exists = True
    ... except FileNotFoundError:
    ...     file_exists = False
    >>> file_exists
    True
    """


def coupon_database_doctests():
    """Function to run the doctests for the CouponDatabase class.

    Note that you should run this doctest at the root folder of the project
    (same level as main.py)

    It's recommended that you add additional doctests

    >>> cdb = CouponDatabase('db-data/coupons.csv')
    >>> sample_coupon_barcode = '149234073227'
    >>> coupon = cdb.get_coupon(sample_coupon_barcode)
    >>> isinstance(coupon, PercentDiscountCoupon)
    True
    """
