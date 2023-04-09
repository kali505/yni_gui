export python = python3
export pyinstaller = pyinstaller
export wine = wine
export cross_pyinstaller = $(wine) '$(HOME)/.wine/drive_c/Program Files/Python310/Scripts/pyinstaller.exe'
export cargo = cargo
export rm = rm
export cp = cp

export WINE_PYTHON_VER=3.10
export WINE_PYTHON_LIB="$(HOME)/.wine/drive_c/Program Files/Python310/"

all: build

build: pyyni/pyyni.so

release: build
	$(pyinstaller) main.spec

cross_build: pyyni/pyyni.pyd

cross_release: cross_build
	$(cross_pyinstaller) cross.spec

clean:
	$(MAKE) -C pyyni clean
	-$(rm) -f dist/*

pyyni/pyyni.so:
	$(MAKE) -C pyyni build

pyyni/pyyni.pyd:
	$(MAKE) -C pyyni cross_build


test: release
	./dist/main

cross_test: cross_release
	$(wine) ./dist/main.exe