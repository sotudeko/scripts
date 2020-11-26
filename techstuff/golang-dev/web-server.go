package main

import (
	"io"
	"net/http"
)

func main() {
	http.HandleFunc("/", handler)
    http.ListenAndServe(":3001", nil)
}

func handler (w http.ResponseWriter, r *http.Request) {
	io.WriteString(w, "Hello from handler")
}

