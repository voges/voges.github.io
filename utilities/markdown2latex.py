import argparse
import logging
import os
import re
import sys


def _self_name() -> str:
    return os.path.basename(os.path.abspath(path=__file__))


def _markdown_to_latex_headings_level_1(markdown_text: str) -> str:
    def _to_latex_headings_level_1(match: re.Match) -> str:
        text = match.group(1)
        return f"\\vspace{{1.5em}}\\begin{{Large}}{text}\\end{{Large}}"

    pattern = re.compile(pattern=r"^# (.+)$", flags=re.MULTILINE)
    return pattern.sub(repl=_to_latex_headings_level_1, string=markdown_text)


def _markdown_to_latex_bold(markdown_text: str) -> str:
    pattern = r"\*\*(.*?)\*\*"
    replacement = r"\\textbf{\1}"
    return re.sub(pattern=pattern, repl=replacement, string=markdown_text)


def _markdown_to_latex_italic(markdown_text: str) -> str:
    pattern = r"_(.*?)_"
    replacement = r"\\emph{\1}"
    return re.sub(pattern=pattern, repl=replacement, string=markdown_text)


def _markdown_to_latex_links(markdown_text: str) -> str:
    pattern = r"\[([^\]]+)\]\(([^)]+)\)"
    replacement = r"\\href{\2}{\1}"
    return re.sub(pattern=pattern, repl=replacement, string=markdown_text)


def _markdown_to_latex_linebreaks(markdown_text: str) -> str:
    pattern = r"\\\n"
    replacement = r"\\\\\n"
    return re.sub(pattern=pattern, repl=replacement, string=markdown_text)


def markdown_to_latex(markdown_text: str) -> str:
    tmp_text = markdown_text

    tmp_text = _markdown_to_latex_headings_level_1(markdown_text=tmp_text)
    tmp_text = _markdown_to_latex_bold(markdown_text=tmp_text)
    tmp_text = _markdown_to_latex_italic(markdown_text=tmp_text)
    tmp_text = _markdown_to_latex_links(markdown_text=tmp_text)
    tmp_text = _markdown_to_latex_linebreaks(markdown_text=tmp_text)

    latex_text = tmp_text

    return latex_text


def read_file_contents(file_path: str) -> str:
    logger = logging.getLogger(name=_self_name())

    try:
        with open(file=file_path, mode="r") as file:
            file_contents = file.read()
            return file_contents
    except FileNotFoundError:
        logger.error(msg=f"File '{file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        logger.error(msg=f"An error occurred: {e}")
        sys.exit(1)


def write_file_contents(file_path: str, file_contents: str):
    logger = logging.getLogger(name=_self_name())

    try:
        with open(file=file_path, mode="w") as file:
            file.write(file_contents)
    except FileNotFoundError:
        logger.error(msg=f"File '{file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        logger.error(msg=f"An error occurred: {e}")
        sys.exit(1)


def logging_setup():
    log_format = "[%(name)s] [%(levelname)s] %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_format)


def parse_command_line() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument("input_file", type=str, help="path to the input file")
    parser.add_argument(
        "--output",
        "-o",
        default="output.tex",
        type=str,
        help="path to the output file (optional)",
        dest="output_file",
    )

    return parser.parse_args()


if __name__ == "__main__":
    logging_setup()
    logger = logging.getLogger(name=_self_name())

    args = parse_command_line()

    input_file = args.input_file
    output_file = args.output_file

    logger.info(msg=f"Input file: {input_file}")
    logger.info(msg=f"Output file: {output_file}")

    markdown_text = read_file_contents(file_path=input_file)
    latex_text = markdown_to_latex(markdown_text=markdown_text)
    write_file_contents(file_path=output_file, file_contents=latex_text)
