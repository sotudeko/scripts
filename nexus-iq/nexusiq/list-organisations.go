package main

import(
    "fmt"
    "net/http"
    "io/ioutil"
    "log"
    "encoding/json"
    // iqrestapi "golang-iqdev/IQRestApi"
)

type Organizations struct {
    Organizations []Organization `json:"organizations"`     
}

type Organization struct {
    Id string `json:"id"`
    Name string `json:"name"`
    Tags []Tag `json:"tags"`
}

type Tag struct {
    Color string `json:"color"`
	Description string `json:"description"`
	Id string `json:"id"`
    Name string `json:"name"`
}

func main(){
	// body := iqrestapi.Init{"admin", "admin123", "http://localhost:8070/api/v2/organizations"}
    body := getIQData("admin", "admin123", "http://localhost:8070/api/v2/organizations")

	var organizations Organizations

	json.Unmarshal(body, &organizations)

	for i := 0; i < len(organizations.Organizations); i++ {
		fmt.Println("Organization:")
		fmt.Println("  name:" + organizations.Organizations[i].Name)
		fmt.Println("  id:" + organizations.Organizations[i].Id)
		fmt.Println("  tags:")

		for j := 0; j < len(organizations.Organizations[i].Tags); j++ {
			fmt.Println("    id:" + organizations.Organizations[i].Tags[j].Id)
			fmt.Println("    name:" + organizations.Organizations[i].Tags[j].Name)
			fmt.Println("    description:" + organizations.Organizations[i].Tags[j].Description)
			fmt.Println("    color:" + organizations.Organizations[i].Tags[j].Color)
			fmt.Println("    ---")
		}
	}
}

func getIQData(username, passwd, url string) []byte {

    // var username string = "admin"
    // var passwd string = "admin123"

    client := &http.Client{}

    req, err := http.NewRequest("GET", url, nil)
    req.SetBasicAuth(username, passwd)

    resp, err := client.Do(req)

    if err != nil{
        log.Fatal(err)
    }

    bodyText, err := ioutil.ReadAll(resp.Body)

    return bodyText
}
