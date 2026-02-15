import colorama
import time
import sys
import typing_extensions
import string
import traceback


def interpret(code: str,
              input: typing_extensions.TextIO = sys.stdin,
              output: typing_extensions.TextIO = sys.stdout) -> None:
  comment = False
  current_color = colorama.Fore.RESET
  focus = 0
  ignore = False
  u = [""] * 4096
  for i in code:
    if comment:
      comment = i != "]"
    elif ignore:
      output.write(i)
      output.flush()
      ignore = False
    else:
      match i:
        case "[":
          comment = True
        case "\\":
          ignore = True
        case "+":
          focus += 1
          focus %= 4096
        case "-":
          focus -= 1
          focus %= 4096
        case ">":
          output.write(f"{colorama.Fore.BLUE}>{current_color}")
          output.flush()
          u[focus] = input.readline().removesuffix("\n")
        case "<":
          output.write(u[focus])
          output.flush()
        case ".":
          time.sleep(0.2)
        case ":":
          time.sleep(0.5)
        case "/":
          if current_color == colorama.Fore.RESET:
            output.write(colorama.Fore.MAGENTA)
            output.flush()
            current_color = colorama.Fore.MAGENTA
          else:
            output.write(colorama.Fore.RESET)
            output.flush()
            current_color = colorama.Fore.RESET
        case _:
          output.write(i)
          output.flush()
  output.write(colorama.Fore.RESET)


def run(module: str,
        input: typing_extensions.TextIO = sys.stdin,
        output: typing_extensions.TextIO = sys.stdout) -> None:
  for i in module:
    assert i in string.ascii_letters + string.digits + "_-,."
  with open(module.replace(",", "/") + ".ezlang.txt", "r") as f:
    interpret(f.read())


def debug(module: str,
          input: typing_extensions.TextIO = sys.stdin,
          output: typing_extensions.TextIO = sys.stdout) -> dict[str, str]:
  try:
    run(module, input, output)
  except BaseException as e:
    return {
        "error": type(e).__name__,
        "message": str(e),
        "traceback": traceback.format_exc()
    }
  else:
    return {"error": "SystemExit", "message": "0", "traceback": "0"}


def print_debug(module: str,
                input: typing_extensions.TextIO = sys.stdin,
                output: typing_extensions.TextIO = sys.stdout,
                error: typing_extensions.TextIO = sys.stderr) -> None:
  result = debug(module, input, output)
  for k, v in result.items():
    error.write(
        f"{colorama.Fore.YELLOW}{k}{colorama.Fore.GREEN}: {colorama.Fore.CYAN}{v}\n"
    )
    error.flush()


def compile(code: str) -> str:
  comment = False
  current_color = colorama.Fore.RESET
  focus = 0
  ignore = False
  result = ["import time", "import sys", "u = ['' for _ in range(4096)]"]
  for i in code:
    if comment:
      if i == "]":
        comment = False
      elif i == "\n":
        result.append("#")
      else:
        result[-1] += i
    elif ignore:
      result.append(f"sys.stdout.write({repr(i)})")
      result.append("sys.stdout.flush()")
      ignore = False
    else:
      match i:
        case "[":
          result.append("#")
          comment = True
        case "\\":
          ignore = True
        case "+":
          focus += 1
          focus %= 4096
        case "-":
          focus -= 1
          focus %= 4096
        case ">":
          result.append("sys.stdout.write(f\"\\033[34m>\\033[0m\")")
          result.append("sys.stdout.flush()")
          result.append(
              f"u[{focus}] = sys.stdin.readline().removesuffix('\\n')")
        case "<":
          result.append(f"sys.stdout.write(u[{focus}])")
          result.append("sys.stdout.flush()")
        case ".":
          result.append("time.sleep(0.2)")
        case ":":
          result.append("time.sleep(0.5)")
        case "/":
          if current_color == colorama.Fore.RESET:
            result.append(f"sys.stdout.write({repr(colorama.Fore.MAGENTA)})")
            result.append("sys.stdout.flush()")
            current_color = colorama.Fore.MAGENTA
          else:
            result.append(f"sys.stdout.write({repr(colorama.Fore.RESET)})")
            result.append("sys.stdout.flush()")
            current_color = colorama.Fore.RESET
        case _:
          result.append(f"sys.stdout.write({repr(i)})")
          result.append("sys.stdout.flush()")
  result.append(f"sys.stdout.write({repr(colorama.Fore.RESET)})")
  return "\n".join(result)


def compile_module(module: str) -> None:
  for i in module:
    assert i in string.ascii_letters + string.digits + "_-,."
  with open(module.replace(",", "/") + ".ezlang.txt", "r") as f:
    code = f.read()
  with open(module.replace(",", "/") + "_ezlang-compiled.py", "w") as f:
    f.write(compile(code))
