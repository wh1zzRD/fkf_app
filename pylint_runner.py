import subprocess
import re
import os

# Run pylint and save the output to a file
with open('pylint.txt', 'w') as pylint_file:
    process = subprocess.run(['pylint', 'controller', 'model', 'view'], stdout=subprocess.PIPE, text=True)
    pylint_file.write(process.stdout)

# Read the pylint output
with open('pylint.txt', 'r') as pylint_file:
    pylint_output = pylint_file.read()

# Extract the pylint score
match = re.search(r'Your code has been rated at ([\-0-9\.]+)/', pylint_output)
score = float(match.group(1)) if match else 0.0
score_minimal = 8.0

# Print the pylint output
print(pylint_output)

# Remove the pylint.txt file

os.remove('pylint.txt')

# Check the pylint score
if score > score_minimal:
    print("Pylint succeeded")
    exit(0)
else:
    print("Pylint failed")
    exit(1)
