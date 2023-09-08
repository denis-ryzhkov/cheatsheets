# Bash Cheat Sheet

* [Reference](https://www.gnu.org/software/bash/manual/bash.html)
* [Cheat Sheet by devhints](https://devhints.io/bash)
* Lint with [shellcheck](https://www.shellcheck.net/):
```bash
find . -name '*.sh' -print0 | xargs -0 shellcheck -s bash
```

## Lib

* [echorun](echorun)
* [try](try)

### My strict mode

```
#!/usr/bin/env bash
set -euo pipefail
```

* See also: [redsymbol](http://redsymbol.net/articles/unofficial-bash-strict-mode/), [disconnected](https://disconnected.systems/blog/another-bash-strict-mode/).

### rand-str

```bash
LC_ALL=C tr -dc A-Za-z0-9 </dev/urandom | head -c 64
```

[Explained](https://stackoverflow.com/a/62087619)

### shared_args

```bash
shared_args=(
  --some "$value_with_spaces"
  "$etc"
)

if condition
then shared_args+=(--more)
fi

command1 --args1 "${shared_args[@]}"
command2 --args2 "${shared_args[@]}"
```

### Single square brackets silent bug

```
A=""
if [ -n "$A"]
then echo "not empty"
else echo "empty"
fi
```

* [Detected](https://www.shellcheck.net/wiki/SC1020) with [shellcheck](https://www.shellcheck.net/).
