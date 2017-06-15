library(stringi)
library(stringr)
library(dplyr)
library(ggplot2)

# Reading csv

team_totals<-read.csv("E:/ODI Scores/Data/Team_totals.csv",stringsAsFactors = FALSE)

# Cleaning data

team_totals<-team_totals[,-c(1,2,11)]
team_totals<-team_totals[-which(is.na(team_totals$Inns)),]

# Reassigning column names

colnames(team_totals)<-c("Opposition","Start.Date","Inns","Ground","Overs","RPO","Result","Score","Team")

# Obtaining required data

# Only 1st innings total  are required. Second innings are chasing and may not matter
# Since the same was done it effectively removes duplicates. Date-level
# duplicates wont work here since multiple ODI matches happen on a single day

team_totals<-team_totals[which(team_totals$Inns==1),]

# Obtaining matches only where there has been result

team_totals<-team_totals[which(team_totals$Result %in% c("won","lost")),]

# Other requried columns

team_totals[,"Year"]<-stri_sub(team_totals[,"Start.Date"],-4)

team_totals[,"Only.Score"]<-data.frame(t(data.frame(lapply(team_totals$Score,function(x) stri_split_fixed(x,"/")[[1]][1]))))[,1]

team_totals[,"Only.Score"]<-as.numeric(as.character(team_totals[,"Only.Score"]))

# Obtaining the average score

team_totals[,"Year"]<-as.factor(team_totals[,"Year"])

median_score<-team_totals%>%
        group_by(Year)%>%
        summarise(Avg.Score=median(Only.Score))

mean_score<-team_totals%>%
        group_by(Year)%>%
        summarise(Avg.Score=mean(Only.Score))

count_matches<-team_totals%>%
        group_by(Year)%>%
        summarise(Count=n())

median_score[,"Count"]<-count_matches[match(median_score$Year,count_matches$Year),2]

write.csv(median_score,"E:/ODI Scores/Results/median_score.csv",row.names = FALSE)
