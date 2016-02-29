"""
Michael Palmer (900757121)
CSCI 5330 A
February 29, 2016

Maximum Subarray Problem
-------------------------
Within an array A, find a contiguous subarray such that the sum of
its elements is greater than that of any other contiguous subarray.
Output the starting and ending indices and the sum of this subarray.
"""
from math import floor

# Directory containing the test files
DATA_DIR = 'data/'


def max_subarray(a, low, high):
    """
    Find the maximum contiguous subarray in the array a
    :param a List of integers to search through
    :param low Lower index
    :param high Upper index
    :returns Tuple containing the lower index, upper index, and sum of the maximum sub array
    """
    if high == low:
        return low, high, a[low]
    else:
        mid = int(floor((low + high) / 2))
        left_low, left_high, left_sum = max_subarray(a, low, mid)
        right_low, right_high, right_sum = max_subarray(a, mid + 1, high)
        cross_low, cross_high, cross_sum = max_crossing_subarray(a, low, mid, high)

        if left_sum >= right_sum and left_sum >= cross_sum:
            return left_low, left_high, left_sum
        elif right_sum >= left_sum and right_sum >= cross_sum:
            return right_low, right_high, right_sum
        else:
            return cross_low, cross_high, cross_sum


def max_crossing_subarray(a, low, mid, high):
    """
    Find the maximum crossing subarray
    :param a List of integers to search through
    :param low Lower index
    :param mid Middle index
    :param high Upper index
    :returns Tuple containing the maximum sum in the left, middle, and right sections
    """
    left_sum = float('-inf')
    tmp_sum = 0
    max_left = -1
    for i in range(mid, low - 1, -1):
        tmp_sum += a[i]
        if tmp_sum > left_sum:
            left_sum = tmp_sum
            max_left = i

    right_sum = float('-inf')
    tmp_sum = 0
    max_right = -1
    for j in range(mid + 1, high + 1):
        tmp_sum += a[j]
        if tmp_sum > right_sum:
            right_sum = tmp_sum
            max_right = j

    return max_left, max_right, left_sum + right_sum


def main():
    # Get filename
    filename = raw_input('Enter filename: %s' % DATA_DIR)

    try:
        # Read file contents into list
        with open(DATA_DIR + filename, 'r') as f:
            values = [int(line.strip().rstrip(',')) for line in f]

        # Print header
        print('\nCSCI 5330 Spring 2016')
        print('Michael Palmer')
        print('900757121\n')
        print('Running data for file %s' % filename)

        # Find the maximum subarray
        low, high, max_sum = max_subarray(values, 0, len(values) - 1)

        # Print the results
        print('Low = %d' % low)
        print('High = %d' % high)
        print('Max = %d' % max_sum)
    except IOError as e:
        print('File "%s" does not exist' % e.filename)

main()
