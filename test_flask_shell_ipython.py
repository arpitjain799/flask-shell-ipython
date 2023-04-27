import pytest
from click.testing import CliRunner
from flask import Flask

from flask_shell_ipython import shell


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    return app


@pytest.fixture
def runner(app):
    return CliRunner()


def test_shell_command(runner, app, mocker):
    mocker.patch('IPython.start_ipython')

    with app.app_context():
        result = runner.invoke(shell, ["--no-banner"])

    assert result.exit_code == 0
    assert "IPython" not in result.output


def test_shell_command_with_banner(runner, app, mocker):
    mocker.patch('IPython.start_ipython')

    with app.app_context():
        result = runner.invoke(shell, ["--simple-prompt"])

    assert result.exit_code == 0
    assert "IPython" in result.output


def test_shell_command_with_custom_config(runner, app, mocker):
    mocker.patch('IPython.start_ipython')

    app.config['IPYTHON_CONFIG'] = {
        'InteractiveShell': {'confirm_exit': False}
    }

    with app.app_context():
        result = runner.invoke(shell, ["--no-banner"])

    assert result.exit_code == 0
    assert "IPython" not in result.output
