from b_continuous_subprocess.continuous_subprocess import ContinuousSubprocess


def test_subprocess_output() -> None:
    """
    Checks whether the output has an expected string.

    :return: No return.
    """
    generator = ContinuousSubprocess('python --version').execute()
    complete_output = '\n'.join(list(generator)).lower()

    assert 'python' in complete_output
