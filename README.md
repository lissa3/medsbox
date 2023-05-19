### Med Sandbox

[] split dependencies

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
