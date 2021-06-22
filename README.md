# sectra-calculator

Simple calculator implemented in Python 3.7.9 with lazy evaluation.
Tested and implemented in Windows 10 with Windows Terminal (PowerShell)

Time spent: ~3h

Execute script with:
`> python.exe \calculator.py [file_path]` to run from file or 
`> python.exe \calculator.py` to run interactively.

## Known issues
* Cross references are possible and may result in infinite recursion, but is handled by raising an exception. A cleaner solution would be to evaluate tree for cross references before adding a node. Example:
```
foo add bar
bar add foo
print foo
``` 
