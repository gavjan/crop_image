if [ ! -d input ]; then
  read -p "[ERROR] input folder is missing. Press enter to exit"
  exit 1
fi
if [ ! -d output ]; then
  mkdir output
fi
rm output/* 2> /dev/null

python3 crop.py
