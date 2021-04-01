#!/usr/bin/python3
import re, sys, os, subprocess
from time import sleep

# Handling user input #
def prompt_user(re_exe):
    while True:
        os.system('clear')
        prompt = input('invalid or no args provided .. enter file to grab bytes\n')
        if re.search(re_exe, prompt) == None:
            print('\n* Improper input .. try again *')
            sleep(2)
            continue

        return prompt

def main():
    re_exe = re.compile(r'[a-zA-Z0-9_"\' \.,\-]{1,20}')

    # If an arg was passed in #
    if len(sys.argv) > 1:
        arg_check = re.search(re_exe, sys.argv[1])
        if arg_check == None:
            filename = prompt_user(re_exe)
        else:
            filename = sys.argv[1]
    # If no args were passed in #
    elif len(sys.argv) == 1:
        filename = prompt_user(re_exe)

    # Run objdump utility with on selected object file, write result to file #
    with open('/tmp/' + filename + '.txt', 'a') as out_file:
        try:
            command = subprocess.Popen(['objdump', '-M', 'intel', 
					'-D', '{}'.format(filename)], 
					stdout=out_file, stderr=out_file,
					shell=False)
            outs, errs = command.communicate(5)
        except (subprocess.CompletedProcess, subprocess.TimeoutExpired, OSError, ValueError):
            command.kill()
            outs, errs = command.communicate()

    re_byte = re.compile(r'\s([0-9a-f]{2}\s){1,7}')
    re_spaceStrip = re.compile(r'\s[^\S\r\n]')
    re_rawByte = re.compile(r'(?:\\t|\s)')
    shellcode = ''

    # Iterate through file line by line, grab needed bytes,
    # and  format bytes to raw \xXX format # 
    with open('/tmp/' + filename + '.txt', 'r') as re_file:
        for line in re_file:
            byte_grab = re.search(re_byte, line)
            if byte_grab == None:
                pass
            else: 
                strip = re.sub(re_spaceStrip, r'', byte_grab.group(0))
                rawByte = re.sub(re_rawByte, r'\\x', strip)
                shellcode += rawByte[:-2]

    print('Shellcode: {}'.format(shellcode))
    os.remove('/tmp/' + filename + '.txt')

if __name__ == '__main__':
    main()