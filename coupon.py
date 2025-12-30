from datetime import datetime


class Coupon:
    def __init__(
        self,
        numeric_barcode: str,
        expiration_date: datetime,
        min_purchase: float,
        description: str,
    ):
        self._barcode = numeric_barcode
        self._expiration_date = expiration_date
        self._min_purchase = min_purchase
        self._description = description
        pass

    def _is_expired(self) -> bool:
        """Check if the coupon is expired by comparing to current datetime.now()

        Returns:
            bool: True if the coupon is expired, False otherwise.
        """
        return datetime.now() > self._expiration_date
        pass

    def get_expiration_date(self):
        """Get the expiration date of the coupon.

        Returns:
             datetime: The expiration date of the coupon.
        """
        return self._expiration_date

    def discount_amount(self, subtotal: float) -> float:
        """Calculate the discount amount for the coupon.
        This is a placeholder for the actual discount amount. You will need to implement the actual discount amount in the subclasses.

        Args:
            subtotal (float): The subtotal of the cart.
        """
        if self._is_expired() or subtotal < self._min_purchase:
            return 0
        return round(subtotal * (self._percent_value / 100),3)
        pass


class PercentDiscountCoupon(Coupon):

    def __init__(
            self,
            numeric_barcode: str,
            expiration_date: datetime,
            min_purchase: float,
            description: str,
            percent_value: float,
        ):
            super().__init__(numeric_barcode, expiration_date, min_purchase, description)
            self._percent_value = percent_value
            pass

    def discount_amount(self, subtotal: float) -> float:
        """Calculates the percentage discount to subtract from the subtotal based on the coupon
        Args:
            subtotal (float): The subtotal of the cart
        Returns:
            float: The discount amount
        """
        if self._is_expired() or subtotal < self._min_purchase:
            return 0
        return round(subtotal * (self._percent_value / 100), 3)
        pass


class FixedDiscountCoupon(Coupon):
    def __init__(
        self,
        numeric_barcode: str,
        expiration_date: datetime,
        min_purchase: float,
        description: str,
        fixed_value: float,
    ):
        super().__init__(
            numeric_barcode, expiration_date, min_purchase, description
        )
        self.fixed_value = fixed_value
    def discount_amount(self, subtotal: float) -> float:
        """Calculates the fixed amount to subtract from the subtotal based on the coupon

        Args:
            subtotal (float): The subtotal of the cart
        Returns:
            float: The discount amount
        """
        if self._is_expired() or subtotal < self._min_purchase:
            return 0
        return min(float(self.fixed_value), subtotal)
        pass

    def apply_discount(self, subtotal: float) -> float:
        discount = self.discount_amount(subtotal)
        return round(subtotal - discount, 3)
        pass


def coupon_doctests():
    """Function to run the doctests for the Coupon class.
    >>> barcode = '012345678925'
    >>> expiration_date_not_expired = datetime(2025, 12, 31, 11, 59, 59)
    >>> expiration_date_expired = datetime(2024, 12, 31, 11, 59, 59)
    >>> min_purchase = 20.0
    >>> description = 'This is our tester!'
    >>> percent_value = 15.5
    >>> fixed_value = 30.0
    >>> test_coupon1 = PercentDiscountCoupon(barcode, \
                                expiration_date_expired, \
                                min_purchase, \
                                description, \
                                percent_value)
    >>> test_coupon1._is_expired()
    True
    >>> test_coupon2 = PercentDiscountCoupon(barcode, \
                                expiration_date_not_expired, \
                                min_purchase, \
                                description, \
                                percent_value)
    >>> test_coupon2._is_expired()
    False
    >>> test_percent = PercentDiscountCoupon(barcode, \
                                                expiration_date_not_expired, \
                                                min_purchase, \
                                                description, \
                                                percent_value)
    >>> test_percent.discount_amount(200.0)
    31.0
    >>> test_percent.discount_amount(15.0)
    0
    >>> test_fixed = FixedDiscountCoupon(barcode, \
                                            expiration_date_not_expired, \
                                            min_purchase, \
                                            description, \
                                            fixed_value)
    >>> test_fixed.discount_amount(200.0)
    30.0
    >>> test_fixed.discount_amount(20.0)
    20.0
    >>> test_fixed.discount_amount(10.0)
    0
    """
    def test_coupon_discount():
        """
        >>> from datetime import datetime, timedelta
        >>> barcode = '123456789012'
        >>> not_expired = datetime.now() + timedelta(days=10)
        >>> expired = datetime.now() - timedelta(days=10)
        >>> min_purchase = 50.0
        >>> description = 'Test coupon'
        >>> percent_value = 20.0

        >>> coupon = PercentDiscountCoupon(barcode, not_expired, min_purchase, description, percent_value)
        >>> coupon.discount_amount(100.0)
        20.0
        >>> coupon.apply_discount(100.0)
        80.0
        >>> coupon.discount_amount(40.0)
        0
        >>> coupon.apply_discount(40.0)
        40.0
        >>> coupon_expired = PercentDiscountCoupon(barcode, expired, min_purchase, description, percent_value)
        >>> coupon_expired.discount_amount(100.0)
        0
        >>> coupon_expired.apply_discount(100.0)
        100.0
        """
        pass
