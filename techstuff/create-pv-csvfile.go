package main

import(
	"fmt"
    "net/http"
    "io/ioutil"
	"log"
	"strings"
	"encoding/json"
	"encoding/csv"
	"os"
)

type Policies struct {
	Policies []Policy `json:"policies"`
}

type Policy struct {
	Id string `json:"id"`
	Name string `json:"name"`
	OwnerId string `json:"ownerId"`
	PolicyType string `json:"policyType"`
}

type ApplicationViolations struct {
	ApplicationViolations []ApplicationViolation `json:"applicationViolations"`
}

type ApplicationViolation struct {
	Application Application `json:"application"`
	PolicyViolations []PolicyViolation `json:"policyViolations"`
}

type Application struct {
	Id string `json:"id"`
	PublicId string `json:"publicId"`
	Name string `json:"name"`
	OrganizationId string `json"organizationId"`
}

type PolicyViolation struct {
	PolicyId string `json:"policyId"`
	PolicyName string `json:"policyName"`
	OpenTime string `json:"openTime"`
	Component Component `json:"component"`
}

type Component struct {
	PackageUrl string `json:"packageUrl"`
}



func main(){

	var iqurl = os.Args[1]
	var iquser = os.Args[2]
	var iqpasswd = os.Args[3]

	var policyIdStr string
	
	policyIdStr = getPolicyIdsStr(iquser, iqpasswd, iqurl)
	
	
	getPolicyViolations(iquser, iqpasswd, iqurl, policyIdStr)
	
	makePolicyViolationsCsv()
	
}

func getPolicyIdsStr(username, passwd, url string) string {
	
	var iqapi = url + "/api/v2/policies"

	body := getData(username, passwd, iqapi)

	var policies Policies
	
	var  policyIdsStr string

	json.Unmarshal(body, &policies)

	for i := 0; i < len(policies.Policies); i++ {
		policyName := policies.Policies[i].Name
		policyId := policies.Policies[i].Id
		//ownerId := policies.Policies[i].OwnerId
		//policyType := policies.Policies[i].PolicyType

		//fmt.Println(policyName + "," + policyId + "," + ownerId  + "," + policyType)

		switch strings.ToLower(policyName) {
			case "security-critical": policyIdsStr = policyIdsStr + "p=" + policyId + "&"
			case "security-high": policyIdsStr = policyIdsStr + "p=" + policyId + "&"
			case "security-medium": policyIdsStr = policyIdsStr + "p=" + policyId + "&"		
		}
	}

	policyIdsStr = strings.TrimRight(policyIdsStr, "&")
	
	fmt.Println("Security policies string: " + policyIdsStr)
	
	return policyIdsStr
	
}

func getPolicyViolations(username, passwd, url, policyIds string) {
	
	var iqapi = url + "/api/v2/policyViolations?" + policyIds

	body := getData(username, passwd, iqapi)

	jsonFile := "policyviolations.json"

	err := ioutil.WriteFile(jsonFile, body, 0644)
	if err != nil {
        panic(err)
    }
	
	fmt.Println("Created file: " + jsonFile)
}


func makePolicyViolationsCsv(){

	var body []byte

	//homedir := os.Getenv("HOME")
	
	jsonFilePath := "policyviolations.json"
	csvFilePath := "policyviolations.csv"
	
	// initialise output file 
	csvFile, err := os.Create(csvFilePath)
	checkError("Cannot create output file", err)
	defer csvFile.Close()

	writer := csv.NewWriter(csvFile)

	header := []string{"PolicyName", "ApplicationName", "OpenTime", "Component"}
	err = writer.Write(header)
	checkError("Cannot write to file", err)

	// read inout json file
	jsonFile, err := os.Open(jsonFilePath)

	if err != nil {
		fmt.Println(err)
	}

	defer jsonFile.Close()
	body, _ = ioutil.ReadAll(jsonFile)

	var applicationViolations ApplicationViolations

	json.Unmarshal(body, &applicationViolations)

	for i := 0; i < len(applicationViolations.ApplicationViolations); i++ {
		
		publicId := applicationViolations.ApplicationViolations[i].Application.PublicId

		for j := 0; j < len(applicationViolations.ApplicationViolations[i].PolicyViolations); j++ {
			
			policyName := ""
			openTime := ""
			packageUrl := ""

			policyName = applicationViolations.ApplicationViolations[i].PolicyViolations[j].PolicyName
			openTime = applicationViolations.ApplicationViolations[i].PolicyViolations[j].OpenTime
			packageUrl = applicationViolations.ApplicationViolations[i].PolicyViolations[j].Component.PackageUrl

			csvLine := []string{policyName, publicId,  openTime, packageUrl}

			err = writer.Write(csvLine)
			checkError("Cannot write to file", err)

			writer.Flush()
		}
	}
	
	fmt.Println("Created file: " + csvFilePath)

}



func getData(username, passwd, url string) []byte {

    client := &http.Client{}

    req, err := http.NewRequest("GET", url, nil)
    req.SetBasicAuth(username, passwd)

    resp, err := client.Do(req)

    if err != nil{
        log.Fatal(err)
    }

    bodyText, err := ioutil.ReadAll(resp.Body)

    // body := string(bodyText)

    return bodyText
}

func checkError(message string, err error) {
    if err != nil {
        log.Fatal(message, err)
    }
}



