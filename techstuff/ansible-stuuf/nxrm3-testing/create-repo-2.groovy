import groovy.json.JsonSlurper
import org.sonatype.nexus.repository.config.Configuration

args = '''{
    "remote_username": "admin",
    "remote_password": "admin123",
    "name": "my-pypi-repo-200",
    "remote_url": "https://pypi.python.org/",
    "strict_content_validation": true,
    "blob_store": "pypi",
    "clean_policy": [ "PyPi-cleanup" ],
    "layout_policy": "strict",
    "write_policy": "allow", 
    "version_policy": "release"
}'''

parsed_args = new JsonSlurper().parseText(args)

configuration = new Configuration(
        repositoryName: parsed_args.name,
        recipeName: 'pypi-proxy',
        online: true,
        attributes: [
                proxy  : [
                        remoteUrl: parsed_args.remote_url,
                        contentMaxAge: 1440.0,
                        metadataMaxAge: 1440.0
                ],
                httpclient: [
                        blocked: false,
                        autoBlock: true,
                        connection: [
                                useTrustStore: false
                        ]
                ],
                storage: [
                        // writePolicy: parsed_args.write_policy.toUpperCase(),
                        blobStoreName: parsed_args.blob_store,
                        // strictContentTypeValidation: Boolean.valueOf(parsed_args.strict_content_validation)
                ],
                negativeCache: [
                        enabled: true,
                        timeToLive: 1440.0
                ],
                cleanup: [
                        policyName: parsed_args.clean_policy.toSet()
                ]
        ]
)

repository.getRepositoryManager().create(configuration)
