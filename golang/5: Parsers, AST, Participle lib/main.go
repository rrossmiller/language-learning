// package main

// import (
// 	"fmt"
// 	"os"

// 	"github.com/alecthomas/repr"

// 	"github.com/alecthomas/participle/v2"
// 	"github.com/alecthomas/participle/v2/lexer"
// )

// // A custom lexer for INI files. This illustrates a relatively complex Regexp lexer, as well
// // as use of the Unquote filter, which unquotes string tokens.
// var (
// 	iniLexer = lexer.MustSimple([]lexer.SimpleRule{
// 		{Name: `Ident`, Pattern: `[a-zA-Z][a-zA-Z_\d]*`},
// 		{Name: `String`, Pattern: `"(?:\\.|[^"])*"`},
// 		{Name: `Float`, Pattern: `\d+(?:\.\d+)?`},
// 		{Name: `Punct`, Pattern: `[][=]`},
// 		{Name: "comment", Pattern: `[#;][^\n]*`},
// 		{Name: "whitespace", Pattern: `\s+`},
// 	})
// 	parser = participle.MustBuild[INI](
// 		participle.Lexer(iniLexer),
// 		participle.Unquote("String"),
// 		participle.Union[Value](String{}, Number{}),
// 	)
// )

// type INI struct {
// 	Properties []*Property `@@*`
// 	Sections   []*Section  `@@*`
// }

// type Section struct {
// 	Identifier string      `"[" @Ident "]"`
// 	Properties []*Property `@@*`
// }

// type Property struct {
// 	Key   string `@Ident "="`
// 	Value Value  `@@`
// }

// type Value interface{ value() }

// type String struct {
// 	Str string `@String`
// }

// func (String) value() {}

// type Number struct {
// 	Number float64 `@Float`
// }

// func (Number) value() {}

// func Check(err error) {
// 	if err != nil {
// 		panic(err)
// 	}
// }
// func main() {
// 	fmt.Printf("parser: %v\n\n***\n", parser)
// 	fName := "parseme.ini"
// 	b, err := os.ReadFile(fName)
// 	Check(err)
// 	ini, err := parser.ParseString(fName, string(b))
// 	Check(err)
// 	repr.Println(ini, repr.Indent("  "), repr.OmitEmpty(true))
// }

package main

import (
	"fmt"

	"github.com/alecthomas/participle/lexer"
	"github.com/alecthomas/participle/v2"
	"github.com/alecthomas/repr"
)

func Check(err error) {
	if err != nil {
		panic(err)
	}
}

// root structure
type INI struct {
	Properties []*Property `@@*`
	Sections   []*Section  `@@*`
}
type Property struct {
	Key   string `@Ident "="`
	Value *Value `@@`
}
type Value struct {
	Pos    lexer.Position
	Str    *string  ` @String`
	Number *float64 ` | @Float | @Int`
}
type Section struct {
	Identifier string      `"[" @Ident "]"`
	Properties []*Property `@@*`
}

// func main() {
// 	parser, err := participle.Build[INI]()
// 	Check(err)

// 	fName := "parseme.ini"
// 	b, _ := os.ReadFile(fName)
// 	ini, err := parser.ParseString(fName, string(b))
// 	Check(err)
// 	fmt.Printf("%v\n", ini)
// 	fmt.Println("\n\nrepr:")
// 	repr.Println(ini, repr.Indent("  "), repr.OmitEmpty(true))
// }

type Blank struct {
	Blank string `"_"`
}

func main() {
	parser, err := participle.Build[Blank]()
	Check(err)

	ini, err := parser.ParseString("fName", "_")
	Check(err)
	fmt.Printf("%v\n", ini)
	fmt.Println("\n\nrepr:")
	repr.Println(ini, repr.Indent("  "), repr.OmitEmpty(true))
}
