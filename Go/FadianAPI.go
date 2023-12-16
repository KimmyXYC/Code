package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"math/rand"
	"net/http"
	"net/url"
	"strings"
	"time"
)

type Response struct {
	Code int    `json:"code"`
	Data string `json:"data"`
}

func main() {
	sentencesData, err := ioutil.ReadFile("sentences.json")
	if err != nil {
		fmt.Println("Error reading sentences.json:", err)
		return
	}

	var sentences []string
	err = json.Unmarshal(sentencesData, &sentences)
	if err != nil {
		fmt.Println("Error parsing sentences.json:", err)
		return
	}

	http.HandleFunc("/api", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")

		params, _ := url.ParseQuery(r.URL.RawQuery)
		name := params.Get("name")

		rand.Seed(time.Now().UnixNano())
		randomIndex := rand.Intn(len(sentences))
		randomSentence := sentences[randomIndex]

		if name != "" {
			randomSentence = strings.Replace(randomSentence, "{name}", name, -1)
		}

		response := Response{
			Code: 0,
			Data: randomSentence,
		}

		responseJSON, err := json.Marshal(response)
		if err != nil {
			http.Error(w, "Internal Server Error", http.StatusInternalServerError)
			return
		}

		w.Write(responseJSON)
	})

	fmt.Println("Starting server at http://127.0.0.1:8888")
	err = http.ListenAndServe(":8888", nil)
	if err != nil {
		fmt.Println("Error starting server:", err)
	}
}
