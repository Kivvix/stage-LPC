#!/usr/bin/env Rscript

## @author J. Massot
#  @date 2014-05-05
#
#  @brief Display density of calexp files into 1% of stripe 82

# import csv file
require(data.table,quiet=TRUE)
dens <- fread("density.csv",sep=",",header=TRUE)

library(plotrix)

col1 <- dens[[1]]
col2 <- dens[[2]]
col3 <- dens[[3]]

m <- matrix(0,nrow=max(col2) , ncol=max(col1))
m[cbind(col2,col1)] = col3
a = mean(col3)

cellcol<-matrix(rep("#000000",nrow(m)),nrow=nrow(m))
cellcol[m<a]<-color.scale(m[m<a],0,c(0.6,1),c(0.8,0.1))
cellcol[m>a]<-rev(color.scale(m[m>a],c(1,0.8),c(0.1,0.8),0))

pdf("density_one_percent.pdf",title="Density of 1% of Stripe 82")
#png("density_one_percent.png", bg="transparent", width=700, height=500)
color2D.matplot( m,cellcolors=cellcol,xlab="",ylab="",main="Image density of 1% of Stripe 82",border=NA,axes=F)
mtext( "RA (+5° to +7.5°)  " , side=1 )
mtext( "Dec (-1.2° to +1.2°)" , side=2 , line=0.3)

mtext( paste( "mean        : ", a        ) , side=1 , line=1.6 , cex=0.7 , adj=0.01 )
mtext( paste( "minimum  : ", min(col3)) , side=1 , line=2.3 , cex=0.7 , adj=0.01 )
mtext( paste( "maximum : ", max(col3)) , side=1 , line=3 , cex=0.7 , adj=0.01 )

legval<-seq(min(m),max(m),length.out=10)
legcol<-rep("#000000",10)
legcol[legval<a]<-color.scale(legval[legval<a],0,c(0.6,1),c(0.8,0.1))
legcol[legval>a]<-rev(color.scale(legval[legval>a],c(1,0.8),c(0.1,0.8),0))
color.legend(ncol(m)/2,-15,ncol(m),-10,round(c(min(m),a,max(m)),1),rect.col=legcol,cex=0.7)
