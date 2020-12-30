#!/bin/bash
# Set error log for debugging
elog=/mnt/c/Users/Image/Documents/GitHub/LSU_Herbarium_Imaging_Scripts/WorkflowScriptsWS2/Debugging/MoveLocalImages.log
# Write date to error log 
echo "$(date)" &>> $elog
# Set variables 
outLogsuffix="local_ws1.txt"
sourceFolder='/mnt/c/Users/Image/Desktop/Imaging/'
destinationFolder='/mnt/Collection/sparklefarts/'
#destinationFolder="/mnt/e/CFLA-LSU-Station2/LSUCollections/"
barcodeMax=15
barcodeMin=9
csvFolder='/mnt/c/Users/Image/Desktop/Imaging/LocalLogs/'
portalFolders="Algae,Bryophyte,Fungi,Lichen,Vascular"
otherFolders="Random"

# Path to your python script 
#python3.8 /mnt/c/Users/Image/Documents/GitHub/LSU_Herbarium_Imaging_Scripts/WorkflowScriptsWS2/MoveLocalImages.py -l "local_ws2.txt" &>> $elog
#python3.8 /mnt/c/Users/Image/Documents/GitHub/LSU_Herbarium_Imaging_Scripts/WorkflowScriptsWS2/MoveLocalImages.py -l "local_ws2.txt" -d "/mnt/e/CFLA-LSU-Station2/LSUCollections/" &>> $elog
#python3.8 /mnt/c/Users/Image/Documents/GitHub/LSU_Herbarium_Imaging_Scripts/WorkflowScriptsWS2/MoveLocalImages.py -l $outLogsuffix -s $sourceFolder -d $destinationFolder -x $barcodeMax -n $barcodeMin -c $csvFolder &>> $elog
python3.8 /mnt/c/Users/Image/Documents/GitHub/LSU_Herbarium_Imaging_Scripts/WorkflowScriptsWS2/MoveLocalImages.py -l $outLogsuffix -s $sourceFolder -d $destinationFolder -p $portalFolders -o $otherFolders -x $barcodeMax -n $barcodeMin -c $csvFolder &>> $elog


# Add extra wait time, a probably unneeded 
sleep 5m