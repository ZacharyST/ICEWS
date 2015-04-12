'''
This script loads 2 years of ICEWS data and reads the source column.  The goal is to create a list of all sources used in ICEWS.  
'''

#Load data
data <- read.csv('/Data/ICEWS/events.2010.20150313084533.tab',header=TRUE,sep='\t')
data <- rbind(data,read.csv('/Data/ICEWS/events.2011.20150313084656.tab',header=TRUE,sep='\t'))

#Keep only sources column 
publishers <- data$Publisher

#Take set of publishers
publishers <- unique(data$Publisher)
publishers <- set(publishers)

#Save
write.table(publishers,file='/Users/Zack/Documents/UCSD/Data/ICEWS/ICEWS_ListOfPublishers.csv', sep=',',row.names=FALSE,col.names='Publisher')
