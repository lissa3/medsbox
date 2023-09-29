### Med Sandbox

## Site about different medical topcs

# Main features:

1. django 4.2

2. Templates

3. Authentication (all-auth)

4. Nested comments (django-tree-bread) with crud's on them

5. Notifications (currently without email notifications)

## dev

```
pip-tools

pip-compile reqs/reqlinux.in (or dev.in)
pip install -r reqs/reqlinux.txt reqs/dev.txt
windows (here): upload files require python-magic-bin
linux: pip install libmagic
```
