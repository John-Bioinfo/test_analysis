library(clusterProfiler)
library(org.Hs.eg.db)
library(ggplot2)

geneNames <- c("AHNAK2", "AQP7", "DNAH11" , "FLG", "HNRNPCL2", "HRNR" , "KMT2C",
                "KMT2D", "MST1L", "MUC12", "MUC16", "MUC17", "MUC19", "MUC3A", 
                "MUC4", "MUC5B", "MUC6", "PABPC3", "PDE4DIP", "PLEC" , "TTN",
                "ANKRD36", "FCGBP", "HERC2", "IGFN1", "KRT18", "SLC25A5", "SYNE2",
                "RYR1", "TNS1", "DST", "SYNE1", "TSNARE1", "NBPF19", "NBPF26",
                "PRKCB", "ADGRG1", "OPCML")


d1 <- read.table("genenames.txt", header=T, stringsAsFactor =F)
geneAll <- d1$GeneName

geneList <- mapIds(org.Hs.eg.db, geneAll, 'ENTREZID', 'SYMBOL')
gene <-  mapIds(org.Hs.eg.db, geneNames, 'ENTREZID', 'SYMBOL')
go_cc <- enrichGO(   gene   = gene,
                  universe  = geneList,
                     OrgDb  = org.Hs.eg.db,
                      ont   = "CC"  ,    
                pAdjustMethod = "BH",
                pvalueCutoff  = 0.01,
                qvalueCutoff  = 0.05)

#dotplot(go_cc, x="count", showCategory=20, color="pvalue")     
#dotplot(go_cc, x="GeneRatio", showCategory=20)

Edata <- as.data.frame(go_cc)[,c(2,3, 5, 9)]
colnames(Edata) <- c("GO description", "GeneRatio", "pvalue" ,"Count")
Edata[,1] <- as.character(Edata[,1])
Edata[,1]<- factor(Edata[,1], levels=rev(unique(Edata[,1])))

Edata$GeneRatio <- Edata$Count/37

#Edata <- Edata[order(Edata[,2]),]

p <- ggplot(Edata, aes(x=GeneRatio, y=`GO description`)) +
     geom_point(aes( colour = -log10( pvalue ), size= Count)  ) +
     ggtitle("GO enrichment")  +  scale_color_gradient(low = 'green', high = 'red') +
     theme(axis.text.x=element_text(angle=0,size=12, vjust=0.7), axis.text.y=element_text(angle=0,size=20, vjust=0.7),plot.title = element_text(lineheight=.8, face="bold", hjust=0.5, size =16), panel.background = element_rect(fill="white", colour='gray'), panel.grid.major = element_line(size = 0.05, colour = "gray"), panel.grid.minor.y = element_line(size=0.05, colour="gray"), panel.grid.minor.x = element_line(size=0.05, colour="gray")
)

## theme_bw()   theme_light()
## https://www.r-bloggers.com/ggplot2-themes-examples/

ggsave("out_GO.pdf", p, width = 10, height=7)

## biological process    BP
## molecular  function   MF
## cellular   component  CC
