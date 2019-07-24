library(dplyr)
library(tidyr)

rm(list=ls())


inFile <- read.csv("/Users/ChatNoir/Google\ Drive/Herbiarum_Notes/MASTER_CatNumb_ImagesStayingAtLSU_FINAL_edited.csv",
                   stringsAsFactors=FALSE)


# Select the first column 
firstCol <- inFile %>% select(1)
# Remove empty rows
firstCol <- firstCol[!apply(firstCol == "", 1, all),]
# Get length of column 
len <- length(firstCol)
# Add column to new master data frame
masterDF <- as.data.frame(firstCol)
# Rename the first column 
masterDF$catalogNumber <- masterDF[,1]
# Add portal name to each barcode
masterDF$portalName <- rep("Vascular",len)
# Keep only main columns, don't save "firstCol"
masterDF <- subset(masterDF,select=c(catalogNumber,portalName))

# Turn this into a function 

addCol <- function(colNum,portal,mfdf,db){
  # Select the column 
  c <- db %>% select(colNum)
  # Remove empty rows
  c <- c[!apply(c == "", 1, all),]
  # Get length of column 
  len <- length(c)
  # Create new dataframe with column
  df <- as.data.frame(c)
  # Rename the first column 
  df$catalogNumber <- df[,1]
  # Add portal name to each barcode
  df$portalName <- rep(portal,len)
  # Keep only main columns, don't save "c"
  df <- subset(df,select=c(catalogNumber,portalName))
  # Merge with main dataframe
  mfdf <- rbind(mfdf,df)
  return(mfdf)
}


masterDF <- addCol(2,"Vascular",masterDF,inFile)
masterDF <- addCol(3,"Vascular",masterDF,inFile)
masterDF <- addCol(4,"Vascular",masterDF,inFile)
masterDF <- addCol(5,"Vascular",masterDF,inFile)
masterDF <- addCol(6,"Vascular",masterDF,inFile)
masterDF <- addCol(7,"Vascular",masterDF,inFile)
masterDF <- addCol(8,"Vascular",masterDF,inFile)
masterDF <- addCol(9,"Lichen",masterDF,inFile)
masterDF <- addCol(10,"Bryophyte",masterDF,inFile)
masterDF <- addCol(11,"Algae",masterDF,inFile)
masterDF <- addCol(12,"Fungi",masterDF,inFile)

write.csv(masterDF, file="/Users/ChatNoir/Projects/HerbariumRA/MasterPortalList/masterDF_july24.csv")
