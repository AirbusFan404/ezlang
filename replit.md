# EZLang

EZLang is a simple, lightweight interpreter and compiler for a custom esoteric-like language.

## Language Specification

EZLang uses a tape-based memory system (4096 slots) and a set of single-character commands.

### Commands

| Command | Description |
|---------|-------------|
| `+`     | Increment memory focus (pointer) |
| `-`     | Decrement memory focus (pointer) |
| `>`     | Read a line from stdin into the current memory focus |
| `<`     | Write the content of the current memory focus to stdout |
| `.`     | Pause for 0.2 seconds |
| `:`     | Pause for 0.5 seconds |
| `/`     | Toggle text color (Magenta / Reset) |
| `[`     | Start a comment (ignored until `]`) |
| `]`     | End a comment |
| `\`     | Escape the next character (output it literally) |
| *other* | Any other character is output literally to stdout |

## Installation

```bash
pip install git+http://github.com/AirbusFan404/ezlang
```

or with poetry:

``` bash
poetry add git+http://github.com/AirbusFan404/ezlang
```

or with uv:

``` bash
uv add git+http://github.com/AirbusFan404/ezlang
```

or with upm (make sure your project is configured in python first!):

``` bash
upm add git+http://github.com/AirbusFan404/ezlang
```

## Usage

### Running a module
```bash
ezlang <module_name>
```
*Note: The interpreter looks for `<module_name>.ezlang.txt`*

### Compiling a module
```bash
ezlangc <module_name>
```
*Compiles to `<module_name>_ezlang-compiled.py`*

### Debugging a module
```bash
ezlangd <module_name>
```

## Example

Create a file named `hello.ezlang.txt`:
```text
/Hello, world!/
```

Run it:
```bash
ezlang hello
```
