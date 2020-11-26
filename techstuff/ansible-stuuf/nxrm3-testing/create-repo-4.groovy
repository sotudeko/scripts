import groovy.json.JsonSlurper
import org.sonatype.nexus.repository.config.Configuration

args = '''{
    "remote_username": "admin",
    "remote_password": "admin123",
    "name": "pypi-proxy",
    "remote_url": "https://pypi.python.org/",
    "strict_content_validation": true,
    "blob_store": "pypi",
    "clean_policy": [ "PyPi-cleanup" ],
    "layout_policy": "strict",
    "write_policy": "allow", 
    "version_policy": "release"
}'''

rr = [
  "name": "string",
  "description": "string",
  "mode": "BLOCK",
  "matchers": [
    "string"
  ]
]

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
                        blobStoreName: parsed_args.blob_store,
                ],
                negativeCache: [
                        enabled: true,
                        timeToLive: 1440.0
                ]
        ]
)

repository.getRepositoryManager().create(configuration)

