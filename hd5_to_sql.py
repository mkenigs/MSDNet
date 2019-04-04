from __future__ import print_function
import tables
import sqlalchemy
import pandas
import progressbar
import sys

import shared_functions
import settings

#TODO
def check_for_multiple_nrows():
    allf=shared_functions.get_all_files(settings.path)
    for f in allf:
        h5=tables.open_file(f)
        if h5.root.metadata.songs.nrows>0:
                print(f)
                h5.close()
                break
        h5.close()

if __name__ == "__main__":

    num_files = sum(1 for x in shared_functions.all_files_generator(settings.path))
    if settings.max<num_files:
        num_files=settings.max

    engine = sqlalchemy.create_engine('mysql://%s:%s@%s/%s' % (settings.user, settings.password, settings.host, settings.database), pool_recycle=3600)

    print("Converting ", num_files, " files to pandas tables:")
    bar = progressbar.ProgressBar(maxval=num_files, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    alllist=[]
    count = 1
    for f in shared_functions.all_files_generator(settings.path):
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
    all.to_sql("myPanda", engine, if_exists='replace')
    print("done.")