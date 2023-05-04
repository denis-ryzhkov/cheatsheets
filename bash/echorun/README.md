# echorun

* Motivation:
  * When you want to log some complex command line and then execute it, you usually `set -x`.
  * But `set -x` logs to stderr, which is visualised as a red error message in some contexts, confusing a user with a false alert.
  * You could redirect stderr to stdout with `(set -x; ...) 2>&1`, but then a real error message from a command would also become stdout, a user may not notice it.
  * So we want to log a command directly to stdout, `set -x` does not support this, and we want to keep it DRY, so we create `echorun` function:

```bash
function echorun {
  # Echo the args, run the args.
  # Similar to `set -x`, but logs to stdout instead of stderr.
  # Explained: https://github.com/denis-ryzhkov/cheatsheets/tree/main/bash/echorun

  echo "${@@Q}"
  "$@"
}
```

* Test:
  ```bash
  echorun echo word "two words" 'new
  line' "single'quote" 'double"quote'
  ```

* If we'd use simple `echo "$@"`, then it would log a broken command without correct quotes:
  ```
  echo word two words new
  line single'quote double"quote
  ```
  * This happens because `"$@"` expands to `"echo" "word" "two words" ...` correctly,
    but the outer `echo` consumes these quotes and prints correct args unquoted,
    so we lose borders of each arg.

* So we use `"${@@Q}"` which means `"$@"` ["in a format that can be reused as input"](https://www.gnu.org/software/bash/manual/bash.html#Shell-Parameter-Expansion):
  ```
  'echo' 'word' 'two words' $'new\nline' 'single'\''quote' 'double"quote'
  ```
  * It adds extra quotes, which are consumed by the outer `echo`,
    preserving inner quotes in the output.
  * If we copy-paste it to a command line or to a script, it runs just fine.

* But if we use `"${@@Q}"` to run the args in a script,
  then it fails because of extra quotes:
  ```
  'echo': command not found
  ```
  * This happens because we tried to run `"'echo'"` instead of `"echo"` or `'echo'` or `echo`.

* So to run all args we need just `"$@"`.
  * It expands to `"echo" "word" "two words" ...` which is what we want in this case.
