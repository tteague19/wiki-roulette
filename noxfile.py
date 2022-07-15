import tempfile

import nox

# By default, we only run the linting, safety, and testing sessions.
nox.options.sessions = "lint", "safety", "tests"

# By default, we run Flake8 on the package source tree, the test suite,
# noxfile.py itself. We can override this default by passing specific
# source files separated from Nox's options by '--'.
locations = ("src", "tests", "noxfile.py")


def install_with_constraints(session: nox.Session, *args, **kwargs) -> None:
    """
    Use the Poetry lock file to pin packages used in nox sessions.

    :param session: A nox Session object
    :type session: nox.Session
    """
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
        session.install(f"--constraint={requirements.name}", *args, **kwargs)


@nox.session(python="3.8")
def black(session: nox.Session) -> None:
    """
    Run a nox session with the black formatter.

    :param session: A nox Session object
    :type session: nox.Session
    """
    args = session.posargs or locations
    install_with_constraints(session, "black")
    session.run("black", *args)


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
    install_with_constraints(
        session,
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
        install_with_constraints(session, "safety")
        session.run("safety", "check", f"--file={requirements.name}", "--full-report")


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
    install_with_constraints(
        session, "coverage[toml]", "pytest", "pytest-cov", "pytest-mock"
    )
    session.run("pytest", *args)
