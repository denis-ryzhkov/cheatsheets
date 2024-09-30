# realtime-capture

Async nature of IO streams prevents preserving ideal chronology without sort by timestamps.

For the cases when there are no timestamps provided, this solution:
* Prints from stdout and stderr of subprocess to stdout and stderr of current process in real time, flushing properly.
* Stops the loop only when all the streams are closed.
* Uses [selectors](https://docs.python.org/3/library/selectors.html) recommended for "high-level and efficient I/O multiplexing" on Unix-like OS.
* Passes typing and other linters.

## Source code

[realtime-capture.py](realtime-capture.py)

## Output sample

```
out 1
err 1
err 2
out 2
err 3
out 3
err 4
out 4
err 5
out 5
0
```
