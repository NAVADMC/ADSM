##########################################################################
# Title: Compare_2x_Epidemic CurveCompare
# Author: Erin Campbell
# Date: 7/17/2018
# Update Date: 5/21/19 Schoenbaum
# Notes: LOOK for boxes below to enter your scenario and working directory
# This script calculates the epi curve across all iterations in 2 scenarios and compares them on one plot
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
scenarioname = "XXXX"
db1 = "C:/Users/meschoenbaum/Documents/ADSM Workspace/Sample Scenario with Outputs/Sample Scenario with Outputs.db"
db2 = "C:/Users/meschoenbaum/Documents/ADSM Workspace/demo425/demo425.db"


##############################################################################
####                completed setting directories          ####
##############################################################################

#connecting to each scenario 

Scenario1 = dbConnect(SQLite(), dbname= db1)
Scenario2 = dbConnect(SQLite(), dbname= db2)



#Scenario 1

EpiCurve<-dbSendQuery(Scenario1, statement = paste("SELECT day, Sum(infnU), Sum(detnU)",
                                                          "FROM  Results_dailybyproductiontype r",
                                                          "WHERE 1=1","AND production_type_id is null",
                                                          "and last_day < 1","group by day","order by 1, 2"))
EpiCur<-dbFetch(EpiCurve)

Dur1<-dbSendQuery(Scenario1, statement = paste("SELECT max(outbreakduration)",
                                               "FROM  Results_dailycontrols",
                                               "WHERE last_day <> 0"))

Dur1fetch<-dbFetch(Dur1)

Dur1Fetchnum<-as.numeric(unlist(Dur1fetch))


#Scenario 2

EpiCurve2<-dbSendQuery(Scenario2, statement = paste("SELECT day, Sum(infnU), Sum(detnU)",
                                                         "FROM  Results_dailybyproductiontype r",
                                                         "WHERE 1=1","AND production_type_id is null",
                                                         "and last_day < 1","group by day","order by 1, 2"))
EpiCur2<-dbFetch(EpiCurve2)

Dur2<-dbSendQuery(Scenario2, statement = paste("SELECT max(outbreakduration)",
                                            "FROM  Results_dailycontrols",
                                            "WHERE last_day <> 0"))

Dur2fetch<-dbFetch(Dur2)

Dur2Fetchnum<-as.numeric(unlist(Dur2fetch))

#Creating variable scenario per table

EpiCur$scenario<-c(rep("Scenario1",Dur1Fetchnum))
EpiCur2$scenario<-c(rep("Scenario2",Dur2Fetchnum))
#use the number of rows that are in each scenario and your appropriate names

# Cast the varible into a new datatype

EpiCur$scenario<=as.numeric(as.character(EpiCur$scenario))
EpiCur2$scenario<=as.numeric(as.character(EpiCur2$scenario))


#Making Master Tables

EPICURVEMaster<-rbind(EpiCur,EpiCur2)
colnames(EPICURVEMaster)<-c("day", "sumInfnU", "sumdetnU","Scenario")

# Drawing epicurve

p<-ggplot(EPICURVEMaster,aes(x=day, y=sumInfnU, group="Scenario", colour=Scenario))+
  geom_line(size=1)+
  labs(title="Epidemic Curve Comparison",x="Time (days)", y = "New Infected Units")

dbDisconnect(Scenario1)
dbDisconnect(Scenario2)

p

