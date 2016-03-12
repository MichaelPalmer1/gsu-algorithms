# coding=utf-8
"""
Michael Palmer (900757121)
CSCI 5330 A
March 23, 2016

Master Theorem
-------------------------

T(n) = aT(n/b) + Θ(n^k * log^i (n))

"""
import math


def master_method(a, b, k, i):
    """
    Perform master method calculations
    T(n) = aT(n/b) + Θ(n^k * log^i (n))
    :param a:
    :param b:
    :param k:
    :param i:
    :return: Output printed to console
    """
    # Validate input
    if a <= 0:
        raise Exception('a must be > 0')
    if b <= 1:
        raise Exception('b must be > 1')
    if k < 0:
        raise Exception('k must be >= 0')
    if i < 0:
        raise Exception('i must be >= 0')

    # Calculate log base b of a
    c = math.log(a, b)
    if c > k:       # Case 1
        case = 1
        output = format_output(c, 0)
    elif c == k:    # Case 2
        case = 2
        output = format_output(k, i + 1)
    else:           # Case 3
        case = 3
        output = 'F(n)'

    # Print the problem
    print('T(n) = %sT(n/%d) + ϴ(%s)' % ('' if a == 1 else a, b, format_output(k, i)))

    # Identify the case
    print('This is case %d' % case)

    # Print the solution
    print('T(n) = ϴ(%s)\n' % output)


def format_exponents(x):
    """
    Format the provided sequence of numbers as a superscript
    :param x: Integer|Float: Numbers to format
    :return: String: Input formatted as a superscript
    """
    output = ''
    exponents = ['⁰', '¹', '²', '³', '⁴', '⁵', '⁶', '⁷', '⁸', '⁹']
    x_str = str(x)
    if '.' not in x_str:
        # Go through the string and convert each number to its superscript equivalent
        for i in range(len(x_str)):
            index = int(x_str[i])
            output += exponents[index]
    else:
        # Exponents with decimals don't look nice, so resorting to the ugly format
        output += '^%0.2f' % x
    return output


def format_output(k, i):
    """
    Format the output
    :param k:
    :param i:
    :return: String of the formatted output
    """
    if k == 0:
        output = '1' if i == 0 else ''
    elif k == 0.5:
        output = '√n'
    elif k == 1:
        output = 'n'
    else:
        output = 'n%s' % format_exponents(k)

    if i != 0:
        output += ' log' if output != '' else 'log'
        if i != 1:
            output += format_exponents(i)
        output += ' n'

    return output

master_method(4, 16, 0, 0)
master_method(4, 2, 2, 0)
master_method(95, 95, 2, 1)
