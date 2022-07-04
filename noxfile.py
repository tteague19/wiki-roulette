import nox


@nox.session(python=["3.9", "3.10"])
def tests(session: nox.Session) -> None:
    """
    Run tests with nox.

    :param session: A nox Session object
    :type session: nox.Session
    """
    session.run("poetry", "install", external=True)
    session.run("pytest", "--cov")
