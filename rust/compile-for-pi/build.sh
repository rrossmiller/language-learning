# PREP:
# brew install arm-linux-gnueabihf-binutils
# cargo build --release --target=${TARGET_ARCH}

# PKG_CONFIG_SYSROOT_DIR=/
cargo build --target armv7-unknown-linux-musleabihf
