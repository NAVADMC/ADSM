##########################################################################
#
# Title: Compare_2x_Total Units Infected
#
# Author: Erin Campbell
# Date: 7/18/2018
# Update Date: 5/21/2019 Schoenbaum
# Notes: LOOK for boxes below to enter your scenario and working directory
#
# This script creates a boxplot comparing the number units infected between scenarios
# It was written to compare two scenarios, but more could be easily added
# It looks at the range of scenarios
#
##############################################################################


#install.packages("RSQLite")
#install.packages("ggplot2")
#install.packages("bit")

library(RSQLite)
library(ggplot2)


##############################################################################
#                     set directories and database here                 #
##############################################################################

directory = "C:/Users/meschoenbaum//Documents/ADSM Workspace/"
ADSMWorkspace = "C:/Users/meschoenbaum//Documents/ADSM Workspace"
db1 = "C:/Users/meschoenbaum/Documents/ADSM Workspace/Sample Scenario with Outputs/Sample Scenario with Outputs.db"
db2 = "C:/Users/meschoenbaum/Documents/ADSM Workspace/NoZones/NoZones.db"


##############################################################################
####                completed setting directories          ####
##############################################################################


## connecting to databases

scenario1<- dbConnect(SQLite(), dbname= db1)
scenario2<- dbConnect(SQLite(), dbname= db2)

  # Scenario1
  
  TotalUnitsInf1<-dbSendQuery(scenario1, statement = paste("SELECT iteration, day, last_day, infcU",
                                                                "FROM  Results_dailybyproductiontype r",
                                                                "WHERE 1=1", 
                                                                "AND production_type_id is null",
                                                                "AND last_day = 1", "order by 1"))
  TUnitsInf1<-dbFetch(TotalUnitsInf1)
 
  #Scenario 2
  

  
  TotalUnitsInf2<-dbSendQuery(scenario2, statement = paste("SELECT iteration, day, last_day, infcU",
                                                               "FROM  Results_dailybyproductiontype r",
                                                               "WHERE 1=1", 
                                                               "AND production_type_id is null",
                                                               "AND last_day = 1", "order by 1"))
  TUnitsInf2<-dbFetch(TotalUnitsInf2)
  

  
  #master table
  
  TUI<-rbind(TUnitsInf1,TUnitsInf2)
  TUI$scenario<-c(rep("scenario1"),rep("scenario2"))
  
  
  #Plotting master table
  p<-qplot(scenario, infcU, geom=c("boxplot"), data=TUI,
            fill=scenario, main="Total Units Infected",
            xlab="", ylab="Units")
  p
  
  