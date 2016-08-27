# coding=utf-8
# Specifying the encoding so that we can use some symbols (i.e. theta, superscripts, etc.)
"""
Michael Palmer
CSCI 5330 A
March 23, 2016

Master Theorem

The formula for the master theorem is as follows: T(n) = aT(n/b) + Θ(n^k * log^i (n)). The purpose of the master
theorem is to calculate the complexity of a divide and conquer expression that is divided into a sub-problems,
with each sub-problem being of size n/b. n represents the size of the entire problem and f(n) represents the cost
outside of the recursive call, such as the cost of merging the sub-problems back together. The end goal is to determine
an asymptotically tight bound for the problem.

"""
import re
from math import log

# Console output formatting
BLUE = '\033[94m'
GREEN = '\033[92m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
END = '\033[0m'

# Define the test cases
cases = [
    # Case 1
    [
        '2T(n/2) + 15',             # Example 1
        '8T(n/2) + n^2 log^2 n'     # Example 2
    ],

    # Case 2
    [
        '9T(n/9) + n log n',        # Example 1
        '2T(n/4) + √n'              # Example 2
    ],

    # Case 3
    [
        'T(n/2) + 5n',              # Example 1
        '4T(n/2) + n^3'             # Example 2
    ]
]


def master_method(a, b, k, i):
    """
    Perform master method calculation and print the results

    :param a: Number of problems (a > 0)
    :param b: Size of the sub-problems (b > 1)
    :param k: Exponent of n (k >= 0)
    :param i: Exponent of the log (i >= 0)
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

    # Format the problem and print it out
    print('T(n) = %sT(n/%d) + ϴ(%s)' % ('' if a == 1 else a, b, format_output(k, i)))

    # Print problem parts
    print('a = %s, b = %s, k = %s, i = %s' % (a, b, k, i))
    fn = format_output(k, i)

    # Calculate log base b of a and print the calculation
    c = log(a, b)
    tn = format_output(c, 0)
    # Using subscript beta here since subscript b does not seem to exist anywhere and beta looks similar to a b
    print('c = logᵦa = log%s%d = %.2f' % (format_numbers(b, False), a, c))
    print('T(n) ∈ ϴ(%s), F(n) ∈ ϴ(%s)' % (tn, fn))

    # Determine the case, format the output, and print the comparison
    if c > k:       # Case 1
        output = format_output(c, 0)
        print('Case 1 because T(n) > F(n) (since c > k)')
    elif c == k:    # Case 2
        output = format_output(c, i + 1)
        print('Case 2 because T(n) ~= F(n) (since c == k)')
    else:           # Case 3
        output = 'F(n)'
        print('Case 3 because T(n) < F(n) (since c < k)')

    # Print the solution (formatted so it stands out)
    print((BOLD + GREEN + 'T(n) = ϴ(%s)\n' + END) % output)


def format_numbers(x, super_script=True):
    """
    Format a series of numbers as a superscript or subscript

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
        # Decimals don't look good, so falling back to the default format
        output += '^%0.2f' % x
    return output


def format_output(k, i):
    """
    Format the expression output based on the values of k and i

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

    if i > 0:          # Logarithm
        output += ' log' if output != '' else 'log'

        # Append the exponent if needed
        output += format_numbers(i) if i > 1 else ''

        # Finally, append the n
        output += ' n'

    return output


def process_input(string):
    """
    Process input expression string to a, b, k, i variables

    :param string: Expression to evaluate
    :return: (a, b, k, i)
    :rtype: tuple
    """
    a, b, k, i = 0, 0, 0, 0

    # Compile the regular expression
    p = re.compile(
        '(?P<a>\d*)T\(n/(?P<b>\d+)\)(?: \+ (?:(?P<n>√n|sqrt\(n\)|\d*n?\^?(?P<k>\d*)) ?(?P<log>log\^?(?P<i>\d*))? ?n?))?'
        , re.IGNORECASE
    )

    # Check for matches
    matches = p.match(string)
    if not matches:
        raise Exception('No matching expression')

    # Convert groups to a dict
    groups = matches.groupdict()

    # If a is not provided, fall back to 1
    a = int(groups['a']) if groups['a'] else 1
    b = int(groups['b'])

    # Check if there is a F(n) in the expression
    if groups['n'] or groups['log']:
        # Check if n^k was specified
        nk = groups['n']
        if nk:
            # Convert to lowercase, just to be safe
            nk = nk.lower()
            if '√' in nk or 'sqrt' in nk:
                # Found a square root
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

    # Return the values
    return a, b, k, i


def main():
    """
    Run the program using the pre-defined test cases
    """
    # Print header
    print('CSCI 5330 Spring 2016')
    print('Michael Palmer')

    # Loop through the test cases
    for case_num, case in enumerate(cases):
        for example, item in enumerate(case):
            # Print case and example numbers (formatted so it stands out)
            print((UNDERLINE + BLUE + BOLD + "Case %d Example %d" + END) % (case_num + 1, example + 1))

            # Print the expression exactly as it was entered
            print('T(n) = %s' % item)

            # Process the expression
            a, b, k, i = process_input(item)

            # Perform the master method
            master_method(a, b, k, i)


def test():
    """
    Run in test mode
    """
    print('Enter expression in the format: aT(n/b) + n^k log^i n')
    while True:
        s = raw_input('T(n) = ')
        a, b, k, i = process_input(s)
        master_method(a, b, k, i)
        if raw_input('Run again? [y/n] ').lower() == 'n':
            break

if __name__ == '__main__':
    print('Run Modes:')
    print('1. Normal (pre-defined test cases)')
    print('2. Test (manual input)')
    run_mode = raw_input('Select run mode: ')
    if run_mode == '1':
        print('')
        main()
    elif run_mode == '2':
        print('')
        test()
    else:
        raise Exception('Invalid run mode')
