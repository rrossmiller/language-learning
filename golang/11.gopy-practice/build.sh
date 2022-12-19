export PATH="$HOME/go/bin:$PATH"
rm -rf out
gopy build -output=out -vm=python3 . && \
clear; \
python3 slices.py