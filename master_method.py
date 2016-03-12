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
    :param a: Number of problems
    :param b: Size of the sub-problems
    :param k: Exponent of n
    :param i: Exponent of the log
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

    # Print the problem
    print('T(n) = %sT(n/%d) + ϴ(%s)' % ('' if a == 1 else a, b, format_output(k, i)))

    # Calculate log base b of a
    c = math.log(a, b)
    print('log%s%d = %.2f' % (format_subscript(b), a, c))

    # Determine the case
    if c > k:       # Case 1
        case = 1
        output = format_output(c, 0)
    elif c == k:    # Case 2
        case = 2
        output = format_output(k, i + 1)
    else:           # Case 3
        case = 3
        output = 'F(n)'

    # Identify the case
    print('This is case %d' % case)

    # Print the solution
    print('T(n) = ϴ(%s)\n' % output)


def format_superscript(x):
    """
    Format the provided sequence of numbers as a superscript
    :param x: Integer|Float: Numbers to format
    :return: String: Input formatted as a superscript
    """
    output = ''
    numbers = ['⁰', '¹', '²', '³', '⁴', '⁵', '⁶', '⁷', '⁸', '⁹']
    if int(x) == x:
        x = int(x)
    x_str = str(x)
    if '.' not in x_str:
        # Go through the string and convert each number to its superscript equivalent
        for i in range(len(x_str)):
            index = int(x_str[i])
            output += numbers[index]
    else:
        # Exponents with decimals don't look nice, so resorting to the ugly format
        output += '^%0.2f' % x
    return output


def format_subscript(x):
    """
    Format the provided sequence of numbers as a subscript
    :param x: Integer|Float: Numbers to format
    :return: String: Input formatted as a subscript
    """
    output = ''
    numbers = ['₀', '₁', '₂', '₃', '₄', '₅', '₆', '₇', '₈', '₉']
    if int(x) == x:
        x = int(x)
    x_str = str(x)
    if '.' not in x_str:
        for i in range(len(x_str)):
            index = int(x_str[i])
            output += numbers[index]
    else:
        output += '_%.2f' % x
    return output


def format_output(k, i):
    """
    Format the output
    :param k: Exponent of n
    :param i: Exponent of the log
    :return: String of the formatted output
    """
    if k == 0:
        output = '1' if i == 0 else ''
    elif k == 0.5:
        output = '√n'
    elif k == 1:
        output = 'n'
    else:
        output = 'n%s' % format_superscript(k)

    if i != 0:
        output += ' log' if output != '' else 'log'
        if i != 1:
            output += format_superscript(i)
        output += ' n'

    return output


def main():
    print('CSCI 5330 Spring 2016')
    print('Michael Palmer')
    print('900757121\n')

    cases = [
        # Case 1
        [
            (4, 16, 0, 0),
            (8, 2, 2, 2)
        ],

        # Case 2
        [
            (9, 9, 1, 1),
            (2, 4, 0.5, 0)
        ],

        # Case 3
        [
            (1, 2, 1, 0),
            (4, 2, 4, 1)
        ],
    ]

    for case_num, case in enumerate(cases):
        for example, item in enumerate(case):
            print("Case %d Example %d" % (case_num + 1, example + 1))
            master_method(item[0], item[1], item[2], item[3])

if __name__ == '__main__':
    main()
