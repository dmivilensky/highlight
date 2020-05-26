#!/bin/bash

while getopts ":l:p:s:d:" opt; do
  case $opt in
    l) login="$OPTARG"
    ;;
    p) pwd="$OPTARG"
    ;;
    s) sheets="$OPTARG"
    ;;
    d) docs="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
    ;;
  esac
done

PROJECT_DIR="$(dirname "$0")"

file="$PROJECT_DIR/../python_scripts/mail.ini"
echo "[Credentials]" > $file
echo "user=${login:-"example@gmail.com"}" >> $file
echo "pwd=${pwd:-"password"}" >> $file
cat $file

file1="$PROJECT_DIR/../python_scripts/google_addresses.ini"
echo "[Address]" > $file1
echo "sheets_id=${sheets:-"no?url?set"}" >> $file1
echo "docs_id=${docs:-"no?url?set?also"}" >> $file1
cat $file1