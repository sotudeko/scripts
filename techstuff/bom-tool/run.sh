#!/bin/bash

java -jar bom-client-1.4.jar --iqPassword admin123 --iqUsername admin --iqUrl http://localhost:8070 --lifecycleStage build --organizationIds WebGoat --reportFileName bom.out --reportingUsername admin
