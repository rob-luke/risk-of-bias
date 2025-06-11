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

This command runs PyInstaller with the `--windowed` option to avoid opening a terminal window. The resulting application can be found in the `dist` directory.

