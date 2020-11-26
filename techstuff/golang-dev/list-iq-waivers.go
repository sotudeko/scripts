package main

import(
    "fmt"
    "net/http"
    "io/ioutil"
    "log"
    "encoding/json"
)

func main(){
    body := getWaivers()

    


    var result map[string]interface{}
    jsonData := []byte(body)
    json.Unmarshal(jsonData, &result)
    fmt.Println(result["applicationWaivers"])

    // jsonData := []byte(body)
    // json.Unmarshal(jsonData, &result)

    // w := result["applicationWaivers"].(map[string]interface{})
    // for k, v := range w {
    //     fmt.Println(k, v.(string))
    // }
    
    
    // fmt.Println(result["applicationWaivers"])

    // json.Unmarshal(jsonData, &v)
    // data := v.(map[string]interface{})

    // for d := range data {
    //     fmt.Println(string(d))
    //     fmt.Println("===========")
    // }

    // v := make(map[string](map[string]string))
    // json.Unmarshal(jsonData, &v)

    // log.Printf("INFO: jsonMap, %s", v)

    // applicationWaivers := v["applicationWaivers"]["stages"]
    // fmt.Println(applicationWaivers)

}

func getWaivers() string {

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


