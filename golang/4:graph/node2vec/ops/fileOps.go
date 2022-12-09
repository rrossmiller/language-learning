package ops
import (
	"os"
)
func Check(e error) {
	if e != nil {
		panic(e)
	}
}

func WriteDot(b []byte) {
	err := os.WriteFile("g.dot", b, 0644) //644: -rw-r--r--
	Check(err)
}
