#!/bin/bash

echo "================ SYSTEM MONITOR ================"

# -------- CPU TEMPERATURE --------
echo -e "\n[CPU Temperature]"
for zone in /sys/class/thermal/thermal_zone*; do
    if [ -f "$zone/temp" ]; then
        temp=$(cat $zone/temp)
        echo "$(basename $zone): $((temp/1000))°C"
    fi
done

# -------- FAN SPEED --------
echo -e "\n[Fan Speeds]"
found_fan=0
for hw in /sys/class/hwmon/hwmon*; do
    for fan in $hw/fan*_input; do
        if [ -f "$fan" ]; then
            echo "$(basename $hw) $(basename $fan): $(cat $fan) RPM"
            found_fan=1
        fi
    done
done
[ $found_fan -eq 0 ] && echo "No fan data available"

# -------- VOLTAGE --------
echo -e "\n[Voltages]"
found_volt=0
for hw in /sys/class/hwmon/hwmon*; do
    for v in $hw/in*_input; do
        if [ -f "$v" ]; then
            val=$(cat $v)
            echo "$(basename $hw) $(basename $v): $val mV"
            found_volt=1
        fi
    done
done
[ $found_volt -eq 0 ] && echo "No voltage data available"

# -------- CURRENT --------
echo -e "\n[Currents]"
found_curr=0
for hw in /sys/class/hwmon/hwmon*; do
    for c in $hw/curr*_input; do
        if [ -f "$c" ]; then
            val=$(cat $c)
            echo "$(basename $hw) $(basename $c): $val mA"
            found_curr=1
        fi
    done
done
[ $found_curr -eq 0 ] && echo "No current data available"

# -------- GPU TEMPERATURE --------
echo -e "\n[GPU Temperature]"

# NVIDIA
if command -v nvidia-smi &> /dev/null; then
    nvidia-smi --query-gpu=temperature.gpu,fan.speed --format=csv,noheader,nounits
else
    echo "NVIDIA GPU not detected or nvidia-smi missing"
fi

# AMD / Intel fallback
for hw in /sys/class/drm/card*/device/hwmon/hwmon*; do
    if [ -f "$hw/temp1_input" ]; then
        temp=$(cat $hw/temp1_input)
        echo "$(basename $hw): $((temp/1000))°C"
    fi
done

echo -e "\n==============================================="
