## Shellcode Generator
![alt text](https://github.com/ngimb64/Shellcode-Generator/blob/main/ShellcodeGen.png?raw=true)

&#9745;&#65039; Bandit verified<br>
&#9745;&#65039; Synk verified<br>
&#9745;&#65039; Pylint verified 10/10

## Prereqs
This program was designed for Python3 on Linux systems with objdump utility.
The modules used should already be included in the Python3 default installation.

## Purpose
The purpose is to run objdump on selected file, grab output bytes, & format as shellcode.

## Installation
- Run the setup.py script to build a virtual environment and install all external packages in the created venv.

> Example: `python3 setup.py venv`

- Once virtual env is built traverse to the (Scripts-Windows or bin-Linux) directory in the environment folder just created.
- For Windows in the Scripts directory, for execute the `./activate` script to activate the virtual environment.
- For Linux in the bin directory, run the command `source activate` to activate the virtual environment.

## How it works
> Example: `python3 shellcodeGen.py <executable>`

- If arg is not passed, the user is prompted for input
- Selected executable is run in objdump, the output in intel syntax is redirected to a temporary text file
- The text file is then iterated over line by line; grabbing bytes, stripping whitespace, & formatting it as shellcode
- The shellcode formatted for the current line will be appended to a variable
- Once all iterations are complete the temp file is deleted and final shellcode result is provided

## Function Layout
-- shellcode_gen.py --
> objdump_run &nbsp;-&nbsp; Takes the passed in binary executable, runs objdump utility, and writes the output to file.

> print_err &nbsp;-&nbsp; Prints a timed error message via stderr.

> prompt_user &nbsp;-&nbsp; Prompt the user for input, handle errors accordingly.

> main &nbsp;-&nbsp; Take input file, run in objdump, and parse output into shellcode.

## Exit Codes
> 0 - Successful operation<br>
> 1 - Error occurred during parsing of args in startup<br>
> 2 - Error occurred writing objdump output to file<br>
> 3 - Error occurred reading objdump output for parsing shellcode