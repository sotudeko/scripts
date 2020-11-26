package main

import(
    "fmt"
    "net/http"
    "io/ioutil"
    "log"
    //"encoding/json"
)

type ApplicationWaivers struct {
    ApplicationWaivers []ApplicationWaiver `json:"applicationWaivers"`     
}

type ApplicationWaiver struct {
    Contact string `json:"contactUserName"`
    Id string `json:"id"`
    Name string `json:"name"`
    OrganisationId string `json:"organizationId"`
    PublicId string `json:"publicId"`
    Stages []Stage `json:"stages"`
}

type Stage struct {
    ComponentPolicyViolations []ComponentPolicyViolation `json:"componentPolicyViolations"`
    StageId string `json:"stageId"`
}

type ComponentPolicyViolation struct {

}

func main(){
    body := getIQWaivers()
    fmt.Println(body)

    

    

}

func getIQWaivers() string {

    var username string = "admin"
    var passwd string = "admin123"

    client := &http.Client{}

    req, err := http.NewRequest("GET", "http://localhost:8070/api/v2/reports/components/waivers", nil)
    req.SetBasicAuth(username, passwd)

    resp, err := client.Do(req)

    if err != nil{
        log.Fatal(err)
    }

    bodyText, err := ioutil.ReadAll(resp.Body)

    body := string(bodyText)

    return body
}


