#!/bin/bash

OAI_INSTANCES=1
PHONE_INSTANCES=1
OUTPUT_PORT=12345
BUILD_PATH="/var/www/public/mi/MI-eNB/cmake_targets/lte_build_oai/build/"
OAI_PATH="/var/www/"

echo "Chaning to the LTE Build directory...";

cd $BUILD_PATH;

echo "Starting OAI Instances...";

for ((i = 0; i < $OAI_INSTANCES; i++))
do
    ENODEB=1 sudo -E ./lte-softmodem -O $OAI_PATH/OAI_config.conf --basicsim --noS1 | nc -l $OUTPUT_PORT
done & 

echo "Starting device simulators..." &

for ((j = 0; j < $PHONE_INSTANCES; j++))
do
    sudo -E ./lte-uesoftmodem -C 2350000000 -r 25 --ue-rxgain 125 --basicsim --noS1 > simulator_$j.txt
done &

echo "Finished";



# echo "" &

# nc -l localhost $OUTPUT_PORT > 12345.txt &

# echo "Port 1" &

# nc -l localhost 12346 > 12346.txt &

# echo "Port 2";


# echo "Start";

# for ((i = 0; i < $OAI_INSTANCES; i++))
# do
#     echo "Hello!"
# done &

# echo "Finished"
