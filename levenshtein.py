from time import time


def levenshtein_distance(s, t):
    # Base cases
    if s == t:
        return 0
    if len(s) == 0:
        return len(t)
    if len(t) == 0:
        return len(s)

    # Work vectors
    v0, v1 = [i for i in range(len(t) + 1)], [0 for _ in range(len(t) + 1)]

    for i in range(len(s)):
        # calculate v1 (current row distances) from the previous row v0
        # first element of v1 is A[i+1][0]
        # edit distance is delete (i+1) chars from s to match empty t
        v1[0] = i + 1

        # use formula to fill in the rest of the row
        for j in range(len(t)):
            cost = 0
            if s[i] != t[j]:
                cost = 1
            v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)

        # copy v1 (current row) to v0 (previous row) for next iteration
        for j in range(len(v0)):
            v0[j] = v1[j]

    return v1[len(t)]

while True:
    # Get input
    s1 = raw_input('Enter string 1: ')
    s2 = raw_input('Enter string 2: ')

    # Separator
    print('-' * 30)

    # Save start time
    start = time()

    # Output results
    print('Distance: %d' % levenshtein_distance(s1, s2))
    print('Runtime: %f sec' % (time() - start))

    # Separator
    print('-' * 30)

    # Run again?
    if raw_input('Run again? [y/n]: ') != 'y':
        break

    # Add test case separator
    print('')
    print('#' * 50)
    print('')
