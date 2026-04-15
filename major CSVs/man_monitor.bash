echo "timestamp,data..." > ec_log.csv
while true; do
  ts=$(TZ=Asia/Kolkata date "+%H:%M:%S")
  sudo hexdump -v -e '1/1 "%d "' /sys/kernel/debug/ec/ec0/io | \
  awk -v t="$ts" '{print t, $0}' | tee -a ec_log.csv
  echo

  sleep 1
done
