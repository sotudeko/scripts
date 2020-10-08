node {
   def mvnHome
   stage('Preparation') { // for display purposes
      // Get some code from a GitHub repository
      git 'https://bitbucket.org/ilkka_turunen/webgoat-example.git'
      // Get the Maven tool.
      // ** NOTE: This 'M3' Maven tool must be configured
      // **       in the global configuration.           
      mvnHome = tool 'M3'
   }
//   stage('Code Quality Scan') {
//       dir('./webgoat'){
//           sh "'${mvnHome}/bin/mvn' sonar:sonar -Dsonar.host.url=http://localhost:9000"
//       }
//   }
   stage('Build') {
      // Run the maven build
      
      dir('./webgoat') {
        // some block
        
        if (isUnix()) {
         echo pwd()
         sh "'${mvnHome}/bin/mvn' -Dmaven.test.failure.ignore clean package"
        } 
        else {
         bat(/"${mvnHome}\bin\mvn" -Dmaven.test.failure.ignore clean package/)
        }
      
      }
   }
//   stage('IQ scan') {
//         dir('./webgoat') {
//           sh "'java' -jar /opt/nexus-iq-cli/nexus-iq-cli-1.43.0-01.jar -i sampleapp -s http://localhost:8070 -a admin:admin123 ./target/WebGoat-5.4.4.3-SNAPSHOT.war"
//         }
//   }
   
   stage('IQ Scan with plugin'){
       nexusPolicyEvaluation failBuildOnNetworkError: false, iqApplication: 'webgoatci', iqStage: 'build', jobCredentialsId: ''
   }
   stage('IQ scan'){
       dir('./webgoat'){
           
        echo '----------------------------------'
        echo 'display scan results'
        echo '----------------------------------'
        def scan_op = sh(returnStdout: true, script: "'java' -jar /opt/nexus-iq-cli/nexus-iq-cli-1.43.0-01.jar -i webgoatci -s http://localhost:8070 -a admin:admin123 ./target/WebGoat-5.4.4.3-SNAPSHOT.war").trim()
        echo scan_op
        
        echo '----------------------------------'
        echo 'report url'
        echo '----------------------------------'
        def reportUrl = "f906eac532ed4bb0b26e2f99f382e4f2"
        
        echo '----------------------------------'
        echo 'display report'
        echo '----------------------------------'
        def scan_report = sh(returnStdout: true, script: "'curl' --silent -u admin:admin123 -X GET http://localhost:8070/api/v2/applications/webgoatci/reports/$reportUrl").trim()
        echo scan_report 
        
        //| 'python' '-m' 'json.tool'
        //reportUrl = sh(returnStdout: true, script: "echo -n $scan_op").trim() 
        //echo reportUrl
        //| grep 'The detailed report can be viewed online at'
       }
   }
}

