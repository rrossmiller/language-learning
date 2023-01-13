package main

import (
	"fmt"
	"log"
	"pbuf/pb"

	"google.golang.org/protobuf/proto"
)

func main() {
	rob := &pb.Person{Name: "Rob", Age: 28, FavFood: &pb.Food{Name: "Poutine", Country: "Canada"}}
	fmt.Println(rob)

	data, err := proto.Marshal(rob)

	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(data)
	fmt.Println()
	var newRob pb.Person
	err = proto.Unmarshal(data, &newRob)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("Name: %v, Age: %v, FavFood: {Name: %v, Country: %v}}", newRob.Name, newRob.Age, newRob.FavFood.Name, newRob.FavFood.Country)
}
