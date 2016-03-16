# coding=utf-8
"""
Michael Palmer (900757121)
CSCI 5330 A
March 23, 2016

Master Theorem
-------------------------

T(n) = aT(n/b) + Θ(n^k * log^i (n))

"""
import re
from math import log


def master_method(a, b, k, i):
    """
    Perform master method calculations
    Formula: T(n) = aT(n/b) + Θ(n^k * log^i (n))

    :param a: Number of problems
    :param b: Size of the sub-problems
    :param k: Exponent of n
    :param i: Exponent of the log
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
    c = log(a, b)
    print('log%s%d = %.2f' % (format_numbers(b, False), a, c))

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


def format_numbers(x, super_script=True):
    """
    Format a set of numbers as a superscript or subscript
    :param x: Numbers to format
    :param super_script: Superscript (True) or subscript (False)
    :return: Numbers as superscript/subscript
    :rtype: str
    """
    output = ''
    superscript = ['⁰', '¹', '²', '³', '⁴', '⁵', '⁶', '⁷', '⁸', '⁹']
    subscript = ['₀', '₁', '₂', '₃', '₄', '₅', '₆', '₇', '₈', '₉']
    numbers = superscript if super_script else subscript

    # Remove decimal places if possible
    if int(x) == x:
        x = int(x)

    # Convert to string
    x_str = str(x)

    # Check for decimals
    if '.' not in x_str:
        # Convert each number to a superscript/subscript
        for s in x_str:
            output += numbers[int(s)]
    else:
        # Decimals don't play nice, so using the default format if one exists
        output += '^%0.2f' % x
    return output


def format_output(k, i):
    """
    Format the output
    :param k: Exponent of n
    :param i: Exponent of the log
    :return: String of the formatted output
    :rtype: str
    """
    if k == 0:          # Constant
        output = '1' if i == 0 else ''
    elif k == 0.5:      # Square Root
        output = '√n'
    elif k == 1:        # Linear
        output = 'n'
    else:               # Exponent
        output = 'n%s' % format_numbers(k)

    if i != 0:          # Logarithm
        output += ' log' if output != '' else 'log'

        # Add the exponent
        output += format_numbers(i) if i != 1 else ''

        # Add the n
        output += ' n'

    return output


def process_input(string):
    """
    Process input string to a, b, k, i variables
    :param string: Expression to evaluate
    :return: (a, b, k, i)
    :rtype: tuple
    """
    a, b, k, i = 0, 0, 0, 0
    # Grab the relevant parts of the expression
    p = re.compile(
        '(?P<a>\d*)T\(n/(?P<b>\d+)\)(?: \+ (?:(?P<n>√n|sqrt\(n\)|\d*n?\^?(?P<k>\d*)) ?(?P<log>log\^?(?P<i>\d*))? ?n?))?'
        , re.IGNORECASE
    )
    matches = p.match(string)
    if not matches:
        raise Exception('No matching expression')

    groups = matches.groupdict()
    a = int(groups['a']) if groups['a'] else 1
    b = int(groups['b'])

    # Check if there is a F(n)
    if groups['n'] or groups['log']:
        # Check if n^k was specified
        nk = groups['n']
        if nk:
            nk = nk.lower()
            if '√' in nk or 'sqrt' in nk:
                # Square root
                k = 0.5
            elif '^' in nk:
                # n^k has an exponent
                k = int(groups['k'])
            elif 'n' in nk:
                # Just n
                k = 1

        # Check if log^i n was specified
        log_i = groups['log']
        if log_i:
            if '^' in log_i:
                # log^i n has an exponent
                i = int(groups['i'])
            else:
                # Just log n
                i = 1

    return a, b, k, i


def main():
    """
    Run the program
    """
    # Print header
    print('CSCI 5330 Spring 2016')
    print('Michael Palmer')
    print('900757121\n')

    # Define the test cases
    cases = [
        # Case 1
        [
            '2T(n/2) + 15',
            '8T(n/2) + n^2 log^2 n'
        ],

        # Case 2
        [
            '9T(n/9) + n log n',
            '2T(n/4) + √n'
        ],

        # Case 3
        [
            'T(n/2) + 5n',
            '4T(n/2) + n^3'
        ]
    ]

    # Loop through the test cases
    for case_num, case in enumerate(cases):
        for example, item in enumerate(case):
            print("Case %d Example %d" % (case_num + 1, example + 1))
            print('T(n) = %s' % item)
            a, b, k, i = process_input(item)
            master_method(a, b, k, i)


def test():
    """
    Run in test mode
    """
    print('Type \'q\' to exit execution')
    print('Enter expression in the format: aT(n/b) + n^k log^i n')
    while True:
        s = raw_input('T(n) = ')
        if s == 'q':
            break
        a, b, k, i = process_input(s)
        master_method(a, b, k, i)

if __name__ == '__main__':
    main()
    # test()
