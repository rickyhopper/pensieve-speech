pensieve-speech
===

pensieve is an easy extensible server architecture to accept socket data such as sensor readings, images, etc.
pensieve-speech is an extension of pensieve, with a handler for glass-based (or any) speech-to-text applications.
As of time of writing, it is unstable and highly volatile. Do not expose to open flames or belligerent children.

Known Dependencies
------------

* [Python 2.7.x](http://www.python.org/)
* [NumPy](http://www.numpy.org/) (pensieve doesn't need SciPy, just NumPy, but it doesn't hurt)
* [OpenCV 2.4.x](http://opencv.org/)
* [PyZMQ](http://zeromq.org/bindings:python) (optional, for streaming/pub-sub servers)
* [ffmpeg](http://www.ffmpeg.org/) (for converting audio files to flac format)

Installation (adapted from pensieve)
------------

1. Clone:
    
    ```bash
    $ git clone git@github.com:rickyhopper/pensieve-speech.git
    ```

2. Install (after `cd pensieve/`):
    
    ```bash
    $ [sudo] python setup.py develop
    ```
    
    Note: This installs in [development mode](https://pythonhosted.org/setuptools/setuptools.html#develop-deploy-the-project-source-in-development-mode), which means Python modules are exposed directly from the source directory. You can then update your local copy to pull in changes from the remote repository, and/or make changes yourself. You can also use `[sudo] python setup.py install` for a typical installation (recommended: [Python virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/)).

3. Install ffmpeg.

Usage
-----

Run server:
```bash
$ python -m pensieve.server
```

Run test client:
```bash
$ python -m pensieve.tests.client
```

Note: You can connect to a running server instance from any pensieve client.
