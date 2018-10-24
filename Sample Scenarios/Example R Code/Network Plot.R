##########################################################################
#
# Title: Network Plot - exposures
#
# Author: Erin Campbell
# Date: 7/26/2018
# Update Date: 10/4/2018 Matt review
# Notes: LOOK for boxes below to enter your scenario and working directory

#
# This script creates a network plot, which allow to compare the contact structure of the infection dynamics. 
# It is importance to know that networks do not have any spatial structure, so it does not tell 
# the location of the farms or the distance between farms. 
#
##############################################################################

#install.packages("igraph")

library ("igraph")# to make network graphs (graph.data.frame)

######################
#SET YOUR DIRECTORY HERE###
######################

directory = "C:/Users/meschoenbaum/Documents/ADSM Vaccination Rings Workspace"
ADSMWorkspace = "C:/Users/meschoenbaum/Documents/ADSM Vaccination Rings Workspace"
SuppFile = "C:/Users/meschoenbaum/Documents/ADSM Vaccination Rings Workspace/TestStack/Daily_exposures_5.csv"

#####################################
####completed setting directories####
#####################################

SuppFileDailyExposures1<-read.csv(SuppFile)


S1farm<-cbind(SuppFileDailyExposures1$Source_ID, SuppFileDailyExposures1$Recipient_ID)
colnames(S1farm)<-c("SourceID","RecipientID")

S1farm_df<-as.data.frame(S1farm)

#### Don't want the NA values included (if you do, comment out the code below)
S1farm_df = S1farm_df[complete.cases(S1farm_df), ]

net1<-graph.data.frame(S1farm_df,directed=T)

plot(net1,layout=layout.fruchterman.reingold,vertex.size=10,edge.arrow.size=0.2, vertex.label.cex = 0.9, vertex.label=S1farm_df$Source_ID, main="Exposure Network")
