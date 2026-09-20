package main

import (
	"encoding/json"
	"fmt"
	"net/http"
)

type Item struct {
	ID   int    `json:"id"`
	Name string `json:"name"`
}

var items = []Item{
	{ID: 1, Name: "Item A"},
	{ID: 2, Name: "Item B"},
}

func itemsHandler(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case http.MethodPost:
		w.Header().Set("Content-Type", "application/json")

		var newItem Item
		err := json.NewDecoder(r.Body).Decode(&newItem)
		if err != nil {
			w.WriteHeader(http.StatusBadRequest)
			json.NewEncoder(w).Encode(map[string]string{"error": "Données invalides"})
			return
		}

		newItem.ID = len(items) + 1
		items = append(items, newItem)

		w.WriteHeader(http.StatusCreated)
		json.NewEncoder(w).Encode(newItem)
		fmt.Println("http.MethodPost")

	case http.MethodGet:
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(items)
		fmt.Println("http.MethodGet")

	default:
		w.WriteHeader(http.StatusMethodNotAllowed)
		w.Write([]byte("Méthode non autorisé"))
		fmt.Println("default")
	}
}

func main() {

	truc := test(1)

	fmt.Println(&truc)
	truc()

	truc = test(2)

	fmt.Println(&truc)
	truc()

	http.HandleFunc("/", itemsHandler)

	fmt.Println("Port 8080")
	http.ListenAndServe(":8080", nil)

}

func test(args int) func() {

	execute := func() {
		fmt.Println("test")
		fmt.Println(args)
	}

	return execute

}

/*
import json, requests

payload = {"ID": 3, "Name": "Item C"}
response = requests.post("http://localhost:8080", data=json.dumps(payload))
*/
