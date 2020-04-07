##########################################################################
#
# Title: Compare_2x_Total Animals Infected
#
# Author: Erin Campbell
# Date: 8/8/2018
# Update Date: 5/21/2019 Missy Schoenbaum
# Notes: LOOK for boxes below to enter your scenario and working directory
#
# This script creates a boxplot comparing the number of animals infected between scenarios
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

# Scenario1

TotalAnimalsInf1<-dbSendQuery(scenario1, statement = paste("SELECT iteration, day, last_day, infcA",
                                                         "FROM  Results_dailybyproductiontype r",
                                                         "WHERE 1=1", 
                                                         "AND production_type_id is null",
                                                         "and last_day = 1", "order by 1"))
TAnimalsInf1<-dbFetch(TotalAnimalsInf1)

#Scenario 2


TotalAnimalsInf2<-dbSendQuery(scenario2, statement = paste("SELECT iteration, day, last_day, infcA",
                                                         "FROM  Results_dailybyproductiontype r",
                                                         "WHERE 1=1", 
                                                         "AND production_type_id is null",
                                                         "and last_day = 1", "order by 1"))
TAnimalsInf2<-dbFetch(TotalAnimalsInf2)



#master table

TAI<-rbind(TAnimalsInf1,TAnimalsInf2)
TAI$scenario<-c(rep("scenario1"),rep("scenario2"))


#Plotting master table
p<-qplot(scenario, infcA, geom=c("boxplot"), data=TAI,
         fill=scenario, main="Total Animals Infected",
         xlab="", ylab="Units")
p

