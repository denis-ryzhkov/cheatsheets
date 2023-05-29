# saferun

Let's check this code:

```bash
#!/usr/bin/env bash
set -euo pipefail

function func {
  echo "func args: $@"
  func-bug
  echo func-never
}

if func arg1 arg2
then echo "func succeeded"
else echo "func failed"
fi
```

Expected output:

```
func args: arg1 arg2
./test.sh: line 6: func-bug: command not found
func failed
```

Actual output:

```
func args: arg1 arg2
./test.sh: line 6: func-bug: command not found
func-never
func succeeded
```

Wait, what?!

But we've used `set -e`, right? Maybe it is not inherited in the function?

```bash
function func {
  set -e
  echo "func args: $@"
  func-bug
  echo func-never
}
```

Actual output:
```
./test.sh: line 7: func-bug: command not found
func-never
func succeeded
```

But how...

```
help set

      -e  Exit immediately if a command exits with a non-zero status.
```

Right? No:

https://www.gnu.org/software/bash/manual/bash.html

> 4.3.1 The Set Builtin  
> -e  
> ...The shell does not exit if the command that fails is part of the command list immediately following a `while` or `until` keyword, part of the test in an `if` statement, part of any command executed in a `&&` or `||` list except the command following the final `&&` or `||`, any command in a pipeline but the last, or if the command’s return status is being inverted with `!`. If a compound command other than a subshell returns a non-zero status because a command failed while `-e` was being ignored, the shell does not exit.  
> ...If a compound command or shell function executes in a context where `-e` is being ignored, none of the commands executed within the compound command or function body will be affected by the `-e` setting, even if `-e` is set and a command returns a failure status. If a compound command or shell function sets `-e` while executing in a context where `-e` is ignored, that setting will not have any effect until the compound command or the command containing the function call completes.

The best workaround so far: https://stackoverflow.com/a/11092989

Reusable function:

```bash
function saferun {
  # Run the args in a `set -e` mode.
  # Error code should be checked with `if ((err))`.
  # Please don't check it directly with `if saferun`, `saferun ||`, etc.
  # Explained: https://github.com/denis-ryzhkov/cheatsheets/tree/main/bash/saferun

  set +e
  (set -e; "$@")
  declare -g err=$?
  set -e
}
```

Usage example:

```bash
saferun func arg1 arg2

if ((err))
then echo "func failed"
else echo "func succeeded"
fi
```

Actual output:
```
func args: arg1 arg2
./test.sh: line 6: func-bug: command not found
func failed
```

This time this is exactly what we expected.
