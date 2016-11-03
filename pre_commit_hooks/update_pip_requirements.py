from __future__ import print_function, with_statement
from subprocess import check_output, CalledProcessError
import sys
import re

def update_pip_requirements(argv=None):
    return_value = 1

    try:
        output = check_output(["pip3", "freeze"])

        # check that all lines matches to the pip requirements pattern
        pip_requirements_regexp = re.compile('([^\s^=]*==[^\s^=]*)|(-e [^\s]*)|([\s]*)')

        cleaned_requirements = ""
        non_matching_rows = ""

        for line in output.decode('utf-8').split('\n'):
            match = pip_requirements_regexp.match(line)
            if match and match.end() == len(line):
                cleaned_requirements += line + '\n'
            else:
                non_matching_rows += line + '\n'

        try:
            with open('requirements.txt', 'w') as file:
                file.write(cleaned_requirements)

            if non_matching_rows.strip() != "":
                print("The following lines have been excluded from the 'requirements.txt' file.")
                print("If they should be included open an issue on github.com/valentinarho/pre-commit-hooks project.")
                print("")
                print(non_matching_rows)

            return_value = 0

        except IOError:
            print("The 'requirements.txt' file cannot be written. Check the folder and file permissions.")
            return_value = 1

    except CalledProcessError:
        print("The 'pip freeze' command exited with errors. The 'requirements.txt' file cannot be updated.")
        return_value = 1

    return return_value

if __name__ == '__main__':
    sys.exit(update_pip_requirements())
