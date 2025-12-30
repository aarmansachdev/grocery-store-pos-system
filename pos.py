from store_backend import StoreBackend
from barcode import BarcodeProcessor
from cart import ShoppingCart
from member import Member


class POSSystem:
    def __init__(
        self,
        inventory_path: str,
        membership_path: str,
        coupon_path: str,
    ):
        self.backend = StoreBackend(inventory_path, membership_path, coupon_path)
        self.barcode_processor = BarcodeProcessor()
        self.cart = ShoppingCart()

    def process_barcodes(self, barcode_file_path: str) -> None:
        """For each line in the barcode file (length 95 strings), we will need to do the following:
        1. Validate the barcode
        2. If it doesn't work, flip the barcode and try again
        3.1 If it doesn't work, just skip the barcode
        3.2 If it does work, convert the barcode to 12 digits (and continue to step 4)
        4. Identify the type of the barcode (item, coupon, or membership)
        5. Process the barcode based on its type (update the shopping cart instance)
        """
        with open(barcode_file_path, 'r') as f:
            for line in f:
                binary_barcode = line.strip()

                if len(binary_barcode) != self.barcode_processor.BARCODE_LENGTH:
                    continue
                numeric = None
                try:
                    self.barcode_processor.validate_barcode(binary_barcode)
                    numeric = self.barcode_processor.convert_to_12_digits(binary_barcode)
                except ValueError:
                    flipped = self.barcode_processor.flip_barcode(binary_barcode)
                    try:
                        self.barcode_processor.validate_barcode(flipped)
                        numeric = self.barcode_processor.convert_to_12_digits(flipped)
                    except ValueError:
                        continue
                if numeric is None:
                    continue
                try:
                    barcode_type = self._identify_barcode_type(numeric)
                except ValueError:
                    continue

                if barcode_type == 'product':
                    product = self.backend.get_product(numeric)
                    if product:
                        self.cart.add_item(product)
                elif barcode_type == 'coupon':
                    coupon = self.backend.get_coupon(numeric)
                    if coupon:
                        self.cart.add_coupon(coupon)
                elif barcode_type == 'membership':
                    member = self.backend.get_member(numeric)
                    if member:
                        self.cart.add_membership(member)
            pass

    def scan(self, barcode_file_path: str):
        """Scan barcodes by processing them correctly."""
        self.process_barcodes(barcode_file_path)
        pass


    def _identify_barcode_type(self, numeric_barcode: str) -> str:
        """Given a barcode (length 12 string), identify the type of the barcode.

        Args:
            numeric_barcode (str): The barcode to identify.

        Returns:
            str: The type of the barcode.

        Raises:
            ValueError: If the numeric_barcode is invalid.
        """
        if len(numeric_barcode) != 12 or not numeric_barcode.isdigit():
            raise ValueError("Invalid barcode length or non-digit characters")

        first_digit = numeric_barcode[0]

        if first_digit == '0':
            return 'product'
        elif first_digit == '1':
            return 'coupon'
        elif first_digit == '2':
            return 'membership'
        else:
            raise ValueError("Invalid barcode type")
        pass

    def checkout(self) -> float:
        """Given the current cart, calculate the total price of the cart, with the coupon applied and membership applicable. We also need to update the inventory and membership databases.

        Returns:
            float: The total price of the cart.
        """
        total = self.cart.calculate_total()
        member = self.cart.get_membership()
        if member:
            self.backend.add_member_points(member, 10)
        for product in self.cart.get_items():
            self.backend.decrease_product_quantity(product, 1)
        self.backend.save_inventory()
        self.backend.save_memberships()

        return total
        pass

    def get_current_cart(self) -> ShoppingCart:
        return self.cart
        pass


def pos_doctests(self):
    """Function to run the doctests for the POSSystem class.

    Note that you should run this doctest at the root folder of the project
    (same level as main.py)

    It's recommended that you add additional doctests
    or test using by creating scripts like main.py

    >>> pos = POSSystem(
    ...     'db-data/inventory.csv',
    ...     'db-data/memberships.csv',
    ...     'db-data/coupons.csv'
    ... )
    >>> pos.process_barcodes('cart-data/scan_1_binary.txt')
    >>> cart = pos.get_current_cart()
    >>> items = cart.get_items()
    >>> len(items) == 2
    True
    >>> item_names = [item.get_name() for item in items]
    >>> 'Apple' in item_names and 'Cheddar Cheese' in item_names
    True
    >>> cart.get_membership().get_name() == 'John Smith'
    True
    >>> cart.get_membership().return_membership_type() == 'Gold'
    True
    >>> import math
    >>> math.isclose(pos.checkout(), 0.415, abs_tol=0.001)
    True
    >>> updated_memerships_exists = False
    >>> try:
    ...     f = open('db-data/updated_memberships.csv')
    ...     f.close()
    ...     updated_memerships_exists = True
    ... except FileNotFoundError:
    ...     updated_memerships_exists = False
    >>> updated_memerships_exists
    True
    >>> updated_inventory_exists = False
    >>> updated_inventory_exists = False
    >>> try:
    ...     f = open('db-data/updated_inventory.csv')
    ...     f.close()
    ...     updated_inventory_exists = True
    ... except FileNotFoundError:
    ...     updated_inventory_exists = False
    >>> updated_inventory_exists
    True
    >>> expected_types = ['coupon', 'membership', 'product', 'product']
    >>> calculated_types = []
    >>> with open('cart-data/scan_1.txt', 'r') as f:
    ...     for line in f:
    ...         numeric_barcode = line.strip()
    ...         barcode_type = pos._identify_barcode_type(numeric_barcode)
    ...         calculated_types.append(barcode_type)
    >>> expected_types == calculated_types
    True
    """
