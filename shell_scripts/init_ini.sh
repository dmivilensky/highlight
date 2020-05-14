#!/bin/bash

while getopts ":l:p:" opt; do
  case $opt in
    l) login="$OPTARG"
    ;;
    p) pwd="$OPTARG"
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