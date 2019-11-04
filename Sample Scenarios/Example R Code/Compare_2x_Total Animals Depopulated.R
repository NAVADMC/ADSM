##########################################################################
#
# Title: Compare_2x_Total Animals Depopulated
#
# Author: Erin Campbell
# Date: 8/8/2018
# Update Date: 7/1/2019
# Update by: Schoenbaum Missy
# Notes: LOOK for boxes below to enter your scenario and working directory
#
# This script creates a boxplot comparing the number of animals depopulated between scenarios
# It was written to compare two scenarios, but more could be easily added
# It looks at the range of scenarios
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
scenarioname = "XXXX"
db1 = "C:/Users/meschoenbaum/Documents/ADSM Workspace/Sample Scenario with Outputs/Sample Scenario with Outputs.db"
db2 = "C:/Users/meschoenbaum/Documents/ADSM Workspace/demo425/demo425.db"


##############################################################################
####                completed setting directories          ####
##############################################################################
## connecting to databases

scenario1<- dbConnect(SQLite(), dbname= db1)
scenario2<- dbConnect(SQLite(), dbname= db2)

## Scenario 1

AnimalsDepo<-dbSendQuery(scenario1, statement = paste("SELECT iteration, day, last_day, descA",
                                                    "FROM  Results_dailybyproductiontype r",
                                                    "WHERE 1=1", 
                                                    "AND production_type_id is null",
                                                    "and last_day = 1",
                                                    "order by 1"))

AnimalDepo<-dbFetch(farmsDepo)


## Scenario 2

AnimalsDepo2<-dbSendQuery(scenario2, statement = paste("SELECT iteration, day, last_day, descA",
                                                     "FROM  Results_dailybyproductiontype r",
                                                     "WHERE 1=1", 
                                                     "AND production_type_id is null",
                                                     "and last_day = 1",
                                                     "order by 1"))

AnimalDepo2<-dbFetch(AnimalsDepo2)

## Master Table

AD<-rbind(AnimalDepo, AnimalDepo2)
AD$scenario<-c(rep("scenario1"),rep("scenario2"))

## Plotting Master Table

p<-qplot(scenario, descA, geom=c("boxplot"), data=AD,
         fill=scenario, main="Animals depopulated",
         xlab="", ylab="Animals")
p
