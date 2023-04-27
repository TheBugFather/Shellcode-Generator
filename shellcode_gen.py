""" Built-in modules """
import os
import re
import shlex
import sys
from pathlib import Path
from subprocess import Popen, TimeoutExpired


def objdump_run(filename: str, tmp_file: Path):
    """
    Takes the passed in binary executable, runs objdump utility, and writes the output to file.

    :param filename:  The file to be run through the objdump utility.
    :param tmp_file:  The temp file where the objdump output will be saved to.
    :return:  Nothing
    """
    # Shell escape filename for execution #
    file = shlex.quote(filename)

    try:
        # Open the temp file in write mode #
        with tmp_file.open('w', encoding='utf-8') as out_file:
            # Create objdump command process, storing output in open file #
            with Popen(['objdump', '-M', 'intel', '-D', file], stdout=out_file,
                       stderr=out_file) as command:
                try:
                    command.communicate()

                # When process completes or is timed out #
                except (TimeoutExpired, ValueError):
                    command.kill()
                    command.communicate()

    # If error occurs during file operation #
    except OSError as io_err:
        print_err(f'Error occurred writing {file} objdump to {tmp_file}: {io_err}')
        sys.exit(2)


def print_err(msg: str):
    """
    Prints a timed error message via stderr.

    :param msg:  The error message to be displayed.
    :return:  Nothing
    """
    print(f'\n* [ERROR]: {msg} *\n', file=sys.stderr)


def prompt_user(re_exe) -> str:
    """
    Prompt the user for input, handle errors accordingly.

    :param re_exe:  The regular expression match format.
    :return:  Validated user input.
    """
    cmd = shlex.quote('clear')

    while True:
        # Clear the display #
        os.system(cmd)
        # Prompt user for input #
        prompt = input('[+] Invalid or no args provided .. enter file to grab bytes: ')

        # If input validation regex fails #
        if not re.search(re_exe, prompt):
            print_err('Improper input .. try again')
            continue

        return prompt


def main():
    """
    Take input file, run in objdump, and parse output into shellcode.

    :return:  Nothing
    """
    # Compile path regex #
    re_exe = re.compile(r'[a-zA-Z\d_\"\' .,\-]{1,20}')

    # If an arg was passed in #
    if len(sys.argv) > 1:
        # Check if arg was passed in #
        arg_check = re.search(re_exe, sys.argv[1])

        # If regex did not match #
        if not arg_check:
            # Prompt the user for input #
            filename = prompt_user(re_exe)
        else:
            # Set the passed in arg as filename #
            filename = sys.argv[1]
    # If no args were passed in #
    elif len(sys.argv) == 1:
        # Prompt the user for binary tp execute on #
        filename = prompt_user(re_exe)
    # If unexpected error occurs parsing args #
    else:
        print_err('Unknown error occurred on program startup')
        # Exit program on error #
        sys.exit(1)

    out_path = Path('/tmp')
    # Set temp file name for pre-parsing #
    tmp_file = out_path / f'{filename}.txt'

    # Run objdump utility on binary file and save to tmp file #
    objdump_run(filename, tmp_file)

    # Compile regular expression for byte formatting #
    re_byte = re.compile(r'\s([a-f\d]{2}\s){1,7}')
    re_space_strip = re.compile(r'\s[^\S\r\n]')
    re_raw_byte = re.compile(r'\s|\t')
    shellcode = ''

    try:
        # Open the temporary file in read mode #
        with tmp_file.open('r', encoding='utf-8') as re_file:
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

        print(f'Shellcode: {shellcode}')

    # If error occurs during file operation #
    except OSError as io_err:
        print_err(f'Error occurred writing shellcode to {tmp_file.name}: {io_err}')
        sys.exit(3)

    # Unlink the temporary parsing file #
    tmp_file.unlink()

    sys.exit(0)


if __name__ == '__main__':
    main()
