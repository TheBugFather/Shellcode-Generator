# Built-in modules #
import os
import re
import shlex
import subprocess
import sys
from time import sleep


'''
########################################################################################################################
Name:       PromptUser
Purpose:    Prompt the user for input, handle errors accordingly.
Parameters: The regular expression match format.
Returns:    Validated user input.
########################################################################################################################
'''
def PromptUser(re_exe) -> str:
    while True:
        os.system(shlex.quote('clear'))
        prompt = input('invalid or no args provided .. enter file to grab bytes\n')
        if not re.search(re_exe, prompt):
            print('\n* Improper input .. try again *')
            sleep(2)
            continue

        return prompt


'''
########################################################################################################################
Name:       PrintErr
Purpose:    Prints a timed error message.
Parameters: The error message to be displayed and the time interval it should be displayed in seconds.
Returns:    None
########################################################################################################################
'''
def PrintErr(msg: str, seconds: int):
    print(f'\n* [ERROR]: {msg} *\n', file=sys.stderr)
    sleep(seconds)


'''
########################################################################################################################
Name:       main
Purpose:    Take input file, run in objdump, and parse output into shellcode.
Parameters: None
Returns:    None
########################################################################################################################
'''
def main():
    # Compile path regex #
    re_exe = re.compile(r'[a-zA-Z0-9_\"\' .,\-]{1,20}')

    # If an arg was passed in #
    if len(sys.argv) > 1:
        # Check if arg was passed in #
        arg_check = re.search(re_exe, sys.argv[1])

        # If regex did not match #
        if not arg_check:
            filename = PromptUser(re_exe)
        else:
            filename = sys.argv[1]
    # If no args were passed in #
    elif len(sys.argv) == 1:
        filename = PromptUser(re_exe)
    else:
        # Exit program on error #
        sys.exit(1)

    # Shell escape filename for execution #
    file = shlex.quote(filename)
    # Set temp file name for pre-parsing #
    tmp_file = f'/tmp/{filename}.txt'

    # Open the file in temporary write mode #
    with open(tmp_file, 'w') as out_file:
        # Create objdump command process, storing output in open file #
        command = subprocess.Popen(['objdump', '-M', 'intel', '-D', file], stdout=out_file,
                                   stderr=out_file, shell=False)
        try:
            command.communicate()
        except (subprocess.CompletedProcess, subprocess.TimeoutExpired, OSError, ValueError):
            command.kill()
            command.communicate()

    # Compile regular expression for byte formatting #
    re_byte = re.compile(r'\s([0-9a-f]{2}\s){1,7}')
    re_space_strip = re.compile(r'\s[^\S\r\n]')
    re_raw_byte = re.compile(r'(?:\s|\t)')
    shellcode = ''

    # If the file exists and has read access #
    if os.path.isfile(tmp_file) and os.access(tmp_file, os.R_OK):
        try:
            # Open the temporary file in read mode #
            with open(f'/tmp/{filename}.txt', 'r') as re_file:
                # Iterate through file line by line #
                for line in re_file:
                    # Attempt to match bytes in line #
                    byte_grab = re.search(re_byte, line)
                    # If regex matches #
                    if byte_grab:
                        # Strip whitespace from match #
                        strip = re.sub(re_space_strip, r'', byte_grab.group(0))
                        # Format raw byte like \xXX #
                        raw_byte = re.sub(re_raw_byte, r'\\x', strip)
                        # Append raw byte to shellcode string #
                        shellcode += raw_byte[:-2]

            print('Shellcode: {}'.format(shellcode))
            # Unlink the temporary parsing file #
            os.remove('/tmp/' + filename + '.txt')

        except (IOError, OSError) as err:
            PrintErr(err, 2)


if __name__ == '__main__':
    main()
