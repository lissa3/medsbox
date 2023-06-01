### Med Sandbox

[X] split dependencies
[X] statuic for dev (admin via static_root)

## setup

```
python -m venv venv
pip install -r req-dev.txt -r req.txt
[WinError 5] Access is denied  ..pip.exe' -
treatment: pip install --upgrade pip
isort .
black .
flake8 .
pre-commit install (auto: only if changed)
pre-commit run -a (forced:check all)

```

## dev

```
pip-tools in dev
dependency  reqs/req.in (or dev.in)
pip-compile reqs/req.in (or dev.in)
pip-compile req.txt or dev.txt
pip install -r reqs/req.txt reqs/dev.txt
```
