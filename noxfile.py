import tempfile

import nox

# By default, we only run the linting, safety, and testing sessions.
nox.options.sessions = "lint", "safety", "tests"


@nox.session(python="3.8")
def black(session: nox.Session) -> None:
    """
    Run a nox session with the black formatter.

    :param session: A nox Session object
    :type session: nox.Session
    """
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)


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


# By default, we run Flake8 on the package source tree, the test suite,
# noxfile.py itself. We can override this default by passing specific
# source files separated from Nox's options by '--'.
locations = ("src", "tests", "noxfile.py")


@nox.session(python=["3.9", "3.10"])
def lint(session: nox.Session) -> None:
    """
    Run the Flake8 linter on specified sections of code.

    :param session: A nox Session object
    :type session: nox.Session:return:
    """
    args = session.posargs or locations

    # We install Flake8 into the virtual environment via pip with the
    # following command. We also add the plugin for Black and import order.
    session.install(
        "flake8",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-import-order",
    )
    session.run("flake8", *args)


@nox.session(python=["3.9", "3.10"])
def safety(session):
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        session.install("safety")
        session.run("safety", "check", f"--file={requirements.name}", "--full-report")
