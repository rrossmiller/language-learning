package main

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
)

func main() {
	url := "https://api.fda.gov/drug/label.json?search=indications_and_usage%3Acosentyx"

	resp, err := http.Get(url)
	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()
	var res *Response

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		panic(err)
	}
	err = json.Unmarshal(body, &res)
	if err != nil {
		panic(err)
	}

	fmt.Println(res.Results[0].IndicationsAndUsage)
}
