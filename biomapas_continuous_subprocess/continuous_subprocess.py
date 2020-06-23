import subprocess
from typing import Generator, Optional


class ContinuousSubprocess:
    """
    Creates a process to execute a wanted command and yields a continuous output stream for consumption.
    """
    def __init__(self, command_string: str) -> None:
        """
        Constructor.

        :param command_string: A command to execute in a separate process.
        """
        self.__command_string = command_string

    def execute(self, shell: bool = True, path: Optional[str] = None, *args, **kwargs) -> Generator[str, None, None]:
        """
        Executes a command and yields a continuous output from the process.

        :param shell: Boolean value to specify whether to execute command in a new shell.
        :param path: Path where the command should be executed.
        :param args: Other arguments.
        :param kwargs: Other named arguments.

        :return: A generator which yields output strings from an opened process.
        """
        process = subprocess.Popen(
            self.__command_string,
            stdout=subprocess.PIPE,
            universal_newlines=True,
            shell=shell,
            cwd=path,
            *args,
            **kwargs
        )

        for stdout_line in iter(process.stdout.readline, ""):
            yield stdout_line

        process.stdout.close()
        return_code = process.wait()

        if return_code:
            raise subprocess.CalledProcessError(return_code, self.__command_string)
