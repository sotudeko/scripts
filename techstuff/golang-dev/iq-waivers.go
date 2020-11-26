package main

import (
	"io/ioutil"
	"log"
	"net/http"
)

func main() {

	resp, err := http.Get("http://localhost:8070/api/v2/reports/components/waivers")

	if err != nil {
		log.Fatalln(err)
	}


	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)

	if err != nil {
		log.Fatalln(err)
	}

	log.Println(string(body))

}


// func handler (w http.ResponseWriter, r *http.Request) {
// 	io.WriteString(w, "Hello from handler")
// }

