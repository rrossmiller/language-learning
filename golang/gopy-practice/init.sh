clear
if [[ ! -d venv ]]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install pybindgen numpy

go get golang.org/x/tools/cmd/goimports;
go get github.com/go-python/gopy
