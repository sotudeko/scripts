import org.sonatype.nexus.repository.storage.Asset
import org.sonatype.nexus.repository.storage.StorageFacet
import org.joda.time.format.DateTimeFormat
import org.joda.time.format.DateTimeFormatter

def repo = repository.repositoryManager.get('maven-central')
File file = new File('assets-out.txt')

StorageFacet storageFacet = repo.facet(StorageFacet)

DateTimeFormatter dtf = DateTimeFormat.forPattern("MM/dd/yyyy HH:mm:ss")

def tx = storageFacet.txSupplier().get()

try {
    tx.begin()
    Iterable<Asset> assets = tx.browseAssets(tx.findBucket(repo))

    assets.forEach {
        println it.blobCreated
        log.info("${it}")
        file << it.name() + ': ' + dtf.print(it.blobCreated) + "\n"
    }
    println file.text
}
finally {
    tx.close()
}

