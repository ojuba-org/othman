#!/bin/sh

quran_path=$1
[ -n "$quran_path" ] || quran_path="quran/quran"

id=1
sura=1

echo "PRAGMA foreign_keys=OFF;"
echo "BEGIN TRANSACTION;"

while [ $sura -le 114 ]; do
  ayah=1
  sura_file="$quran_path/$(printf '%03d' $sura).txt"
  total_ayat=$(wc -l $sura_file | cut -d\  -f1)

  while [ $ayah -le $total_ayat ]; do
    text=$(head -n $ayah $sura_file | tail -n 1)
    echo UPDATE Quran SET othmani=\'$text\' WHERE id=$id\;

    ayah=$(expr $ayah + 1)
    id=$(expr $id + 1)
  done

  sura=$(expr $sura + 1)
done

echo "COMMIT;"
