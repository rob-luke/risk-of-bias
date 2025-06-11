# macOS Standalone Application

A simple script is provided to create a standalone macOS application using [PyInstaller](https://pyinstaller.org/).
The generated application bundles the `risk_of_bias` web interface so it can be run without a Python interpreter.

## Building

First install the optional development dependencies, which include PyInstaller:

```console
pip install "risk_of_bias[all]"
```

Then run the build script:

```console
make mac
```

The resulting application can be found in the `dist` directory.
It should launch the web app after a few seconds when run.

## GitHub Release Builds

Each time a release is created on GitHub, an automated workflow runs
`make mac` on a macOS runner and attaches the resulting application to
the release. The pre-built download can be found in the release assets.
