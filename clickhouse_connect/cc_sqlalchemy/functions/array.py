from typing import List, TypeVar, Any, Optional, Union

from sqlalchemy.sql.functions import ReturnTypeFromArgs

_T = TypeVar("_T", bound=Any)
Number = Union[int, float]


# Base class for all array functions.
class ArrayFunction(ReturnTypeFromArgs[_T]):
    """Base class for ClickHouse array functions."""
    pass


# -------------------------------------------------------------------
# Boolean checks on arrays
# -------------------------------------------------------------------

class empty(ArrayFunction[int]):
    """Checks whether the input array is empty.

    Returns:
        UInt8 — 1 if the array is empty, 0 otherwise.
    """
    pass


class notEmpty(ArrayFunction[int]):
    """Checks whether the input array is non-empty.

    Returns:
        UInt8 — 1 if the array is non-empty, 0 otherwise.
    """
    pass


# -------------------------------------------------------------------
# Array size and length functions
# -------------------------------------------------------------------

class length(ArrayFunction[int]):
    """Returns the number of items in the array.

    Alias:
        OCTET_LENGTH
    """
    pass


# -------------------------------------------------------------------
# Functions returning empty arrays of specific types
# -------------------------------------------------------------------

class emptyArrayUInt8(ArrayFunction[List[int]]):
    """Returns an empty array of type UInt8."""
    pass


class emptyArrayUInt16(ArrayFunction[List[int]]):
    """Returns an empty array of type UInt16."""
    pass


class emptyArrayUInt32(ArrayFunction[List[int]]):
    """Returns an empty array of type UInt32."""
    pass


class emptyArrayUInt64(ArrayFunction[List[int]]):
    """Returns an empty array of type UInt64."""
    pass


class emptyArrayInt8(ArrayFunction[List[int]]):
    """Returns an empty array of type Int8."""
    pass


class emptyArrayInt16(ArrayFunction[List[int]]):
    """Returns an empty array of type Int16."""
    pass


class emptyArrayInt32(ArrayFunction[List[int]]):
    """Returns an empty array of type Int32."""
    pass


class emptyArrayInt64(ArrayFunction[List[int]]):
    """Returns an empty array of type Int64."""
    pass


class emptyArrayFloat32(ArrayFunction[List[float]]):
    """Returns an empty array of type Float32."""
    pass


class emptyArrayFloat64(ArrayFunction[List[float]]):
    """Returns an empty array of type Float64."""
    pass


class emptyArrayDate(ArrayFunction[List[Any]]):
    """Returns an empty array of type Date."""
    pass


class emptyArrayDateTime(ArrayFunction[List[Any]]):
    """Returns an empty array of type DateTime."""
    pass


class emptyArrayString(ArrayFunction[List[str]]):
    """Returns an empty array of type String."""
    pass


class emptyArrayToSingle(ArrayFunction[List[_T]]):
    """Accepts an empty array and returns a one-element array equal to the default value."""
    pass


# -------------------------------------------------------------------
# Array creation functions
# -------------------------------------------------------------------

class range(ArrayFunction[List[Number]]):
    """Returns an array of numbers from `start` to `end - 1` by `step`.

    Syntax:
        range(end)
        range(start, end)
        range(start, end, step)

    Note:
        All arguments must be of integer types.
    """
    pass


class array(ArrayFunction[List[_T]]):
    """Creates an array from the provided constant arguments.

    Note:
        At least one argument must be provided.
    """
    pass


class arrayWithConstant(ArrayFunction[List[_T]]):
    """Creates an array of given length filled with the constant element.

    Arguments:
        length: The desired length.
        elem: The constant element.
    """
    pass


class arrayConcat(ArrayFunction[List[_T]]):
    """Combines two or more arrays passed as arguments."""
    pass


# -------------------------------------------------------------------
# Array element access functions
# -------------------------------------------------------------------

class arrayElement(ArrayFunction[_T]):
    """Gets the element with the specified index (1-based) from the array.

    Note:
        Supports negative indexes (from the end) and returns a default value if out-of-bounds.
    """
    pass


class arrayElementOrNull(ArrayFunction[Optional[_T]]):
    """Gets the element with the specified index (1-based) from the array.

    Note:
        Returns NULL if the index is out-of-bounds.
    """
    pass


