from database import ProductDatabase, MemberDatabase, CouponDatabase
from product import Product
from member import Member
from coupon import Coupon


class StoreBackend:
    """I think we can provide this class fully implemented"""

    def __init__(self, inventory_path: str, membership_path: str, coupon_path: str):
        self.product_database = ProductDatabase(inventory_path)
        self.member_database = MemberDatabase(membership_path)
        self.coupon_database = CouponDatabase(coupon_path)

    def get_product(self, numeric_barcode: str) -> Product:
        return self.product_database.get_product(numeric_barcode)

    def decrease_product_quantity(self, product: Product, quantity: int):
        """Given a product and a quantity to decrease by, decrement the inventory of the product by the quantity.

        Args:
            product (Product): The product to decrease the quantity of.
            quantity (int): The quantity to decrease by.
        """
        self.product_database.decrement_inventory(product.get_barcode(), quantity)

    def get_member(self, numeric_barcode: str) -> Member:
        return self.member_database.get_member(numeric_barcode)

    def add_member_points(self, member: Member, points: int):
        """Given a member and a quantity to increase by, increment the points of the member by the quantity.

        Args:
            member (Member): The member to update the points of.
            points (int): The points to increase by.
        """
        self.member_database.add_points(member.get_barcode(), points)

    def get_coupon(self, numeric_barcode: str) -> Coupon:
        return self.coupon_database.get_coupon(numeric_barcode)

    def save_inventory(self):
        self.product_database.save_inventory()

    def save_memberships(self):
        self.member_database.save_memberships()


def store_backend_doctests():
    """Function to run the doctests for the StoreBackend class.

    Note that you should run this doctest at the root folder of the project
    (same level as main.py)

    It's recommended that you add additional doctests

    >>> store_backend = StoreBackend('db-data/inventory.csv', 'db-data/memberships.csv', 'db-data/coupons.csv')
    >>> store_backend is not None
    True
    >>> milk_barcode = '012345678905'
    >>> milk = store_backend.get_product(milk_barcode)
    >>> milk.get_name() == 'Milk'
    True
    >>> milk.get_price() == 2.99
    True
    >>> milk.get_quantity() == 150
    True
    >>> store_backend.decrease_product_quantity(milk, 10)
    >>> milk.get_quantity() == 140
    True
    >>> non_existent_barcode = ''
    >>> store_backend.get_product(non_existent_barcode) is None
    True
    >>> jane_barcode = '257274767454'
    >>> jane = store_backend.get_member(jane_barcode)
    >>> jane.get_points() == 1200
    True
    >>> store_backend.add_member_points(jane, 100)
    >>> jane.get_points() == 1300
    True
    """
