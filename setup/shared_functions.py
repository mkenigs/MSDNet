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
import hdf5_getters

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

def get_most_getters() :
    """
    get all getters except for get_num_songs. We assume that all we need is in hdf5_getters.py
    further assume that they have the form get_blablabla and that's the
    only thing that has that form
    """
    return filter(lambda x: x[:4] == 'get_' and x!='get_num_songs', hdf5_getters.__dict__.keys())