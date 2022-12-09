clear
go build

echo "GoGrep"
./gtime -p ./gogrep -i comman test/*.html

echo
echo "Grep"
./gtime -p grep -ni comman test/*.html