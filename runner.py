from glob import glob
from sys import stderr

while True:
    programs = {}
    n = 1

    # Print and save list of programs
    print('Programs:')
    for f in glob('*.py'):
        if f != 'runner.py':
            programs[n] = f
            print('%d. %s' % (n, f.replace('.py', '').replace('_', ' ').capitalize()))
            n += 1
    print('%d. %s' % (n, 'Exit'))

    # Read which program to run
    program = int(raw_input('Enter program number: '))
    print('')

    # Exit
    if program == n:
        break

    # Verify a valid program was selected
    if program not in range(1, n):
        stderr.write('Invalid selection')
        exit()

    # Run the program
    execfile(programs[program])

    # Separate executions
    print('')
