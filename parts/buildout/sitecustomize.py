
# The following is from
# /usr/lib/python2.6/sitecustomize.py
# install the apport exception handler if available
try:
    import apport_python_hook
except ImportError:
    pass
else:
    apport_python_hook.install()
