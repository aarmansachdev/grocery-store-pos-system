
class BarcodeProcessor:
    LEFT_SIDE_MODULES = {
        "0001101": "0",
        "0011001": "1",
        "0010011": "2",
        "0111101": "3",
        "0100011": "4",
        "0110001": "5",
        "0101111": "6",
        "0111011": "7",
        "0110111": "8",
        "0001011": "9",
    }  # Dictionary mapping 7-bit binary modules to their corresponding digits

    RIGHT_SIDE_MODULES = {
        "1110010": "0",
        "1100110": "1",
        "1101100": "2",
        "1000010": "3",
        "1011100": "4",
        "1001110": "5",
        "1010000": "6",
        "1000100": "7",
        "1001000": "8",
        "1110100": "9",
    }  # Dictionary mapping 7-bit binary modules to their corresponding digits

    GUARDS = {"LEFT": "101", "CENTER": "01010", "RIGHT": "101"}

    BARCODE_LENGTH = 95
    LEFT_GUARD_LENGTH = RIGHT_GUARD_LENGTH = 3
    NUMBER_OF_MODULES = 6
    MODULE_WIDTH = 7
    CENTER_GUARD_LENGTH = 5

    def invert_barcode(self, binary_barcode: str) -> str:
        """Given a barcode (length 95 string), invert it.

        Args:
            binary_barcode (str): The barcode to invert.
        Returns:
            str: The inverted barcode.
        """
        if len(binary_barcode) != self.BARCODE_LENGTH:
            raise ValueError("Wrong length")
        return ''.join('1' if bit == '0' else '0' for bit in binary_barcode)
        

    def _validate_length(self, binary_barcode: str) -> bool:
        """Given a barcode (length 95 string), validate it.
        Checks for 95 length
        """
        if len(binary_barcode) != self.BARCODE_LENGTH:
            raise ValueError("Wrong length")
        return True
        

    def _validate_left_guard(self, binary_barcode: str) -> bool:
        """Given a barcode, validate it.
        Correct left guard pattern.

        """
        if binary_barcode[:3] != self.GUARDS["LEFT"]:
            raise ValueError("Wrong LEFT guard")
        return True
        

    def _validate_right_guard(self, binary_barcode: str) -> bool:
        """Given a barcode, validate it.
        Correct right guard pattern

        """
        if binary_barcode[-3:] != self.GUARDS["RIGHT"]:
            raise ValueError("Wrong RIGHT guard")
        return True

    def _validate_center_guard(self, binary_barcode: str) -> bool:
        """Given a barcode, validate it.
        Correct center guard pattern

        """
        center_index = len(binary_barcode) // 2  
        start = center_index - 2  
        end = center_index + 3    
        if binary_barcode[start:end] != self.GUARDS["CENTER"]:
            raise ValueError("Wrong CENTER guard")
        return True
        

    def _get_left_modules(self, binary_barcode: str) -> list[str]:
        """Given a barcode (length 95 string), get the left modules.

        Args:
            binary_barcode (str): The barcode to get the left modules from.
        Returns:
            list[str]: The left modules, each module is a length 7 string.
        """
        start = self.LEFT_GUARD_LENGTH  
        end = start + self.NUMBER_OF_MODULES * self.MODULE_WIDTH
        modules = [binary_barcode[i:i + self.MODULE_WIDTH] for i in range(start, end, self.MODULE_WIDTH)]
        return modules

    def _get_right_modules(self, binary_barcode: str) -> list[str]:
        """Given a barcode (length 95 string), get the right modules.

        Args:
            binary_barcode (str): The barcode to get the right modules from.
        Returns:
            list[str]: The right modules, each module is a length 7 string.
        """
        start = self.LEFT_GUARD_LENGTH + self.NUMBER_OF_MODULES * self.MODULE_WIDTH + self.CENTER_GUARD_LENGTH
        end = start + self.NUMBER_OF_MODULES * self.MODULE_WIDTH
        modules = [binary_barcode[i:i + self.MODULE_WIDTH] for i in range(start, end, self.MODULE_WIDTH)]
        return modules
        pass

    def _validate_modules(self, binary_barcode, module="LEFT") -> bool:
        """Given a barcode (length 95 string), validate the modules.

        Args:
            binary_barcode (str): The barcode to validate.
            module (str, optional): The module to validate. Defaults to "LEFT".

        Raises:
            ValueError: Wrong number of modules
            ValueError: Wrong length within module
            ValueError: Wrong number of ones in module
            ValueError: Wrong start or end in module

        Returns:
            bool: True if the modules are valid, Raising an error otherwise.
        """
        if module == "LEFT":
            modules = self._get_left_modules(binary_barcode)
            expected_ones_parity = 1
            expected_start, expected_end = '0', '1'
        else:
            modules = self._get_right_modules(binary_barcode)
            expected_ones_parity = 0
            expected_start, expected_end = '1', '0'

        if len(modules) != self.NUMBER_OF_MODULES:
            raise ValueError(f"Wrong number of {module} modules")

        for m in modules:
            if len(m) != self.MODULE_WIDTH:
                raise ValueError(f"Wrong length within {module} module")
            if m.count('1') % 2 != expected_ones_parity:
                raise ValueError(f"Wrong number of ones in {module} module")
            if not (m.startswith(expected_start) and m.endswith(expected_end)):
                raise ValueError(f"Wrong start or end in {module} module")
        return True


    def convert_to_12_digits(self, binary_barcode: str) -> str:
        """Given a barcode (length 95 string), convert it to 12 digits.

        Args:
            binary_barcode (str): The barcode to convert.
        Returns:
            str: The the 12 digit representation of the barcode.
        """
        left_modules = self._get_left_modules(binary_barcode)
        right_modules = self._get_right_modules(binary_barcode)

        left_digits = ''.join(self.LEFT_SIDE_MODULES[m] for m in left_modules)
        right_digits = ''.join(self.RIGHT_SIDE_MODULES[m] for m in right_modules)

        return left_digits + right_digits
    

    def modulo_check(self, numeric_barcode: str) -> bool:
        """Given a numeric barcode (length 12 string), check through the modulo check if it's read in properly.
        The modulo check is as follows:
            - Sum digits in odd positions (even index)
            - Sum digits in even positions (odd index)
            - Multiply the sum of the odd positions by 3
            - Add the sum of the even positions to the result
            - Take the next multiple of 10 of the result
            - Subtract the result from the next multiple of 10 of the result
            - If the result is equal to the check digit (last digit of barcode), the barcode is valid, otherwise it is invalid.

        Args:
            barcode_12 (str): The barcode to check.
        Returns:
            bool: True if the barcode is valid, Raising an error otherwise.
        """
        if len(numeric_barcode) != 12 or not numeric_barcode.isdigit():
           raise ValueError("Invalid barcode format")

        digits = [int(d) for d in numeric_barcode]
        check_digit = digits[-1]

        odd_sum = sum(digits[i] for i in range(0, 11, 2)) 
        even_sum = sum(digits[i] for i in range(1, 11, 2))

        total = odd_sum * 3 + even_sum
        nearest_10 = (total + 9) // 10 * 10
        computed_check = nearest_10 - total

        if computed_check != check_digit:
            raise ValueError("Security check failed")
        return True

    def validate_barcode(self, binary_barcode: str) -> bool:
        """Given a barcode (length 95 string), validate it. DEV: can use asserst here
        Checks for
            - 95 length X
            - correct guard pattern (LEFT and RIGHT and CENTER)
            - correct number of modules (6 for each side)
            - correct module width (7)
            - left modules have an odd number of 1s
            - left modules starts with 0 and ends with 1
            - right modules have an even number of 1s
            - right modules starts with 1 and ends with 0
            - Security check passes

        Args:
            binary_barcode (str): The barcode to validate.
        Returns:
            bool: True if the barcode is valid, False otherwise.
        """

        assert self._validate_length(binary_barcode)
        assert self._validate_left_guard(binary_barcode)
        assert self._validate_center_guard(binary_barcode)
        assert self._validate_right_guard(binary_barcode)

        assert self._validate_modules(binary_barcode, module="LEFT")
        assert self._validate_modules(binary_barcode, module="RIGHT")

        numeric_barcode = self.convert_to_12_digits(binary_barcode)
        assert self.modulo_check(numeric_barcode)

        return True

    def flip_barcode(self, barcode: str) -> str:
        """Return the barcode flipped (reversed).

        Args:
            barcode (str): The barcode to flip.

        Returns:
            str: The flipped barcode.
        """
        return barcode[::-1]


