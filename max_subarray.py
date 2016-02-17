from math import floor


def max_sub_array(arr, low, high):
    if high == low:
        return low, high, arr[low]
    else:
        mid = int(floor((low + high) / 2))
        left_low, left_high, left_sum = max_sub_array(arr, low, mid)
        right_low, right_high, right_sum = max_sub_array(arr, mid + 1, high)
        cross_low, cross_high, cross_sum = max_crossing_sub_array(arr, low, mid, high)

        if left_sum >= right_sum and left_sum >= cross_sum:
            return left_low, left_high, left_sum
        elif right_sum >= left_sum and right_sum >= cross_sum:
            return right_low, right_high, right_sum
        else:
            return cross_low, cross_high, cross_sum


def max_crossing_sub_array(A, low, mid, high):
    left_sum = -99999999999999999999
    tmp_sum = 0
    max_left = -1
    for i in range(mid, low, -1):
        tmp_sum += A[i]
        if tmp_sum > left_sum:
            left_sum = tmp_sum
            max_left = i

    right_sum = -99999999999999999999
    tmp_sum = 0
    max_right = -1
    for j in range(mid + 1, high + 1):
        tmp_sum += A[j]
        if tmp_sum > right_sum:
            right_sum = tmp_sum
            max_right = j

    return max_left, max_right, left_sum + right_sum

a = [3, 8, 2, -1, -3, 0, 28, -5, -10, 2]
l, h, s = max_sub_array(a, 0, len(a) - 1)

print("Low: %d" % l)
print("High: %d" % h)
print("Sum: %d" % s)
