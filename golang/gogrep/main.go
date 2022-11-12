package main

import (
	"errors"
	"flag"
	"fmt"
	"os"
	"strings"
	"unicode/utf8"

	"github.com/fatih/color"
)

var green = color.New(color.FgRed).SprintFunc()

func main() {
	// start := time.Now()
	parallel := flag.Bool("p", false, "search files in parallel")
	noCase := flag.Bool("i", false, "case insensitve")
	// recursive := flag.Bool("r", false, "recursive")
	flag.Parse()

	args := flag.Args()
	pattern, file := args[0], args[1]
	if *noCase {
		pattern = strings.ToLower(pattern)
	}
	// regex

	if _, e := os.Stat(file); errors.Is(e, os.ErrNotExist) {
		// panic(e)
		fmt.Printf("%q does not exist\n", file)
		os.Exit(1)
	}

	var fileBytes []byte
	fileBytes, e := os.ReadFile(file)
	check(e)
	fileContents := string(fileBytes)

	// check the file contents for the input string
	// TODO support multiple instance in the same line (instead of seeing if the line has it,
	// slide over each token and add to map if found (key = line num, val = str))
	patternLength := utf8.RuneCountInString(pattern)
	lines := strings.Split(fileContents, "\n")
	var sb strings.Builder
	var lineSb strings.Builder
	if *parallel {
		fmt.Println("not implemented yet")
		// 	fmt.Println("running parallel")
		// 	var wg sync.WaitGroup
		// 	wg.Add(len(lines))
		// 	for i, line := range lines {
		// 		go findParallel(i, patternLength, line, pattern, &wg)
		// 	}
		// 	wg.Wait()
	} else {
		for i, line := range lines {
			lineHasString := false
			lineCheck := strings.Clone(line)
			// if ignore case, make everything lowercase
			if *noCase {
				lineCheck = strings.ToLower(lineCheck)
			}
			// for every word on the line
			lineSplit := strings.Split(line, " ")
			for j, word := range strings.Split(lineCheck, " ") {
				// if the word contains the pattern
				if strings.Contains(word, pattern) {
					lineHasString = true
					idx := strings.Index(word, pattern)                           // start index of the pattern in the word
					pre := string(lineSplit[j][:idx])                             // string before the pattern
					match := green(string(lineSplit[j][idx : idx+patternLength])) //pattern in the string
					post := string(lineSplit[j][idx+patternLength:])              // string after the pattern
					lineSplit[j] = pre + match + post
				}
				lineSb.WriteString(lineSplit[j] + " ")
			}
			if lineHasString {
				s := fmt.Sprintf("%d: %s\n", i+1, lineSb.String())
				sb.WriteString(s)
			}
			lineSb.Reset()
		}
	}
	fmt.Println(sb.String())
	// fmt.Printf("elapsed: %v seconds\n", time.Since(start))
}

// func findParallel(i, patternLength int, line, pattern string, wg *sync.WaitGroup) {
// 	defer wg.Done()
// 	if strings.Contains(line, pattern) {
// 		idx := strings.Index(line, pattern)
// 		pre := string(line[:idx])
// 		post := string(line[idx+patternLength:])
// 		fmt.Printf("%d: %s%s%s\n", i+1, pre, green((pattern)), post)
// 	}
// }

func check(e error) {
	if e != nil {
		panic(e)
		// log.Fatal("something went wrong reading the file")
	}
}
