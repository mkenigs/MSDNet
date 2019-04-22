#!/usr/bin/env python3
from __future__ import print_function
"""
Some code borrowed under this license:

Thierry Bertin-Mahieux (2010) Columbia University
tb2332@columbia.edu

This code query the musicbrainz database to get some information
like musicbrainz id and release years.
The databased in installed locally.

This is part of the Million Song Dataset project from
LabROSA (Columbia University) and The Echo Nest.


Copyright 2010, Thierry Bertin-Mahieux

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import glob

def all_files_generator(basedir,ext='.h5') :
    """
    From a root directory, go through all subdirectories
    and find all files with the given extension.
    Return all absolute paths in a list.
    """
    for root, dirs, files in os.walk(basedir):
        files = glob.glob(os.path.join(root,'*'+ext))
        for f in files :
            yield os.path.abspath(f)


import tables
import sqlalchemy
import pandas
import progressbar
import sys

import settings

# TODO remove
# def check_for_multiple_nrows():
#     allf=get_all_files(settings.path)
#     for f in allf:
#         h5=tables.open_file(f)
#         if h5.root.metadata.songs.nrows>0:
#                 print(f)
#                 h5.close()
#                 break
#         h5.close()

if __name__ == "__main__":

    num_files = sum(1 for x in all_files_generator(settings.path))
    if settings.max<num_files:
        num_files=settings.max

    engine = sqlalchemy.create_engine('mysql://%s:%s@%s/%s' % (settings.user, settings.password, settings.host, settings.database), pool_recycle=3600)

    print("Converting ", num_files, " files to pandas tables:")
    bar = progressbar.ProgressBar(maxval=num_files, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    alllist=[]
    count = 1
    for f in all_files_generator(settings.path):
        if count > num_files:
            break
        bar.update(count)
        count+=1
        h5file=tables.open_file(f)
        dfs = []
        for t in h5file.root._f_walknodes('Table'):
            df=pandas.DataFrame.from_records(t.read())
            dfs.append(df)

        pdf=pandas.concat(dfs, axis=1, join='inner', sort='False') #TODO could do all at once?
        alllist.append(pdf)
        h5file.close()

    bar.finish()
    print("Concatenating tables...", end="")
    all=pandas.concat(alllist)
    print("done.")
    print("Converting to sql...", end="")
    all.to_sql("megarelation", engine, if_exists='replace')
    print("done.")