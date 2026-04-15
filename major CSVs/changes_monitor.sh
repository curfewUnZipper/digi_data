echo "timestamp,data..." > ec_log.csv
prev=""

while true; do
  ts=$(TZ=Asia/Kolkata date "+%H:%M:%S")
  curr=$(sudo hexdump -v -e '1/1 "%d "' /sys/kernel/debug/ec/ec0/io)

  if [ -n "$prev" ]; then
    echo "$curr" | awk -v t="$ts" -v p="$prev" '
    {
      split($0, a, " ");
      split(p, b, " ");
      printf "%s ", t;
      for (i=1; i<=length(a); i++) {
        if (a[i] != b[i]) {
          printf "[%d:%s->%s] ", i-1, b[i], a[i];
        }
      }
      printf "\n";
    }' | tee -a changes_monitor.csv
  fi

  prev="$curr"
  echo
  sleep 1
done
