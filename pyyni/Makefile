clean:
	-$(rm) -f pyyni.so
	-$(rm) -f pyyni.pyd
	$(cargo) clean

build: pyyni.so

cross_build: pyyni.pyd

pyyni.so: target/release/libpyyni.so
	$(cp) target/release/libpyyni.so pyyni.so

target/release/libpyyni.so:
	$(cargo) build --release

pyyni.pyd: target/x86_64-pc-windows-gnu/release/pyyni.dll
	$(cp) target/x86_64-pc-windows-gnu/release/pyyni.dll pyyni.pyd

target/x86_64-pc-windows-gnu/release/pyyni.dll:
	PYO3_CROSS_PYTHON_VERSION=$(WINE_PYTHON_VER) \
	PYO3_CROSS_LIB_DIR=$(WINE_PYTHON_LIB) \
	$(cargo) build --target=x86_64-pc-windows-gnu --release