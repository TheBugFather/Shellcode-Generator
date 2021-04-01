## Prereqs
This program was designed for Python3 on Linux systems with objdump utility.
The modules use should be included in the Python3 default installation.

# Installation
python3 & objdump are directly installed with Linux apt package manager.

## Purpose
The purpose is to run objdump on selected file, grab bytes, & format as shellcode.
Ideally this program can be added to environment executables/path as a handy terminal utility.

## How it works
Example: python3 shellcodeGen.py exe_name
- If arg is not passed, the user is prompted for input
- Selected executable is run in objdump, the output is redirected to a temporary text file
- The text file is then iterated over line by line; grabbing bytes, stripping whitespace, & formating it as shellcode
- The shellcode formated for the current line will be appended to a variable
- Once all iterations are complete the temp file is deleted and final shellcode is provided