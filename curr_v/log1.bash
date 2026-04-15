echo "time,current_A,voltage_V,power_W" > battery_log.csv

while true; do
  ts=$(date "+%H:%M:%S")

  curr=$(cat /sys/class/hwmon/hwmon2/curr1_input)
  volt=$(cat /sys/class/hwmon/hwmon2/in0_input)

  curr_A=$(awk "BEGIN {print $curr/1000000}")
  volt_V=$(awk "BEGIN {print $volt/1000000}")
  power_W=$(awk "BEGIN {print $curr_A * $volt_V}")

  echo "$ts,$curr_A,$volt_V,$power_W" | tee -a battery_log.csv

  sleep 1
done
