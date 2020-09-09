package iqrestapi

// go install

import(
    "net/http"
    "io/ioutil"
    "log"
)

type Init struct {
    username string
    passwd string
    url string
}

func (iq *Init) GetData() []byte {

    var username string = iq.username
    var passwd string = iq.passwd

    client := &http.Client{}

    req, err := http.NewRequest("GET", iq.url, nil)
    req.SetBasicAuth(username, passwd)

    resp, err := client.Do(req)

    if err != nil{
        log.Fatal(err)
    }

    bodyText, err := ioutil.ReadAll(resp.Body)

    // body := string(bodyText)

    return bodyText
}