class has(ArrayFunction[int]):
    """Checks whether the array contains the specified element.

    Returns:
        UInt8 — 1 if present, 0 otherwise.
    """
    pass


# -------------------------------------------------------------------
# Array subset and intersection functions
# -------------------------------------------------------------------

class hasAll(ArrayFunction[int]):
    """Checks whether the first array contains all the elements of the second array.

    Returns:
        1 if the first array is a superset of the second, 0 otherwise.
    """
    pass


class hasAny(ArrayFunction[int]):
    """Checks whether the two arrays have at least one element in common.

    Returns:
        1 if there is an intersection, 0 otherwise.
    """
    pass


class hasSubstr(ArrayFunction[int]):
    """Checks whether all elements of the second array appear as a contiguous subsequence in the first array.

    Returns:
        1 if array2 is a substring of array1, 0 otherwise.
    """
    pass


# -------------------------------------------------------------------
# Array search functions
# -------------------------------------------------------------------

class indexOf(ArrayFunction[int]):
    """Returns the index (1-based) of the first occurrence of an element in the array.

    Returns:
        0 if the element is not found.
    """
    pass


class indexOfAssumeSorted(ArrayFunction[int]):
    """Returns the index (1-based) of an element in a sorted array using binary search.

    Note:
        Undefined results if the array is not sorted.
    """
    pass


# -------------------------------------------------------------------
# Array counting and dot product functions
# -------------------------------------------------------------------

class arrayCount(ArrayFunction[int]):
    """Counts the number of elements for which an optional function returns a non-zero value.

    Note:
        If no function is provided, counts the number of non-zero elements.
    """
    pass


class arrayDotProduct(ArrayFunction[Number]):
    """Returns the dot product of two arrays (or tuples) of numeric values.

    Aliases:
        scalarProduct, dotProduct
    """
    pass


class countEqual(ArrayFunction[int]):
    """Returns the number of elements in the array equal to the given value."""
    pass


# -------------------------------------------------------------------
# Array enumeration functions
# -------------------------------------------------------------------

class arrayEnumerate(ArrayFunction[List[int]]):
    """Returns an array [1, 2, 3, ..., length(arr)] corresponding to the element positions."""
    pass


class arrayEnumerateUniq(ArrayFunction[List[int]]):
    """For each element in the array, returns its position among elements with the same value."""
    pass


class arrayEnumerateUniqRanked(ArrayFunction[List[int]]):
    """For multidimensional arrays, returns an array indicating, for each element, its occurrence rank among similar values.

    Parameters:
        clear_depth: The level at which to enumerate separately.
        max_array_depth: The maximum depth considered.
    """
    pass


# -------------------------------------------------------------------
# Array modification functions
# -------------------------------------------------------------------

class arrayPopBack(ArrayFunction[List[_T]]):
    """Removes the last element from the array."""
    pass


class arrayPopFront(ArrayFunction[List[_T]]):
    """Removes the first element from the array."""
    pass


class arrayPushBack(ArrayFunction[List[_T]]):
    """Adds one element to the end of the array."""
    pass


class arrayPushFront(ArrayFunction[List[_T]]):
    """Adds one element to the beginning of the array."""
    pass


class arrayResize(ArrayFunction[List[_T]]):
    """Changes the length of the array.

    If the new size is larger, the array is extended using a provided extender value (or a default value).
    If smaller, the array is truncated.
    """
    pass


class arraySlice(ArrayFunction[List[_T]]):
    """Returns a slice of the array.

    Parameters:
        offset: Starting position (1-based; negative for offset from the end).
        length: Number of elements to include (if negative, returns an open slice).
    """
    pass


class arrayShingles(ArrayFunction[List[List[_T]]]):
    """Generates an array of consecutive sub-arrays ("shingles") of the specified length."""
    pass


# -------------------------------------------------------------------
# Array sorting function
# -------------------------------------------------------------------

class arraySort(ArrayFunction[List[_T]]):
    """Sorts the elements of the array in ascending order.

    Optionally accepts a lambda function to determine the sorting key.

    Note:
        This is a higher-order function; additional arrays can be passed to define multi-key sort.
    """
    pass
