# B.ContinuousSubprocess

A helper package that lets you execute long running processes
and continuously receive their output.

#### Description

Imagine you want to programmatically run a command that lists objects
in a given directory. The command `subprocess.call('ls')` will do the 
trick quite conveniently. However, the same approach to long running
commands like `cdk deploy *` or `pytest -s` or `ls / -R` is not very
convenient as you get the whole output only when the process finishes.
This package solves this inconvenience by outputting data in real-time
as the process runs.

#### Remarks

[Biomapas](https://biomapas.com) aims to modernise life-science 
industry by sharing its IT knowledge with other companies and 
the community. This is an open source library intended to be used 
by anyone. Improvements and pull requests are welcome.

#### Related technology

- Python 3
- Python subprocess Popen
- OS processes

#### Assumptions

The project assumes the following:

- You have basic knowledge in python programming.
- You have basic knowledge in OS processes.

#### Useful sources

- Read more about python subprocess:<br>
https://docs.python.org/3/library/subprocess.html.

- Read more about python subprocess "Popen" specifically:<br>
https://docs.python.org/3/library/subprocess.html#popen-objects

#### Install

The project is built and uploaded to PyPi. Install it by using pip.

```
pip install b-continuous-subprocess
```

Or directly install it through source.

```
pip install .
```

### Usage & Examples

The library is extremely easy to use. Simply create an instance of 
`ContinuousSubprocess` and execute it to get a generator. Then iterate
through the generator to receive your process output in real time.

```python
from b_continuous_subprocess.continuous_subprocess import ContinuousSubprocess

command = 'cdk deploy *'
generator = ContinuousSubprocess(command).execute()

for data in generator:
    print(data, end='')
```

Example how to handle errors:

```python
import json
import subprocess

from b_continuous_subprocess.continuous_subprocess import ContinuousSubprocess

continuous_process = ContinuousSubprocess('cdk deploy *')
generator = continuous_process.execute()

try:
    for line in generator:
        print(line, end='')
except subprocess.CalledProcessError as ex:
    error_output = json.loads(ex.output)
    
    # Error message.
    message = error_output['message']
    # Stack trace.
    trace = error_output['trace']
    # The length of a stack trace (in lines).
    trace_size = error_output['trace_size']
    # The maximum possible (allowed) length of a stack trace.
    max_trace_size = error_output['max_trace_size']
    
    print(message)
    
    for line in trace:
        print(line, end='')
```

#### Testing

The project has tests that can be run. 
These are mostly simple tests that can be run out-of-the-box.

Run tests from a root directory with `pytest` python testing library:
```
pytest
```

The tests usually take less than a few seconds to complete.

#### Contribution

Found a bug? Want to add or suggest a new feature?<br>
Contributions of any kind are gladly welcome. You may contact us 
directly, create a pull-request or an issue in github platform.
Lets modernize the world together.