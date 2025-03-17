from typing import TypeVar, Any, Union

from sqlalchemy.sql.functions import ReturnTypeFromArgs

_T = TypeVar("_T", bound=Any)
Number = Union[int, float]


# Base class for all arithmetic functions.
class ArithmeticFunction(ReturnTypeFromArgs[Union[int, float]]):
    """Base class for ClickHouse arithmetic functions."""
    pass


# -------------------------------------------------------------------
# Basic arithmetic operations
# -------------------------------------------------------------------

class plus(ArithmeticFunction[_T]):
    """Returns the sum of two numbers.

    ClickHouse:
        plus(x, y) returns x + y.
    """
    pass


class minus(ArithmeticFunction[_T]):
    """Returns the difference between two numbers.

    ClickHouse:
        minus(x, y) returns x - y.
    """
    pass


class multiply(ArithmeticFunction[_T]):
    """Returns the product of two numbers.

    ClickHouse:
        multiply(x, y) returns x * y.
    """
    pass


class divide(ArithmeticFunction[_T]):
    """Returns the quotient of two numbers.

    ClickHouse:
        divide(x, y) returns x / y.
        Note: Division by zero will raise an exception.
    """
    pass


# -------------------------------------------------------------------
# Integer division functions
# -------------------------------------------------------------------

class intDiv(ArithmeticFunction[_T]):
    """Returns the integer division of two numbers.

    ClickHouse:
        intDiv(x, y) returns the integer quotient of x divided by y.
        Note: Throws an exception if y is zero.
    """
    pass


class intDivOrZero(ArithmeticFunction[_T]):
    """Returns the integer division of two numbers or zero if the divisor is zero.

    ClickHouse:
        intDivOrZero(x, y) returns 0 when y is 0; otherwise, returns intDiv(x, y).
    """
    pass


# -------------------------------------------------------------------
# Floating point tests and modulo functions
# -------------------------------------------------------------------

class isFinite(ArithmeticFunction[_T]):
    """Checks if a number is finite (not infinity or NaN).

    ClickHouse:
        isFinite(x) returns 1 if x is finite, 0 otherwise.
    """
    pass


class isInfinite(ArithmeticFunction[_T]):
    """Checks if a number is infinite.

    ClickHouse:
        isInfinite(x) returns 1 if x is either +Inf or -Inf, 0 otherwise.
    """
    pass


class isNotFinite(ArithmeticFunction[_T]):
    """Checks if a number is not finite (either infinity or NaN).

    ClickHouse:
        isNotFinite(x) returns 1 if x is not finite, 0 otherwise.
    """
    pass


class isNaN(ArithmeticFunction[_T]):
    """Checks if a number is NaN (Not a Number).

    ClickHouse:
        isNaN(x) returns 1 if x is NaN, 0 otherwise.
    """
    pass


class modulo(ArithmeticFunction[_T]):
    """Returns the remainder of the division of two numbers.

    ClickHouse:
        modulo(x, y) returns x % y.
    """
    pass


class moduloOrZero(ArithmeticFunction[_T]):
    """Returns the remainder of the division of two numbers, or 0 if the divisor is zero.

    ClickHouse:
        moduloOrZero(x, y) returns 0 when y is 0; otherwise, returns modulo(x, y).
    """
    pass


class positiveModulo(ArithmeticFunction[_T]):
    """Returns a non-negative remainder of the division.

    ClickHouse:
        positiveModulo(x, y) returns a positive remainder even when x is negative.
    """
    pass


class negate(ArithmeticFunction[_T]):
    """Returns the negation of the number.

    ClickHouse:
        negate(x) returns -x.
    """
    pass


class abs(ArithmeticFunction[_T]):
    """Returns the absolute value of the number.

    ClickHouse:
        abs(x) returns the absolute value.
    """
    pass


# -------------------------------------------------------------------
# Greatest common divisor and least common multiple
# -------------------------------------------------------------------

class gcd(ArithmeticFunction[_T]):
    """Returns the greatest common divisor of two numbers.

    ClickHouse:
        gcd(x, y) computes the greatest common divisor.
    """
    pass


class lcm(ArithmeticFunction[_T]):
    """Returns the least common multiple of two numbers.

    ClickHouse:
        lcm(x, y) computes the least common multiple.
    """
    pass


# -------------------------------------------------------------------
# Comparison functions
# -------------------------------------------------------------------

class max2(ArithmeticFunction[_T]):
    """Returns the maximum of two numbers.

    ClickHouse:
        max2(x, y) returns the larger of x and y.
    """
    pass


class min2(ArithmeticFunction[_T]):
    """Returns the minimum of two numbers.

    ClickHouse:
        min2(x, y) returns the smaller of x and y.
    """
    pass


# -------------------------------------------------------------------
# Decimal arithmetic functions
# -------------------------------------------------------------------

class multiplyDecimal(ArithmeticFunction[_T]):
    """Returns the product of two numbers with decimal arithmetic.

    ClickHouse:
        multiplyDecimal(x, y) returns the product preserving the decimal precision.
    """
    pass


class divideDecimal(ArithmeticFunction[_T]):
    """Returns the quotient of two numbers with decimal arithmetic.

    ClickHouse:
        divideDecimal(x, y) returns the division result preserving the decimal precision.
    """
    pass


# -------------------------------------------------------------------
# Byte operations
# -------------------------------------------------------------------

class byteSwap(ArithmeticFunction[_T]):
    """Returns the value with its byte order reversed.

    ClickHouse:
        byteSwap(x) swaps the byte order of the integer value.
    """
    pass
