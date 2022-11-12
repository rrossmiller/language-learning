package main

import (
	"errors"
	"flag"
	"fmt"
	"os"
	"strings"
	"sync"
	"unicode/utf8"

	"github.com/fatih/color"
)

var green = color.New(color.FgRed).SprintFunc()
var noCase *bool

func main() {
	// parallel := flag.Bool("p", false, "search files in parallel")
	noCase = flag.Bool("i", false, "case insensitve")
	// recursive := flag.Bool("r", false, "recursive")
	// regex := flag.Bool("r", false, "regex")
	flag.Parse()

	args := flag.Args()
	pattern, fileNames := args[0], args[1:]
	if *noCase {
		pattern = strings.ToLower(pattern)
	}

	var outputSb strings.Builder
	var wg sync.WaitGroup
	wg.Add(len(fileNames))

	// for every file
	for _, fileName := range fileNames {
		// check if the file exists
		if _, e := os.Stat(fileName); errors.Is(e, os.ErrNotExist) {
			fmt.Printf("%q does not exist\n", fileName)
			os.Exit(1)
		}

		multiFile := len(fileNames) > 1
		go searchFile(fileName, pattern, multiFile, &outputSb, &wg) // fixme write files together
	}
	wg.Wait()
	// print the output
	fmt.Println(outputSb.String())
}

func searchFile(fileName, pattern string, multiFile bool, outputSb *strings.Builder, wg *sync.WaitGroup) {
	defer wg.Done()

	// read the file
	var fileBytes []byte
	fileBytes, e := os.ReadFile(fileName) //todo stream file intsead of opening the whole thing
	check(e)
	fileContents := string(fileBytes)

	// check the file's contents for the pattern
	patternLength := utf8.RuneCountInString(pattern)
	lines := strings.Split(fileContents, "\n")
	var lineSb strings.Builder
	for i, line := range lines {
		lineHasPattern := false           //default: the line doesn't contain pattern
		lineMutStr := strings.Clone(line) // make a clone of the line so the output maintains the input's capitalization

		// if ignore case, make everything lowercase
		if *noCase {
			lineMutStr = strings.ToLower(lineMutStr)
		}

		// for every word on the line
		lineSplit := strings.Split(line, " ")
		for j, word := range strings.Split(lineMutStr, " ") {
			// if the word contains the pattern
			if strings.Contains(word, pattern) {
				lineHasPattern = true                                         // the pattern is found in the line
				idx := strings.Index(word, pattern)                           // start index of the pattern in the word
				pre := string(lineSplit[j][:idx])                             // string before the pattern
				match := green(string(lineSplit[j][idx : idx+patternLength])) // hightlight the pattern in the string
				post := string(lineSplit[j][idx+patternLength:])              // string after the pattern
				lineSplit[j] = pre + match + post                             // overwrite the text with the highlighted pattern
			}
			lineSb.WriteString(lineSplit[j] + " ") // write the word to the line string builder
		}

		// if the line has the pattern, write the line and line number to the output
		if lineHasPattern {
			var s string
			if multiFile {
				s = fmt.Sprintf("%d:%s: %s\n", i+1, fileName, lineSb.String())
			} else {
				s = fmt.Sprintf("%d: %s\n", i+1, lineSb.String())
			}
			outputSb.WriteString(s)
		}
		lineSb.Reset() // reset the line string builder for the next line
	}
}

func check(e error) {
	if e != nil {
		panic(e)
		// log.Fatal("something went wrong reading the fileNames")
	}
}
