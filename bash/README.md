# Bash Cheat Sheet

* [Reference](https://www.gnu.org/software/bash/manual/bash.html)
* [Cheat Sheet by devhints](https://devhints.io/bash)
* Lint with [shellcheck](https://www.shellcheck.net/):
```bash
sh_files=$(find . -name '*.sh')
shellcheck -s bash $sh_files
```
* Arrays are great for:
```bash
shared_args=(
  --some "$value_with_spaces"
  "$etc"
)
command1 --args1 "${shared_args[@]}"
command2 --args2 "${shared_args[@]}"
```

## Lib

* [echorun](echorun)
* [try](try)

### rand-str

```bash
LC_ALL=C tr -dc A-Za-z0-9 </dev/urandom | head -c 64
```

[Explained](https://stackoverflow.com/a/62087619)
