from subprocess import CalledProcessError

from b_continuous_subprocess.continuous_subprocess import ContinuousSubprocess


def test_subprocess_error() -> None:
    """
    Checks whether an exception is raised when an unknown command is passed.

    :return: No return.
    """
    try:
        list(ContinuousSubprocess('TestCommandThatProbablyDoesNotExist').execute())
    except CalledProcessError:
        return

    raise AssertionError('Expected to raise an exception.')
