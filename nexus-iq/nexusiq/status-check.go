package main

import(
    "fmt"
    "net/http"
    "io/ioutil"
    "log"
    "encoding/json"
)

type Application struct {
    ApplicationId string `json:"applicationId"`
    ReportDataUrl string `json:"reportDataUrl"`
		Stage string `json:"stage:`
}

type Components struct {
	Components []Component `json:"components"`
}

type Component struct {
	Hash string `json:"hash"`
	PackageUrl string `json:"packageUrl"`
	LicenseData LicenseData
	SecurityData SecurityData
}

type LicenseData struct {
	Status string `json:"status"`
}

type SecurityData struct {
	SecurityIssues []SecurityIssue `json:"securityIssues"`
}

type SecurityIssue struct {
	Status string `json:"status"`
	Reference string `json:"reference"`
	Severity string `json:"severity"`
}

type OutputStatus struct {
	ApplicationName string
	Component []Component
	LicenseStatus string
	SecurityStatus []string
}



func main(){
	appsJson := getIQData("admin", "admin123", "http://localhost:8070/api/v2/reports/applications")

	var applications []Application

	json.Unmarshal(appsJson, &applications)

	for i := 0; i < len(applications); i++ {

		//fmt.Println("Application:")
    //fmt.Println("  id:" + applications[i].ApplicationId)
    //fmt.Println("  stage:" + applications[i].Stage)
		//fmt.Println("  reportDataUrl:" + applications[i].ReportDataUrl)

		applicationName := applications[i].ReportDataUrl
		fmt.Println("Application:" + applicationName)

	  reportJson := getIQData("admin", "admin123", "http://localhost:8070/" + applications[i].ReportDataUrl);

    var components Components

		json.Unmarshal(reportJson, &components)

		for i := 0; i < len(components.Components); i++ {
			//fmt.Println("hash: " + components.Components[i].Hash)
			//fmt.Println("purl: " + components.Components[i].PackageUrl)
			//fmt.Println("license status: " + components.Components[i].LicenseData.Status)

			purl := components.Components[i].PackageUrl
			licenseStatus := components.Components[i].LicenseData.Status
			fmt.Println("  Component: " + purl)
			fmt.Println("    License Status: " + licenseStatus)

			for j := 0; j < len(components.Components[i].SecurityData.SecurityIssues); j++ {
				//fmt.Println("security status: " + components.Components[i].SecurityData.SecurityIssues[j].Status)

				SecurityStatus := components.Components[i].SecurityData.SecurityIssues[j].Status
				SecurityReference := components.Components[i].SecurityData.SecurityIssues[j].Reference
				SecuritySeverity := components.Components[i].SecurityData.SecurityIssues[j].Severity
				fmt.Println("    - Security Status: " + SecurityStatus)
				fmt.Println("    Security Reference: " + SecurityReference)
				fmt.Println("    Security Severity: " + SecuritySeverity)
			}

			fmt.Println("")
		}
	}
}

func getIQData(username, passwd, url string) []byte {

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


