import groovy.json.JsonSlurper
import groovy.json.JsonOutput
import static groovy.json.JsonOutput.*
import static java.nio.charset.StandardCharsets.UTF_8


class IQApplications {

    static String repositoryUrl = 'http://localhost:8070'
    static String iqUserAndPassword = 'admin:admin123'
    static String iqSonatypeWorkDir = '/opt/nxiq/sonatype-work'

    static void main(String[] args) {

        def applicationsMap = getApplications()

        if (applicationsMap.size() == 0){
            println 'No applications found for Nexus IQ'
            System.exit(0)
        }

        def iqReportsDir = iqSonatypeWorkDir + '/clm-server/report'

        println()
        println('Nexus IQ Applications')
        println()

        if (!dirExists(iqReportsDir)){
            println 'Could not find sonatype workdir'
            System.exit(0)
        }

        File dir = new File(iqReportsDir)

        String[] applications = dir.list()
        int numberOfApplications = 0
 
        for (String applicationId : applications) {
            if (!applicationId.startsWith(".")){
                numberOfApplications++
                def applicationName = applicationsMap[applicationId].name 
                int numberOfReports = countApplicationReports(iqReportsDir + '/' + applicationId)

                println('name: ' + applicationName)
                println('  id: ' + applicationId )
                println('  number of reports (scans): ' + numberOfReports)
                reportDates(iqReportsDir + '/' + applicationId)
                println()
            }
        }

        println('Number of applications: ' + numberOfApplications)
        println()
    }

    static Boolean dirExists(dir){
        if (new File(dir).exists()){
            return true
        }
        else {
            return false
        }
    }

    static def countApplicationReports(applicationReportsDir){
        File dir = new File(applicationReportsDir)
        String[] reports = dir.list()
        int numberOfReports = 0

        for (String reportId : reports) {
            if (!reportId.startsWith(".")){
                numberOfReports++
            }
        }

        return numberOfReports
    }

    static reportDates(applicationReportsDir){
        File reportsDir = new File(applicationReportsDir)
        File[] reports = reportsDir.listFiles()

        def map = [:]

        for (File reportId : reports) {
            if (!reportId.getName().startsWith(".")){
                map[reportId.lastModified()] = [name: reportId.getName()]
            }
        }

        println('  reports: ')

        for (entry in map.sort{it.key}) {
            def timeMs = entry.key
            def fmt = new Date(timeMs).format('MMM dd yyyy hh:mm:ss')
            println "    $entry.value.name : $fmt [$timeMs]"
        }   
    }

    static getApplications(){
        def encoded = iqUserAndPassword.getBytes().encodeBase64().toString()
         
        def map = [:]

        def endpoint = repositoryUrl + '/api/v2/applications'

        def url = new URL(endpoint)
        def applicationsConnection = url.openConnection()

        applicationsConnection.requestMethod = 'GET'
        applicationsConnection.setRequestProperty("Authorization", "Basic $encoded")

        if (applicationsConnection.responseCode == 200) {
            def applicationsContent = applicationsConnection.content.text

            def jsonSlurper = new JsonSlurper()
            def applicationsJsonObject = jsonSlurper.parseText(applicationsContent)

            applicationsJsonObject.applications.each {
                //println JsonOutput.prettyPrint(JsonOutput.toJson(it))

                String applicationId = it.id
                String applicationName = it.name
                String contactName = it.contactUserName
                String publicId = it.publicId

                map[applicationId] = [name: applicationName, publicId: publicId, contactName: contactName]
            }
        }

        return map
    }

    static getApplications2(){
        def map = [:]

        def endpoint = repositoryUrl + '/api/v2/applications'

        def url = new URL(endpoint)
        def applicationsConnection = url.openConnection()

        applicationsConnection.requestMethod = 'GET'
        applicationsConnection.setRequestProperty("Authorization", "Basic YWRtaW46YWRtaW4xMjM=")

        if (applicationsConnection.responseCode == 200) {
            def applicationsContent = applicationsConnection.content.text

            def jsonSlurper = new JsonSlurper()
            def applicationsJsonObject = jsonSlurper.parseText(applicationsContent)

            applicationsJsonObject.applications.each {
                //println JsonOutput.prettyPrint(JsonOutput.toJson(it))

                String applicationId = it.id
                String applicationName = it.name
                String contactName = it.contactUserName
                String publicId = it.publicId

                map[applicationId] = [name: applicationName, publicId: publicId, contactName: contactName]
            }
        }

        return map
    }
}





