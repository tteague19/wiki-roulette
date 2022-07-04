import nox


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
    args = session.posargs or ["--cov"]
    session.run("poetry", "install", external=True)
    session.run("pytest", *args)
