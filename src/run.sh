if [ ! -d input ]; then
  read -p "[ERROR] input folder is missing. Press enter to exit"
  exit 1
fi
if [ ! -d output ]; then
  mkdir output
fi
rm output/* 2> /dev/null


ls -1 input | grep -E -o ".*\.(webp|jpeg|png|jfif)" | parallel convert input/{} input/{.}.jpg

## Sequential
#ls -1 ../input | grep -E -o ".*\.(webp|jpeg|png|jfif)" | while read line; do
#  line_no_extension="${line%%.*}"
#  convert ../input/"$line" ../input/"$line_no_extension".jpg
#done

rm input/*.png input/*.jpeg input/*.webp 2> /dev/null

python3 src/crop.py
