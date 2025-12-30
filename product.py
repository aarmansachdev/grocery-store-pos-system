class Product:
    def __init__(
        self, numeric_barcode: str, name: str, price: float, quantity: int
    ):
        self.numeric_barcode = numeric_barcode
        self.name = name
        self.price = float(price)
        self.quantity = quantity

        pass

    def decrease_quantity(self, quantity: int):
        """Decrease the quantity of the product by the specified quantity.

        Args:
            quantity (int): The quantity to decrease by.
        """
        self.quantity = max(0, self.quantity - quantity)
        pass

    def is_in_stock(self) -> bool:
        """Check if the quantity of the product is greater than 0.

        Returns:
            bool: True if the product is in stock, False otherwise.
        """
        return self.quantity > 0
        pass

    def get_barcode(self) -> str:
        """Get the barcode of the product.

        Returns:
            str: The barcode of the product.
        """
        return str(self.numeric_barcode)
        pass

    def get_name(self) -> str:
        """Get the name of the product.

        Returns:
            str: The name of the product.
        """
        return str(self.name)
        pass

    def get_price(self) -> float:
        """Get the price of the product.

        Returns:
            float: The price of the product.
        """
        return float(self.price)
        pass

    def get_quantity(self) -> int:
        """Get the quantity of the product.

        Returns:
            int: The quantity of the product.
        """
        return self.quantity
        pass

    def get_unit_price(self) -> float:
        """Get the unit price of the product.

        Returns:
            float: The price of a single unit of the product.
        """
        return float(self.price)
        pass


def product_doctests():
    """Function to run the doctests for the Product class.
    >>> numeric_barcode = '012345678905'
    >>> p = Product(numeric_barcode, 'Test', 10.0, 5)
    >>> p.get_barcode() == numeric_barcode
    True
    >>> p.get_name() == 'Test'
    True
    >>> p.get_price() == 10.0
    True
    >>> p.get_quantity() == 5
    True
    >>> p.is_in_stock()
    True
    >>> p.decrease_quantity(5)
    >>> p.get_quantity() == 0
    True
    >>> p.is_in_stock()
    False
    """