def barcode_doctests():
    """
    >>> from tester_student import generate_barcode_12, barcode_digits2binary
    >>> scanner = BarcodeProcessor()
    >>> valid_numeric = '252109613999'
    >>> valid_binary = barcode_digits2binary(valid_numeric)
    >>> invalid_numeric = '036000291439'
    >>> invalid_binary = barcode_digits2binary(invalid_numeric)
    >>> scanner._validate_length('')
    Traceback (most recent call last):
    ...
    ValueError: Wrong length
    >>> scanner._validate_length(valid_binary)
    True
    >>> scanner._validate_left_guard('101' + '0'*92)
    True
    >>> scanner._validate_right_guard('0'*92 + '101')
    True
    >>> scanner._validate_center_guard(valid_binary)
    True
    >>> scanner._validate_modules(valid_binary, module='LEFT')
    True
    >>> scanner._validate_modules(valid_binary, module='RIGHT')
    True
    >>> scanner.validate_barcode(valid_binary)
    True
    >>> scanner.modulo_check(valid_numeric)
    True
    >>> scanner.convert_to_12_digits(valid_binary) == valid_numeric
    True
    >>> scanner.modulo_check(invalid_numeric)
    Traceback (most recent call last):
    ...
    ValueError: Security check failed
    >>>
    >>> checks = []
    >>> with open('cart-data/scan_1_binary.txt', 'r') as f:
    ...     for binary_barcode in f:
    ...         binary_barcode = binary_barcode.strip()
    ...         is_valid = scanner.validate_barcode(binary_barcode)
    ...         checks.append(is_valid)
    >>> all(checks)
    True

    >>> checks = []
    >>> with open('cart-data/scan_1.txt', 'r') as f:
    ...     for line in f:
    ...         numeric_barcode = line.strip()
    ...         is_valid = scanner.modulo_check(numeric_barcode)
    ...         checks.append(is_valid)
    >>> all(checks)
    True
    """
