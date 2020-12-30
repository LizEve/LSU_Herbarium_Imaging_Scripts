#!/bin/bash
# Set error log for debugging
elog=/mnt/c/Users/Image/Documents/GitHub/LSU_Herbarium_Imaging_Scripts/WorkflowScriptsWS2/Debugging/MoveLocalImages.log
# Write date to error log 
echo "$(date)" &>> $elog
# Path to your python script 
python3.8 /mnt/c/Users/Image/Documents/GitHub/LSU_Herbarium_Imaging_Scripts/WorkflowScriptsWS2/MoveLocalImages.py -l "local_ws2.txt" &>> $elog

#python3.8 /mnt/c/Users/Image/Documents/GitHub/LSU_Herbarium_Imaging_Scripts/WorkflowScriptsWS2/MoveLocalImages.py -l "local_ws2.txt" -d "/mnt/e/CFLA-LSU-Station2/LSUCollections/" &>> $elog

# Add extra wait time, a probably unneeded 
sleep 5m