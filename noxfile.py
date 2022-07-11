import nox

# By default, we exclude Black from the sessions we run.
nox.options.sessions = "lint", "tests"

# By default, we run Flake8 on the package source tree, the test suite,
# noxfile.py itself. We can override this default by passing specific
# source files separated from Nox's options by '--'.
locations = "src", "tests", "noxfile.py"


@nox.session(python=["3.9", "3.10"])
def tests(session: nox.Session) -> None:
    """
    Run tests with nox.

    :param session: A nox Session object
    :type session: nox.Session
    """
    # If the first argument (a set of positional arguments) is non-empty, we
    # use its contents. Otherwise, we default to the settings for coverage.py
    # in the TOML file.
    args = session.posargs or ["--cov", "-m", "not e2e"]
    session.run("poetry", "install", external=True)
    session.run("pytest", *args)


@nox.session(python=["3.9", "3.10"])
def lint(session: nox.Session) -> None:
    """
    Run the Flake8 linter on specified sections of code.

    :param session: A nox Session object
    :type session: nox.Session:return:
    """
    args = session.posargs or locations

    # We install Flake8 into the virtual environment via pip with the
    # following command. We also add the plugin for Black.
    session.install("flake8", "flake8-black")
    session.run("flake8", *args)
