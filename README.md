# yni_gui
GUI version of yni.

Made using tkinter and rust.

# Dev Setup

This preject is for linux.

Essential tools: 
* rust toolchain
* python
* pyinstaller

Cross build for Windows (Optional):

1. Install wine.

2. Install python and pyinstaller in wine.

3. Install mingw-w64

4. cargo target add x86_64-pc-windows-gnu

You should setup cygwin or msys2 because this project is for linux.


# Build

## Building

```make build```

or

```make cross_build```

## Making Binary

``` make release```

or

``` make cross_release```