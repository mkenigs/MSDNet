#!/bin/bash
cd data
curl https://labrosa.ee.columbia.edu/millionsong/sites/default/files/AdditionalFiles/mxm_dataset.db > mxm_dataset.db
sqlite3 mxm_dataset.db -cmd ".output mxm.sql" ".dump"
patch mxm.sql ../mxm.patch
mysql -u root -p -e "source mxm.sql"