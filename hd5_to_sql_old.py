#!/usr/bin/env python

import shared_functions
import hdf5_getters
import sys
import mysql.connector
import numpy
import pandas

def createMegarelation(h5, mycursor):
    nSongs = hdf5_getters.get_num_songs(h5)
    types={type(hdf5_getters.get_track_id(h5))}
    typeDict = { numpy.ndarray:"TEXT", numpy.int32:"INT", numpy.string_:"TEXT", numpy.float64:"DOUBLE PRECISION"}
    replaceDict = { numpy.ndarray:"\'%s\'", numpy.int32:"%s", numpy.string_:"\'%s\'", numpy.float64:"%s"}
    createAttrs="track_id VARCHAR(40) PRIMARY KEY"
    insertAttrs="track_id"
    percentS="\'%s\'"
    songidx=0
    for getter in mostGetters:
        numpyType=type( hdf5_getters.__getattribute__(getter)(h5,songidx))
        if numpyType!=numpy.ndarray:
            sqlType = typeDict[numpyType] if numpyType in typeDict else "TEXT"
            percentForType = replaceDict[numpyType] if numpyType in typeDict else "\'%s\'"

            if getter[4:] in ["release", "key"]:
                createAttrs +=", "+getter[4:]+"_attr "
                insertAttrs +=", "+getter[4:]+"_attr"
            else:
                createAttrs+=", " + getter[4:] + " "# don't want leading get_
                insertAttrs+=", " + getter[4:]
            
            createAttrs+=sqlType
            percentS+=", "+percentForType
    h5.close()

    mycursor.execute("CREATE TABLE megarelation2 (" + createAttrs + ")")

    return (insertAttrs, percentS)

if __name__ == '__main__':
    if len(sys.argv)<2:
        sys.exit(0) # should die with usage
    allh5files = shared_functions.all_files_generator(sys.argv[1],ext='.h5')
    mostGetters = shared_functions.get_most_getters()
    mostGetters.remove("get_track_id")
    mdsdb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="INGlkYT8jn1pEWPP3o$ANvO4O70eaH!3OClDBi3BtDczG$$%$xnr3rM&7B1wU5csiA1LBo!PyAF%^7&gbQu1rTP8PUGR8alJEZmc",
        database="msd"
    )

    mycursor = mdsdb.cursor()

    # insertAttrs = "track_id, "
    # percentS = "\'%s\', "
    # for getter in mostGetters:
    #     if getter[4:] in ["release", "key"]:
    #         insertAttrs +=getter[4:]+"_attr "
    #     else:
    #         insertAttrs+=getter[4:]
    #     percentS+="%s"
    #     if getter != mostGetters[-1]:
    #         insertAttrs+=", "
    #         percentS+=", "

    mycursor.execute("DROP TABLE IF EXISTS megarelation2")
    (insertAttrs, percentS)=createMegarelation(hdf5_getters.open_h5_file_read("millionsongsubset_full/MillionSongSubset/data/A/A/A/TRAAABD128F429CF47.h5"), mycursor)

    for f in allh5files:
        h5 = hdf5_getters.open_h5_file_read(f) 
        nSongs = hdf5_getters.get_num_songs(h5)
        for songidx in xrange(nSongs):
            insertList=[hdf5_getters.get_track_id(h5)]
            for getter in mostGetters:
                attr = hdf5_getters.__getattribute__(getter)(h5,songidx)
                if type(attr)!=numpy.ndarray:
                    if pandas.isnull(attr):
                        attr="NULL"
                    if type(attr)==numpy.string_:
                        if attr.find("\'")!=-1:
                            attr=attr.replace("\'", "\\\'")
                    insertList.append(attr)

        insertCom = "INSERT INTO megarelation2 (" + insertAttrs + ") VALUES (" + percentS + ")"

        com = insertCom % tuple(insertList)
        mycursor.execute(com)

        h5.close()
    mdsdb.commit()


