.. contents:: :depth: 1

Introduction
============

**mr.hermes** is an extension of the smtpd.DebuggingServer from the Python
standard library. It dumps all mails it receives to the standard output and
optionally to files in a configurable directory.

Usage
=====

There are several ways to use this package. Probably the most two common are
the following.

Command line
------------

Install it with your preferred Python packaging tool (setuptools, distribute,
pip or whatever). Run it from the command line using
``python -m smtpd -n -c mr.hermes.DebuggingServer localhost:8025``.

If you want to dump the output to a directory, then set the
**DEBUG_SMTP_OUTPUT_PATH** environment variable. For example like
``DEBUG_SMTP_OUTPUT_PATH=mails python -m smtpd -n -c mr.hermes.DebuggingServer localhost:8025``.

Buildout
--------

Add a part to your config like this::

    [debugsmtp]
    # Run a simple smtp server on 8025 that echos incoming email
    recipe = zc.recipe.egg
    eggs = mr.hermes
    entry-points = debugsmtp=runpy:run_module
    scripts = debugsmtp
    host = localhost
    port = 8025
    path = ${buildout:directory}/var/mails
    initialization =
        import os
        os.environ.setdefault('DEBUG_SMTP_OUTPUT_PATH', '${:path}')
        sys.argv[1:] = ['-n', '-c', 'mr.hermes.DebuggingServer', '${:host}:${:port}']
    arguments = 'smtpd', run_name='__main__', alter_sys=True

You can then add this script to something like supervisord_ and use
`mr.laforge`_ to automatically start it when you need it.

.. _supervisord: http://pypi.python.org/pypi/supervisor
.. _`mr.laforge`: http://pypi.python.org/pypi/mr.laforge
