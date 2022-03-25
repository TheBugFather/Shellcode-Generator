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
Name:       PromptUser
Purpose:    Prompt the user for input, handle errors accordingly.
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

    # Run objdump utility with on selected object file, write result to file #
    with open('/tmp/' + filename + '.txt', 'a') as out_file:
        try:
            command = subprocess.Popen(['objdump', '-M', 'intel', '-D', file], stdout=out_file,
                                       stderr=out_file, shell=False)
            command.communicate()
        except (subprocess.CompletedProcess, subprocess.TimeoutExpired, OSError, ValueError):
            command.kill()
            command.communicate()

    re_byte = re.compile(r'\s([0-9a-f]{2}\s){1,7}')
    re_space_strip = re.compile(r'\s[^\S\r\n]')
    re_raw_byte = re.compile(r'(?:\s|\t)')
    shellcode = ''

    # Iterate through file line by line, grab needed bytes,
    # and  format bytes to raw \xXX format # 
    with open('/tmp/' + filename + '.txt', 'r') as re_file:
        for line in re_file:
            byte_grab = re.search(re_byte, line)
            if byte_grab:
                strip = re.sub(re_space_strip, r'', byte_grab.group(0))
                raw_byte = re.sub(re_raw_byte, r'\\x', strip)
                shellcode += raw_byte[:-2]

    print('Shellcode: {}'.format(shellcode))
    os.remove('/tmp/' + filename + '.txt')


if __name__ == '__main__':
    main()
