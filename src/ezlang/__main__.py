import click
import sys
import typing_extensions
from . import run, compile_module, print_debug


@click.group(help="EZLang CLI (python -m ezlang)")
def main():
  pass


@click.command(help="Run an EZLang module.")
@click.argument("module", type=str, required=True)
@click.option("--input",
              type=click.File("r"),
              default="-",
              help="Input file (default: stdin)")
@click.option("--output",
              type=click.File("w"),
              default="-",
              help="Output file (default: stdout)")
def ezlang(module: str, input: typing_extensions.TextIO,
           output: typing_extensions.TextIO):
  if input == "-":
    input = sys.stdin
  if output == "-":
    output = sys.stdout
  run(module, input, output)


@click.command(help="Compile an EZLang module.")
@click.argument("module", type=str, required=True)
def ezlangc(module: str):
  compile_module(module)


@click.command(help="Debug an EZLang module.")
@click.argument("module", type=str, required=True)
@click.option("--input",
              "-i",
              type=click.File("r"),
              default="-",
              help="Input file (default: stdin)")
@click.option("--output",
              "-o",
              type=click.File("w"),
              default="-",
              help="Output file (default: stdout)")
@click.option("--error", "-e", type=click.File("w"), default="-")
def ezlangd(module: str, input: typing_extensions.TextIO,
            output: typing_extensions.TextIO, error):
  if input == "-":
    input = sys.stdin
  if output == "-":
    output = sys.stdout
  if error == "-":
    error = sys.stderr
  print_debug(module, input, output, error)


main.add_command(ezlang, "run")
main.add_command(ezlangc, "compile")
main.add_command(ezlangd, "debug")

if __name__ == "__main__":
  main()
