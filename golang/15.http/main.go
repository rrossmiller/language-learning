package main

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"math"
	"net/http"
	"os"
	"time"

	"golang.org/x/text/language"
	"golang.org/x/text/message"
)

func main() {
	start := time.Now()
	readFile("ndc.json")
	fmt.Println()
	fmt.Println(time.Since(start))
	fmt.Println()
	fmt.Println()

	// // stream the json
	// fmt.Println("stream")
	// start = time.Now()
	// f, err := os.Open("ndc.json")
	// if err != nil {
	// 	panic(err)
	// }
	// decodeStream(f)
	// fmt.Println(time.Since(start))

	// fmt.Println()
	// fmt.Println()
	fmt.Println("stream Async (not yet)")
	start = time.Now()
	decodeAsync("ndc.json")
	fmt.Println()
	fmt.Println()
	fmt.Println(time.Since(start))
}

func decodeAsync(f string) {
	r, err := os.Open(f)
	if err != nil {
		panic(err)
	}
	fmt.Println("file opened")
	dec := json.NewDecoder(r)

	// read open bracket
	_, err = dec.Token()
	if err != nil {
		log.Fatal(err)
	}

	//async work
	jobs := make(chan Ndc)
	numWorkers := 4
	for i := 0; i < numWorkers; i++ {
		go func(jobs <-chan Ndc) {
			url := "https://api.fda.gov/drug/ndc.json?search=product_ndc:"
			var ndcResponse NdcResponse
			i := 0
			for n := range jobs {
				fmt.Print(i)
				i++
				// confirm the NDC
				//TODO remap the ndc from 11 to newer format https://health.maryland.gov/phpa/OIDEOR/IMMUN/Shared%20Documents/Handout%203%20-%20NDC%20conversion%20to%2011%20digits.pdf
				resp, err := http.Get(url + n.NDC)
				if err != nil {
					panic(err)
				}
				body, err := io.ReadAll(resp.Body)
				if err != nil {
					panic(err)
				}

				err = json.Unmarshal(body, &ndcResponse)
				if err != nil {
					panic(err)
				}
				resp.Body.Close()
			}
		}(jobs)
	}
	// while the array contains values
	i := 0
	for dec.More() {
		var ndc Ndc
		// decode an array value (Message)
		err := dec.Decode(&ndc)
		if err != nil {
			panic(err)
		}
		// write the ndc to a channel and process it in parallel
		jobs <- ndc
		i++
		if i == 100 {
			break
		}
	}
	close(jobs)

	// read closing bracket
	_, err = dec.Token()
	if err != nil {
		panic(err)
	}
}

func readFile(fname string) {
	// read in the NDCs from graph
	fmt.Println("file")
	b, err := os.ReadFile(fname)
	if err != nil {
		panic(err)
	}
	fmt.Println("file read")
	var ndcs []Ndc
	json.Unmarshal(b, &ndcs)

	url := "https://api.fda.gov/drug/ndc.json?search=product_ndc:"
	var ndcResponse NdcResponse
	i := 0
	for _, n := range ndcs {
		if i == 100 {
			break
		}
		fmt.Print(i)
		i++
		// confirm the NDC
		//TODO remap the ndc from 11 to newer format https://health.maryland.gov/phpa/OIDEOR/IMMUN/Shared%20Documents/Handout%203%20-%20NDC%20conversion%20to%2011%20digits.pdf
		resp, err := http.Get(url + n.NDC)
		if err != nil {
			panic(err)
		}
		body, err := io.ReadAll(resp.Body)
		if err != nil {
			panic(err)
		}

		err = json.Unmarshal(body, &ndcResponse)
		if err != nil {
			panic(err)
		}
		resp.Body.Close()
	}
}

func decodeStream(f string) {
	p := message.NewPrinter(language.English)

	start := time.Now()

	r, err := os.Open(f)
	if err != nil {
		panic(err)
	}
	fmt.Println("file opened")
	fmt.Println(time.Since(start))

	dec := json.NewDecoder(r)

	// read open bracket
	_, err = dec.Token()
	if err != nil {
		log.Fatal(err)
	}

	// while the array contains values
	i := 0
	for dec.More() {
		var ndc Ndc
		// decode an array value (Message)
		err := dec.Decode(&ndc)
		if err != nil {
			panic(err)
		}
		// write the ndc to a channel and process it in parallel

		i++
	}

	// read closing bracket
	_, err = dec.Token()
	if err != nil {
		panic(err)
	}
	p.Println(i)
}
func printSize(i int, p *message.Printer) string {

	var s string
	if i >= int(math.Pow10(6)) {
		f := float64(i) / math.Pow10(6)
		s = p.Sprintf("%.2f MB", f)
	} else if i >= 1000 {
		f := float64(i) / 1000
		s = p.Sprintf("%.2f KB", f)
	} else {
		s = p.Sprint(i, "B")
	}
	return s
}

// func asdf() {
// 	if false {
// 		meds := []string{"cosentyx", "trintellix", "cetirizine", "Lisinopril", "Amlodipine", "50580-726-03"}
// 		// conditions:=[]string{"psoriasis",""}
// 		url := "https://api.fda.gov/drug/label.json?search=indications_and_usage:"

// 		for _, v := range meds {
// 			if v[0] != '5' {
// 				continue
// 			}
// 			resp, err := http.Get(url + v)
// 			if err != nil {
// 				panic(err)
// 			}
// check response code
// 			defer resp.Body.Close()

// 			var res IndicationResponse
// 			body, err := io.ReadAll(resp.Body)
// 			if err != nil {
// 				panic(err)
// 			}

// 			err = json.Unmarshal(body, &res)
// 			if err != nil {
// 				panic(err)
// 			}
// 			fmt.Println(res.Meta.Results.Total)
// 			fmt.Println(res.Results[0].IndicationsAndUsage)
// 		}
// 		fmt.Println()
// 		fmt.Println()
// 	}

// 	if true {
// 		b, err := os.ReadFile("./ndc.json")
// 		if err != nil {
// 			panic(err)
// 		}

// 		var ndcs []Ndc
// 		json.Unmarshal(b, &ndcs)
// 		fmt.Println(ndcs[50])

// 		// go through graph NDCs and Match as many as possible to FDA NDC, search by NDC, then by name if no match is found
// 		url := "https://api.fda.gov/drug/ndc.json?search=product_ndc:"
// 		var ndcResponse NdcResponse
// 		// v := ndcs[50].NDC
// 		//82417-1063 works
// 		v := "0078-0639" //cosentyx
// 		// v := "82417-1063"

// 		fmt.Println(url + v)
// 		resp, err := http.Get(url + v)
// 		if err != nil {
// 			panic(err)
// 		}
// 		defer resp.Body.Close()
// 		body, err := io.ReadAll(resp.Body)
// 		if err != nil {
// 			panic(err)
// 		}

// 		err = json.Unmarshal(body, &ndcResponse)
// 		if err != nil {
// 			fmt.Println(ndcResponse)
// 			panic(err)
// 		}
// 		fmt.Println(ndcResponse.Meta.Results.Total)
// 		fmt.Println(ndcResponse.Results[0].BrandName)
// 	}
// }
