library(ggplot2)

setwd("D:/maftools/kegg_enrich")

Rawdata <- read.table("test_enrichRes.xls", header=TRUE, sep="\t", stringsAsFactor =F)

Edata <- Rawdata[,c(2,3, 5, 9)]

#Ndata[,2] <- -log10(  Ndata[, 2]  )
colnames(Edata) <- c("Pathway Name", "GeneRatio", "pvalue" ,"Count")
Edata$GeneRatio <- Edata$Count/2596
Edata <- Edata[order(Edata[,2]),]

## ggplot(testData, aes(x=ERank, y=Score)) + 
##     geom_point(aes(size=Num))

## p <- ggplot(testData, aes(x=NLabel, y=Score)) +
##     geom_point(aes(size = Num), colour = "blue")

pvalue <- Edata$pvalue
print(head(Edata))
p <- ggplot(Edata, aes(x=GeneRatio, y=`Pathway Name`)) +
     geom_point(aes(size = Count, colour = -log10( pvalue ))  ) +
     theme(axis.text.x=element_text(angle=0,size=12, vjust=0.7)) +
     ggtitle("KEGG Pathway enrichment")  +  scale_color_gradient(low = 'green', high = 'red') +
     theme(plot.title = element_text(lineheight=.8, face="bold", hjust=0.5, size =16)) + theme_bw()

ggsave("out_KEGG.pdf", p, width = 10, height=7)
