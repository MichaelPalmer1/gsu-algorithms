"""
Michael Palmer (900757121)
CSCI 5330 A
February 29, 2016

Maximum Subarray Problem
"""
from math import floor

DATA_DIR = 'data/'


def max_subarray(arr, low, high):
    """
    Find the maximum subarray
    :param arr List of integers to search through
    :param low Lower index
    :param high Upper index
    :returns Tuple containing the lower index, upper index, and sum of the maximum sub array
    """
    if high == low:
        return low, high, arr[low]
    else:
        mid = int(floor((low + high) / 2))
        left_low, left_high, left_sum = max_subarray(arr, low, mid)
        right_low, right_high, right_sum = max_subarray(arr, mid + 1, high)
        cross_low, cross_high, cross_sum = max_crossing_subarray(arr, low, mid, high)

        if left_sum >= right_sum and left_sum >= cross_sum:
            return left_low, left_high, left_sum
        elif right_sum >= left_sum and right_sum >= cross_sum:
            return right_low, right_high, right_sum
        else:
            return cross_low, cross_high, cross_sum


def max_crossing_subarray(arr, low, mid, high):
    """
    Find the maximum crossing subarray
    :param arr List of integers to search through
    :param low Lower index
    :param mid Middle index
    :param high Upper index
    :returns Tuple containing the maximum sum in the left, middle, and right sections
    """
    left_sum = float('-inf')
    tmp_sum = 0
    max_left = -1
    for i in range(mid, low - 1, -1):
        tmp_sum += arr[i]
        if tmp_sum > left_sum:
            left_sum = tmp_sum
            max_left = i

    right_sum = float('-inf')
    tmp_sum = 0
    max_right = -1
    for j in range(mid + 1, high + 1):
        tmp_sum += arr[j]
        if tmp_sum > right_sum:
            right_sum = tmp_sum
            max_right = j

    return max_left, max_right, left_sum + right_sum


def main():
    while True:
        # Get filename
        filename = raw_input('Enter filename: %s' % DATA_DIR)

        # Exit the loop
        if filename == 'exit':
            break

        try:
            # Read file contents into list
            with open(DATA_DIR + filename, 'r') as f:
                values = [int(line.strip().rstrip(',')) for line in f]

            # Print header
            print('\nCSCI 5330 Spring 2016')
            print('Michael Palmer')
            print('900757121')
            print('Running data for file %s' % filename)

            # Find the maximum subarray
            low, high, max_sum = max_subarray(values, 0, len(values) - 1)

            # Print the results
            print('Low = %d' % low)
            print('High = %d' % high)
            print('Sum = %d' % max_sum)

            # Print exit message
            print('\nTo quit, type "exit"')
        except IOError as e:
            print('File "%s" does not exist' % e.filename)

main()
