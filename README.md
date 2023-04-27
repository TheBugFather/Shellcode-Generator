<div align="center" style="font-family: monospace">
<h1>Shellcode-Generator</h1>
&#9745;&#65039; Bandit verified &nbsp;|&nbsp; &#9745;&#65039; Synk verified &nbsp;|&nbsp; &#9745;&#65039; Pylint verified 10/10
<br><br>

![alt text](https://github.com/ngimb64/Shellcode-Generator/blob/main/ShellcodeGen.png?raw=true)
</div>

## Purpose
The purpose is to run objdump on selected file, grab output bytes, & format as shellcode.

### License
The program is licensed under [GNU Public License v3.0](LICENSE.md)

### Contributions or Issues
[CONTRIBUTING](CONTRIBUTING.md)

## Prereqs
This program is updated to Python version 3.10.6 on Linux systems with objdump utility.
The modules used should already be included in the Python default installation.

## Installation
- Run the setup.py script to build a virtual environment and install all external packages in the created venv.

> Examples:<br> 
>       &emsp;&emsp;- Windows:  `python setup.py venv`<br>
>       &emsp;&emsp;- Linux:  `python3 setup.py venv`

- Once virtual env is built traverse to the (Scripts-Windows or bin-Linux) directory in the environment folder just created.
- For Windows, in the venv\Scripts directory, execute `activate` or `activate.bat` script to activate the virtual environment.
- For Linux, in the venv/bin directory, execute `source activate` to activate the virtual environment.
- If for some reason issues are experienced with the setup script, the alternative is to manually create an environment, activate it, then run pip install -r packages.txt in project root.
- To exit from the virtual environment when finished, execute `deactivate`.

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