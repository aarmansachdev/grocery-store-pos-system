from product import Product
from member import Member, SilverMember, GoldMember, PlatinumMember
from coupon import Coupon, FixedDiscountCoupon, PercentDiscountCoupon
from datetime import datetime


class ShoppingCart:
    def __init__(self):
        self.items = []
        self.membership = None
        self.coupons = []

        pass

    def add_item(self, item: Product):
        """Add the specified item to the cart.

        Args:
            item (Product): The item to add to the cart.
        """
        self.items.append(item)
        pass

    def add_membership(self, membership: Member):
        """Add a membership to the cart.

        Args:
            membership (Member): The membership to add to the cart.
        """
        self.membership = membership
        pass

    def add_coupon(self, coupon: Coupon):
        """Add a coupon to the cart.

        Args:
            coupon (Coupon): The coupon to add to the cart.
        """
        if coupon not in self.coupons:
            if coupon.get_expiration_date() >= datetime.now():
                self.coupons.append(coupon)

        pass

    def get_items(self) -> list[Product]:
        """Get the items in the cart.

        Returns:
            list[Product]: The items in the cart.
        """
        return self.items
        pass

    def get_membership(self) -> Member:
        """Get the membership in the cart.

        Returns:
            Member: The membership in the cart.
        """
        return self.membership
        pass

    def get_coupons(self) -> list[Coupon]:
        """Get the coupons in the cart.

        Returns:
            list[Coupon]: The coupons in the cart.
        """
        return self.coupons
        pass

    def calculate_subtotal(self) -> float:
        """Calculate the price of all items in the cart.

        Returns:
            float: The subtotal of the cart.
        """
        return sum(item.get_unit_price() for item in self.items)
        pass

    def calculate_total(self) -> float:
        """Calculate the total price of the cart, with coupon applied and membership applicable

        Returns:
            float: The total price of the cart.
        """
        subtotal = self.calculate_subtotal()
        if self.membership is not None:
            subtotal = self.membership.apply_discount(subtotal)
        if self.coupons:
            coupon = self.coupons[0]
            subtotal = coupon.apply_discount(subtotal)

        return float(subtotal)

        pass

    def __str__(self):
        """Return a string representation of the shopping cart. This is for debugging purposes

        Returns:
            str: A formatted string showing the cart's contents, membership, coupons, and totals.
        """
        lines = [f"Items: {[item.get_name() for item in self.items]}"]
        lines.append(f"Membership: {self.membership.get_name() if self.membership else 'None'}")
        lines.append(f"Coupons: {[coupon.get_barcode() for coupon in self.coupons]}")
        lines.append(f"Subtotal: {self.calculate_subtotal():.2f}")
        lines.append(f"Total: {self.calculate_total():.2f}")
        return "\n".join(lines)
        pass


def shopping_cart_doctests():
    """Function to run the doctests for the ShoppingCart class.

    Note that you should run this doctest at the root folder of the project
    (same level as main.py)

    # It's recommended that you add additional doctests

    >>> cart = ShoppingCart()
    >>> cart.add_item(Product('random_barcode', 'Milk', 2, 150))
    >>> cart.add_item(Product('random_barcode2', 'Bread', 3, 80))
    >>> cart.calculate_subtotal() == 5 == cart.calculate_total()
    True
    >>> sm = PlatinumMember('random_barcode3', 'John', 0)
    >>> cart.add_membership(sm)
    >>> cart.calculate_total() == 4.5
    True
    >>> from datetime import datetime
    >>> fc = FixedDiscountCoupon('b4', datetime(2030, 1, 1), 1, 'desc', 1)
    >>> cart.add_coupon(fc)
    >>> cart.calculate_total() == 3.5
    True
    >>> cart.add_coupon(fc)
    >>> len(cart.get_coupons()) == 1
    True
    >>> len(cart.get_items()) == 2
    True
    """
