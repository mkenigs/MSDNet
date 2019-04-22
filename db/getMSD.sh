#!/bin/bash
mkdir -p data
cd data
curl http://static.echonest.com/millionsongsubset_full.tar.gz > millionsongsubset_full.tar.gz
tar -C data -xzf millionsongsubset_full.tar.gz
cd ..
pip3 install -r requirements.txt
python3 hdf5_to_sql.py
mysql -u root -p -e normalizeMSD.sql