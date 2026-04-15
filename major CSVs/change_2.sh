echo -n "time" > ec_log.csv
for i in $(seq 0 255); do echo -n ",b$i" >> ec_log.csv; done
echo "" >> ec_log.csv

prev=""

while true; do
  ts=$(TZ=Asia/Kolkata date "+%H:%M:%S")
  curr=$(sudo hexdump -v -e '1/1 "%u "' /sys/kernel/debug/ec/ec0/io)

  echo "$curr" | awk -v t="$ts" -v p="$prev" '
  {
    split($0, a, " ");
    split(p, b, " ");

    printf "%s", t;

    for (i=1; i<=length(a); i++) {
      if (p == "") {
        change = 0;
      } else {
        change = a[i] - b[i];
      }
      printf ",%d(%d)", a[i], change;
    }
    printf "\n";
  }' | tee -a ec_log.csv

  prev="$curr"
  echo
  sleep 1
done 
