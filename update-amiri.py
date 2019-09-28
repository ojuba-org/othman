#! /usr/bin/python3

import sys
import os
import sqlite3

#os.system("curl -sSL https://github.com/khaledhosny/quran-data/tarball/master | tar -C othman-data -xzf -")
#os.system("mv othman-data/khaledhosny-quran-data-* othman-data/quran-data")

UPDATE_SQL='UPDATE Quran SET othmani=? WHERE id=?'

db=sqlite3.connect("othman-data/quran.db")

#db.execute("BEGIN")
#db.execute("UPDATE Quran SET othmani=''")
#db.execute("COMMIT")
#exit(-1);

db.execute("BEGIN")
counter=1
for i in range(1, 115):
    with open("othman-data/quran-data/quran/{:03d}.txt".format(i), "r") as f:
        for line in f:
            line=line.strip()
            if not line: continue
            print(counter)
            db.execute(UPDATE_SQL, (line, counter))
            counter+=1
db.execute("COMMIT")
db.execute("VACUUM")

