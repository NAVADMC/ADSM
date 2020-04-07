##########################################################################
#
# Title: Compare_2x_Outbreak Duration Boxplot
#
# Author: Erin Campbell
# Date: 7/17/2018
# Update Date: 5/21/2019 Schoenbaum
# Notes: LOOK for boxes below to enter your scenario and working directory
#
# This script creates a boxplot comparison for outbreak duration across different scenarios
# Feel free to add additional scenarios following this example
##############################################################################


#install.packages("RSQLite")
#install.packages("ggplot2")

library(RSQLite)
library(ggplot2)


##############################################################################
######         set directories here        ######
##############################################################################

directory = "C:/Users/meschoenbaum//Documents/ADSM Workspace/"
ADSMWorkspace = "C:/Users/meschoenbaum//Documents/ADSM Workspace"
db1 = "C:/Users/meschoenbaum/Documents/ADSM Workspace/Sample Scenario with Outputs/Sample Scenario with Outputs.db"
db2 = "C:/Users/meschoenbaum/Documents/ADSM Workspace/demo425/demo425.db"


##############################################################################
####               completed setting directories                      ####
##############################################################################


  ## connecting to databases

  scenario1<- dbConnect(SQLite(), dbname= db1)
  scenario2<- dbConnect(SQLite(), dbname= db2)

  ##Scenario 1
  
  OutbreakDuration <- dbSendQuery(scenario1, statement = paste("SELECT iteration, outbreakduration",
                                                                      "FROM  Results_dailycontrols r",
                                                                      "WHERE 1=1",
                                                                      "AND last_day >0","order by 1"))
  OutDur<-dbFetch(OutbreakDuration)
  
  Dur1<-dbSendQuery(scenario1, statement = paste("SELECT max(iteration)",
                                           "FROM  Results_dailycontrols",
                                           "WHERE last_day <> 0"))
  Dur1fetch<-dbFetch(Dur1)
  
  
  Dur1Fetchnum<-as.numeric(unlist(Dur1fetch))
  
  
  ##Scenario 2 
  
  OutbreakDuration1 <- dbSendQuery(scenario2, statement = paste("SELECT iteration, outbreakduration",
                                                                     "FROM  Results_dailycontrols r",
                                                                     "WHERE 1=1",
                                                                     "AND last_day >0","order by 1"))
  OutDur2<-dbFetch(OutbreakDuration1)
  
  
  Dur2<-dbSendQuery(scenario2, statement = paste("SELECT max(iteration)",
                                                 "FROM  Results_dailycontrols",
                                                 "WHERE last_day <> 0"))
  Dur2fetch<-dbFetch(Dur2)
  
  Dur2Fetchnum<-as.numeric(unlist(Dur2fetch))
  
  ##Creating master table
  
  OUTBREAKDUR<-rbind(OutDur,OutDur2)
  OUTBREAKDUR$scenario<-c(rep("Scenario 1",Dur1Fetchnum),rep("Scenarrio 2",Dur2Fetchnum))
  
  ##Creating Boxplot
  
  p<-qplot(scenario, outbreakDuration, geom=c("boxplot"), data=OUTBREAKDUR,
            fill=scenario, main="Outbreak Duration Comparison",
            xlab="", ylab="Duration (days)")
  p

  