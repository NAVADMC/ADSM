##########################################################################
#
# Title: Compare_2x_Total Units Depopulated
#
# Author: Erin Campbell
# Date: 7/18/2018
# Update Date: 5/21/2019 Missy Schoenbaum
# Notes: LOOK for boxes below to enter your scenario and working directory
#
# This script creates a boxplot comparing the number of farms depopulated between scenarios
# It was written to compare two scenarios, but more could be easily added
# It looks at the range of scenarios
#
##############################################################################


#install.packages("RSQLite")
#install.packages("ggplot2")

library(RSQLite)
library(ggplot2)


##############################################################################
#                     set directories and database here                 #
##############################################################################

directory = "C:/Users/meschoenbaum//Documents/ADSM Workspace/"
ADSMWorkspace = "C:/Users/meschoenbaum//Documents/ADSM Workspace"
db1 = "C:/Users/meschoenbaum/Documents/ADSM Workspace/Sample Scenario with Outputs/Sample Scenario with Outputs.db"
db2 = "C:/Users/meschoenbaum/Documents/ADSM Workspace/demo425/demo425.db"


##############################################################################
####                completed setting directories          ####
##############################################################################


## connecting to databases

scenario1<- dbConnect(SQLite(), dbname= db1)
scenario2<- dbConnect(SQLite(), dbname= db2)

## Scenario 1

farmsDepo<-dbSendQuery(scenario1, statement = paste("SELECT iteration, day, last_day, descU",
                                                           "FROM  Results_dailybyproductiontype r",
                                                           "WHERE 1=1", 
                                                           "AND production_type_id is null",
                                                           "and last_day = 1",
                                                           "order by 1"))

FarmDepo<-dbFetch(farmsDepo)

#Scenario 2

farmsDepo<-dbSendQuery(scenario2, statement = paste("SELECT iteration, day, last_day, descU",
                                                          "FROM  Results_dailybyproductiontype r",
                                                          "WHERE 1=1", 
                                                          "AND production_type_id is null",
                                                          "and last_day = 1",
                                                          "order by 1"))

FarmDepo2<-dbFetch(farmsDepo)

# Master Table

FD<-rbind(FarmDepo,FarmDepo2)
FD$scenario<-c(rep("scenario1",Dur1Fetchnum),rep("scenario2",Dur2Fetchnum))

#Farms depopulated
p<-qplot(scenario, descU, geom=c("boxplot"), data=FD,
          fill=scenario, main="Farms depopulated",
          xlab="", ylab="Units")
p