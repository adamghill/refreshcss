from pathlib import Path

from click.testing import CliRunner

from refreshcss.cli import cli
from tests.utils import assert_css

expected = """\
td div.pos {
    color: green;
    width: 20px;
    font-weight: 700;
}
td div.neg {
    color: red;
    width: 20px;
    }
.table {
    border: 1px #ccc solid;
    }
.callout {
    border: 1px #ccc solid;
    background: #f2f2f2;
    margin: 0px 3rem 0px 3rem;
    border-radius: 1rem;
    padding: 2rem;
    }
.container {
    margin-left: 0px;
    }
.header.last-commit {
    min-width: 8em;
    }
.header {
    font-weight: bold;
    }
.info {
    cursor: help;
    color: grey;
    font-weight: normal;
    }
.info::before {
    content: '\\27AF  ';
    }
.digital-ocean {
    float: right;
    }
@media only screen and (max-width: 30em) {
    .digital-ocean {
        display: none;
    }
}"""


def test_cli():
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "tests/static/css/styles.css",
            "tests/templates/base.html",
            "tests/templates/index.html",
        ],
    )
    assert result.exit_code == 0
    assert_css(expected, result.output)


def test_cli_recursive():
    runner = CliRunner()
    result = runner.invoke(
        cli, ["--recursive", "tests/static/css/styles.css", "tests/templates/"]
    )
    assert result.exit_code == 0
    assert_css(expected, result.output)


def test_cli_encoding():
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "--encoding",
            "utf-8",
            "-r",
            "tests/static/css/styles.css",
            "tests/templates/",
        ],
    )
    assert result.exit_code == 0
    assert_css(expected, result.output)


def test_cli_invalid_encoding():
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "--encoding",
            "foobar",
            "-r",
            "tests/static/css/styles.css",
            "tests/templates/",
        ],
    )
    assert result.exit_code == 2
    assert "Error: Invalid value for encoding" in result.output


def test_cli_output_file():
    runner = CliRunner()
    base_path = Path.cwd()
    with runner.isolated_filesystem():
        result = runner.invoke(
            cli,
            [
                "-o",
                "output.css",
                "-R",
                f"{base_path}/tests/static/css/styles.css",
                f"{base_path}/tests/templates/",
            ],
        )
        assert result.exit_code == 0
        assert_css(expected, Path("output.css").read_text(encoding="utf-8"))
