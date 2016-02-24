from glob import glob
from sys import stderr

programs = {}
n = 1

# Print and save list of programs
print('Programs:')
for f in glob('*.py'):
    if f != 'runner.py':
        programs[n] = f
        print('%d. %s' % (n, f))
        n += 1

# Read which program to run
program = int(raw_input('Enter program number: '))
print('')

# Verify a valid program was selected
if program not in range(1, n):
    stderr.write('Invalid selection')
    exit()

# Run the program
execfile(programs[program])
