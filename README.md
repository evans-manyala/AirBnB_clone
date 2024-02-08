# AirBnB_clone aka hbnb

## Table of contents

- [Introduction](#Introduction)
- [Environment](#Environment)
- [Installation](#Installation)
- [Testing](#Testing)
- [Usage](#Usage)
- [Authors](#Authors)

## Introduction

This is a solo project to build a clone (hbnb) of [AirBnB](https://www.airbnb.com) for ALX SE Course.

The console is a command interpreter for clone AirBnb Project and it performs the following tasks:

- Creating a new object
- Retriving an object from a file
- Performing operations on objects
- Destroying an object

### Storage

Classes created are managed by the `Storage` engine in the `FileStorage` Class.

## Environment

The following are the enviroment used to design, test and run the clone AirBnB console. All the development and testing was done using these platforms:

- MacOs Ventura 13.6.4 and OS Ubuntu 22.04 LTS
- Python 3.11.2
- VSCode 1.86
- Vim 9.0
- Code version control with Git 2.39.5
- Code hosting via GitHub

<a href="https://www.apple.com/macos/sonoma/" target="_blank"> <img height="" src="https://img.shields.io/badge/mac%20os-000000?style=for-the-badge&logo=apple&logoColor=white" alt="Apple"></a> <a href="https://ubuntu.com/" target="_blank"> <img height="" src="https://img.shields.io/static/v1?label=&message=Ubuntu&color=E95420&logo=Ubuntu&logoColor=E95420&labelColor=2F333A" alt="Ubuntu"></a><!-- bash --> <a href="https://www.gnu.org/software/bash/" target="_blank"> <img height="" src="https://img.shields.io/static/v1?label=&message=GNU%20Bash&color=4EAA25&logo=GNU%20Bash&logoColor=4EAA25&labelColor=2F333A" alt="terminal"></a> <!-- python--> <a href="https://www.python.org" target="_blank"> <img height="" src="https://img.shields.io/static/v1?label=&message=Python&color=FFD43B&logo=python&logoColor=3776AB&labelColor=2F333A" alt="Python"></a> </a> <!-- vim --> <a href="https://www.vim.org/" target="_blank"> <img height="" src="https://img.shields.io/static/v1?label=&message=Vim&color=019733&logo=Vim&logoColor=019733&labelColor=2F333A" alt="Suite CRM"></a> <!-- vs code --> <a href="https://code.visualstudio.com/" target="_blank"> <img height="" src="https://img.shields.io/static/v1?label=&message=Visual%20Studio%20Code&color=5C2D91&logo=Visual%20Studio%20Code&logoColor=5C2D91&labelColor=2F333A" alt="Visual Studio"></a> </a><!-- git --> <a href="https://git-scm.com/" target="_blank"> <img height="" src="https://img.shields.io/static/v1?label=&message=Git&color=F05032&logo=Git&logoColor=F05032&labelColor=2F333A" alt="git distributed version control system"></a> <!-- github --> <a href="https://github.com" target="_blank"> <img height="" src="https://img.shields.io/static/v1?label=&message=GitHub&color=181717&logo=GitHub&logoColor=f2f2f2&labelColor=2F333A" alt="Github"></a>

 <!-- Style guidelines -->

- Style guidelines:
  - [pycodestyle (version 2.11.\*)](https://pypi.org/project/pycodestyle/)
  - [PEP8](https://pep8.org/)

## Installation

```bash
git clone https://github.com/evans-manyala/AirBnB_clone.git
```

Change to the `AirBnb` directory and run the command:

```bash
 ./console.py
```

### Execution

For the interactive mode

```bash
$ ./console.py
(hbnb) help

Documented commands (type help <topic>):
========================================
EOF  help  quit

(hbnb)
(hbnb)
(hbnb) quit
$
```

For the Non-interactive mode

```bash
$ echo "help" | ./console.py
(hbnb)

Documented commands (type help <topic>):
========================================
EOF  help  quit
(hbnb)
$
$ cat test_help
help
$
$ cat test_help | ./console.py
(hbnb)

Documented commands (type help <topic>):
========================================
EOF  help  quit
(hbnb)
$
```

## Testing

For all the unit testing, these are defined in the `tests` folder.

### Documentation

- Modules:

```python
python3 -c 'print(__import__("my_module").__doc__)'
```

- Classes:

```python
python3 -c 'print(__import__("my_module").MyClass.__doc__)'
```

- Functions (inside and outside a class):

```python
python3 -c 'print(__import__("my_module").my_function.__doc__)'
```

and

```python
python3 -c 'print(__import__("my_module").MyClass.my_function.__doc__)'
```

### Python Unit Tests

- unittest module
- File extension `.py`
- Files and folders star with `test_`
- Organization:for `models/base.py`, unit tests in: `tests/test_models/test_base.py`
- Execution command: `python3 -m unittest discover tests`
- or: `python3 -m unittest tests/test_models/test_base.py`

### run test in interactive mode

```bash
echo "python3 -m unittest discover tests" | bash
```

### run test in non-interactive mode

To perform the tests in non-interactive mode, use the command:

````bash
python3 -m unittest discover tests```


- Quit the console:

```bash
(hbnb) quit
$
````

## Authors

<details>
    <summary>Evans Manyala</summary>
    <ul>
    <li><a href="https://www.github.com/evans-Manyala">Github</a></li>
    <li><a href="https://www.twitter.com/evans_manyala">Twitter</a></li>
    <li><a href="mailto:imagineitke@gmail.com">e-mail</a></li>
    </ul>
</details>
