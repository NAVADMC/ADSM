##########################################################################
#
# Title: StackedAllFiles_X
#
# Author: Erin Campbell
# Date: 7/17/2018
# Update Date: 6/12/2018 Missy Schoenbaum
# Notes: LOOK for boxes below to enter your scenario and working directory
#
# This script combines all the output files
# This script was tested agaisnt ADSM Beta production v3.5.10.16
# This version has a bug that writes the states_ file out as a matrix 
# with an ambiguous identifier, the script accomdates for this bug.
# Thanks to Matt Branan for function help
#
##############################################################################

#############################################################################
#
# Preparation for running
# Know what directory your scenario file outpus are in, fill in variable
# Clean out any old files if you previously attempted to run this script
# The old files will be within the directory noted in the variable ScenarioDirectory
# 
#############################################################################



####################
#set directory here#
####################

# WHERE TO FIND OUTPUT FILES
Scenariodirectory = "C:/Users/meschoenbaum/My Documents/ADSM Beta Workspace/SampleDaily/Supplemental OUtput Files"
# WHERE YOUR ADSM WORKSPACE WAS INSTALLED, DEFAULT IS MY DOCUMENTS
ADSMWorkspace = "C:/Users/meschoenbaum/My Documents/ADSM Beta Workspace"
# NAME OF THE SCENARIO TO BE WRITTEN INTO THE COMBINED FILE, USEFUL FOR COMPARISON IN ANALYSIS
scenario = "SampleDaily"

setwd(Scenariodirectory)


# Scenariodirectory = "H:/Projects/Statistics - Consulting/Missy Schoenbaum - ADSM R postprocessing/Data/ADSM Workspace/states2"
# ADSMWorkspace = "H:/Projects/Statistics - Consulting/Missy Schoenbaum - ADSM R postprocessing/Data/ADSM Workspace"

## MB: Just putting this into a function

#### Function: Stackfiles
#### Arguments:
  ## directory: file path to where the files to be stacked live (output files are created here as well)
  ## filepattern: a string (wrapped in single or double quotes) that uniquely identifies the files to be stacked within the directory
  ## scenarioname: a string (wrapped in single or double quotes) that you want ot use to identify the ADSM scenario (sets these results apart from results from additional ADSM runs)
stackfiles<-function(directory, 
                     filepattern, 
                     scenarioname){
  
  allfiles<-list.files(Scenariodirectory)
  wantfiles<-allfiles[grep(filepattern, allfiles)]
  
  df<-do.call(rbind,lapply(wantfiles, read.csv))
  
  df$Scenario = scenario
  

  #will show the first few lines of dataset, check these to make sure they are correct
  
  write.csv(df, 
            paste0(scenario, "_stacked_", filepattern, ".csv"), 
            row.names=FALSE)
  #creates a new CSV file in the working directory folder
}

stackfiles(directory = Scenariodirectory,
            filepattern = "states",
            scenarioname = Scenario)

stackfiles(directory = Scenariodirectory,
           filepattern = "events",
           scenarioname = Scenario)

stackfiles(directory = Scenariodirectory,
           filepattern = "exposures",
           scenarioname = Scenario)

#############################################################################
#
# Troubleshooting
# Know what directory your scenario file outpus are in, confirm variable is correct
# Clean out any old files if you previously attempted to run this script
# The old files will be within the directory noted in the variable ScenarioDirectory
# 
#############################################################################

