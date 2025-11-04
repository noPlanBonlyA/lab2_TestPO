"""Calculator class with basic mathematical operations."""

import math
from typing import Union

Number = Union[int, float]


class Calculator:
    """A calculator class with basic mathematical operations."""
    
    def __init__(self):
        self.last_result = 0
    
    def add(self, a: Number, b: Number) -> Number:
        result = a + b
        self.last_result = result
        return result
    
    def subtract(self, a: Number, b: Number) -> Number:
        result = a - b
        self.last_result = result
        return result
    
    def multiply(self, a: Number, b: Number) -> Number:
        result = a * b
        self.last_result = result
        return result
    
    def divide(self, a: Number, b: Number) -> Number:
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        result = a / b
        self.last_result = result
        return result
    
    def power(self, base: Number, exponent: Number) -> Number:
        """Raises base to the power of exponent."""
        try:
            if base < 0 and not isinstance(exponent, int):
                raise ValueError("Cannot raise negative number to non-integer power")
            result = base ** exponent
            if math.isnan(result) or math.isinf(result):
                raise ValueError("Operation resulted in invalid number")
            self.last_result = result
            return result
        except OverflowError:
            raise ValueError("Operation resulted in overflow")
    
    def square_root(self, number: Number) -> Number:
        """Calculate square root of a number."""
        if number < 0:
            raise ValueError("Cannot calculate square root of negative number")
        result = math.sqrt(number)
        self.last_result = result
        return result
    
    def get_last_result(self) -> Number:
        return self.last_result
    
    def clear(self) -> None:
        """Reset the last result to zero."""
        self.last_result = 0
