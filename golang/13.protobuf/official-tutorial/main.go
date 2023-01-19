package main

import (
	"addr/github.com/protocolbuffers/protobuf/examples/go/tutorial/pb"
	"fmt"
)

// https://protobuf.dev/getting-started/gotutorial/
func main() {
	x := pb.Person{
		Id:    1234,
		Name:  "John Doe",
		Email: "jdoe@example.com",
		Phones: []*pb.Person_PhoneNumber{
			{Number: "555-4321", Type: pb.Person_HOME},
		}}
	fmt.Printf("Id: %v\nName: %v\nEmail: %v\n  Number: %v\n  Type: %v\n", x.Id, x.Name, x.Email, x.Phones[0].Number, x.Phones[0].Type)

	// https://protobuf.dev/getting-started/gotutorial/#writing-a-message
}
