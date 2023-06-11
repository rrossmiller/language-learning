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
