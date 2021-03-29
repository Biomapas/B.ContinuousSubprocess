"""
Module for continuous subprocess management.
"""
import json
import subprocess
from collections import deque
from queue import Queue, Empty
from threading import Thread
from typing import Generator, Optional, IO, AnyStr


class ContinuousSubprocess:
    """
    Creates a process to execute a wanted command and
    yields a continuous output stream for consumption.
    """

    def __init__(self, command_string: str) -> None:
        """
        Constructor.

        :param command_string: A command to execute in a separate process.
        """
        self.__command_string = command_string
        self.__process: Optional[subprocess.Popen] = None

    @property
    def command_string(self) -> str:
        """
        Property for command string.

        :return: Command string.
        """
        return self.__command_string

    def terminate(self) -> None:
        if not self.__process:
            raise ValueError('Process is not running.')

        self.__process.terminate()

    def execute(
        self,
        shell: bool = True,
        path: Optional[str] = None,
        max_error_trace_lines: int = 1000,
        *args,
        **kwargs
    ) -> Generator[str, None, None]:
        """
        Executes a command and yields a continuous output from the process.

        :param shell: Boolean value to specify whether to
        execute command in a new shell.
        :param path: Path where the command should be executed.
        :param max_error_trace_lines: Maximum lines to return in case of an error.
        :param args: Other arguments.
        :param kwargs: Other named arguments.

        :return: A generator which yields output strings from an opened process.
        """
        # Check if the process is already running (if it's set, then it means it is running).
        if self.__process:
            raise RuntimeError(
                'Process is already running. '
                'To run multiple processes initialize a second object.'
            )

        process = subprocess.Popen(
            self.__command_string,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            shell=shell,
            cwd=path,
            *args,
            **kwargs
        )

        # Indicate that the process has started and is now running.
        self.__process = process

        # Initialize a mutual queue that will hold stdout and stderr messages.
        q = Queue()
        # Initialize a limited queue to hold last N of lines.
        dq = deque(maxlen=max_error_trace_lines)

        # Create a parallel thread that will read stdout stream.
        stdout_thread = Thread(
            target=ContinuousSubprocess.__read_stream, args=[process.stdout, q]
        )
        stdout_thread.start()

        # Create a parallel thread that will read stderr stream.
        stderr_thread = Thread(
            target=ContinuousSubprocess.__read_stream, args=[process.stderr, q]
        )
        stderr_thread.start()

        # Run this block as long as our main process is alive.
        while process.poll() is None:
            try:
                # Rad messages produced by stdout and stderr threads.
                item = q.get(block=True, timeout=1)
                dq.append(item)
                yield item
            except Empty:
                pass

        return_code = process.poll()

        # Make sure both threads have finished.
        stdout_thread.join(timeout=1)
        stderr_thread.join(timeout=1)

        # Indicate that the process has finished as is no longer running.
        self.__process = None

        if return_code:
            error_trace = list(dq)
            raise subprocess.CalledProcessError(
                returncode=return_code,
                cmd=self.__command_string,
                output=json.dumps(
                    {
                        'message': 'An error has occurred while running the specified command.',
                        'trace': error_trace,
                        'trace_size': len(error_trace),
                        'max_trace_size': max_error_trace_lines,
                    }
                ),
            )

    @staticmethod
    def __read_stream(stream: IO[AnyStr], queue: Queue):
        for line in iter(stream.readline, ''):
            if line != '':
                queue.put(line)
