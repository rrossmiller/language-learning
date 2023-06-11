#!/bin/zsh
rm mini-grep

if [[ $1 == 'r' ]]; then
	echo "building release"
	cargo build --release &&
		mv target/release/mini-grep .
	shift
else
	cargo build &&
		mv target/debug/mini-grep .
fi

if [[ $? -ne 0 ]]; then
	exit 1
fi
clear
./mini-grep $@
