package main

import(
    "fmt"
    "net/http"
    "io/ioutil"
    "log"
    "encoding/json"
)

type Applications struct {
    Applications []Application `json:"applications"`     
}

type Application struct {
    Id string `json:"id"`
    Name string `json:"name"`
	PublicId string `json:"publicId:`
	OrganisationId string `json:"organizationId"`
}

type Report struct {
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

type ReportOutput struct {
  applicationName string
  component []ReportComponent
}

type ReportComponent struct {
    name string
    licenseStatus string
    securityStatus []string
}

func main(){
	body := getIQData("admin", "admin123", "http://localhost:8070/api/v2/applications")

	var applications Applications

    json.Unmarshal(body, &applications)
    
    fmt.Println("{")
    fmt.Println("  \"applications\": [")


	for i := 0; i < len(applications.Applications); i++ {

        applicationName := applications.Applications[i].Name
        fmt.Println("  ", "{")
        fmt.Println(opJson("    ", "application", applicationName))

        reportsJson := getIQData("admin", "admin123", "http://localhost:8070/api/v2/reports/applications")

        var reports []Report

        json.Unmarshal(reportsJson, &reports)

        for i := 0; i < len(reports); i++ {

            reportJson := getIQData("admin", "admin123", "http://localhost:8070/" + reports[i].ReportDataUrl);

            var components Components

            json.Unmarshal(reportJson, &components)

            for i := 0; i < len(components.Components); i++ {

                purl := components.Components[i].PackageUrl
                licenseStatus := components.Components[i].LicenseData.Status
                
                fmt.Println("      [")
                fmt.Println(opJson("    ", "component", purl))
                fmt.Println(opJson("    ", "licenseStatus ", licenseStatus))

                // for j := 0; j < len(components.Components[i].SecurityData.SecurityIssues); j++ {

                //     SecurityStatus := components.Components[i].SecurityData.SecurityIssues[j].Status
                //     SecurityReference := components.Components[i].SecurityData.SecurityIssues[j].Reference
                //     SecuritySeverity := components.Components[i].SecurityData.SecurityIssues[j].Severity
                //     fmt.Println("    - Security Status: " + SecurityStatus)
                //     fmt.Println("    Security Reference: " + SecurityReference)
                //     fmt.Println("    Security Severity: " + SecuritySeverity)
                // }
            }
        }

        fmt.Println("  ", "},")


    }
    
    fmt.Println("  ]")
    fmt.Println("}")
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

func opJson(indent, key, value string) string {
    return indent  +  "\"" + key + "\": \"" + value + "\","
}


