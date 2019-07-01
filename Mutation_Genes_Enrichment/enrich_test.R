library(clusterProfiler)
library(org.Hs.eg.db)
library(ggplot2)

setwd("D:/medical_service/go_enrich")

# geneNames <- c("AHNAK2", "AQP7", "DNAH11" , "FLG", "HNRNPCL2", "HRNR" , "KMT2C",
 #               "KMT2D", "MST1L", "MUC12", "MUC16", "MUC17", "MUC19", "MUC3A", 
 #               "MUC4", "MUC5B", "MUC6", "PABPC3", "PDE4DIP", "PLEC" , "TTN",
 #               "ANKRD36", "FCGBP", "HERC2", "IGFN1", "KRT18", "SLC25A5", "SYNE2",
 #               "RYR1", "TNS1", "DST", "SYNE1", "TSNARE1", "NBPF19", "NBPF26",
 #               "PRKCB", "ADGRG1", "OPCML")

d1 <- read.table("genenames.txt", header=T, stringsAsFactor =F)
geneNames <- d1$GeneName 
 
 
gene <-  mapIds(org.Hs.eg.db, geneNames, 'ENTREZID', 'SYMBOL')
BP.params <- enrichGO(   gene   = gene,
                     OrgDb  = org.Hs.eg.db,
                      ont   = "BP"  ,    
                pAdjustMethod = "BH",
                pvalueCutoff  = 0.01,
                qvalueCutoff  = 0.05)
                
CC.params <- enrichGO(   gene   = gene,
                     OrgDb  = org.Hs.eg.db,
                      ont   = "CC"  ,    
                pAdjustMethod = "BH",
                pvalueCutoff  = 0.01,
                qvalueCutoff  = 0.05)
                
MF.params <- enrichGO(   gene   = gene,
                     OrgDb  = org.Hs.eg.db,
                      ont   = "MF"  ,    
                pAdjustMethod = "BH",
                pvalueCutoff  = 0.01,
                qvalueCutoff  = 0.05)
                
BP.list <- setReadable(BP.params, org.Hs.eg.db, keyType = "ENTREZID")
CC.list <- setReadable(CC.params, org.Hs.eg.db, keyType = "ENTREZID")
MF.list <- setReadable(MF.params, org.Hs.eg.db, keyType = "ENTREZID")

BP.list <- transform(BP.list, GOType= "BP")
CC.list <- transform(CC.list, GOType = "CC")
MF.list <- transform(MF.list, GOType = "MF")

#dotplot(BP.list, showCategory=30)

goAll <- as.data.frame(rbind(BP.list[c(1:10),], CC.list[c(1:10),], MF.list[c(1:10),]))
goAll <- goAll[nrow(goAll):1, ]


#ggplot(data=goAll)+  geom_bar(aes(x=ID,y=-log10(pvalue), fill=GOType), stat='identity') + coord_flip() + scale_x_discrete(limits=goAll$ID) 
p1 <- ggplot(data=goAll)+  geom_bar(aes(x=Description,y=-log10(pvalue), fill=GOType), stat='identity') + coord_flip() + scale_x_discrete(limits=goAll$Description) 

ggsave("out_bar.pdf", p1, width = 10, height=6)
# legend.position=c(0,1),legend.justification=c(-1,0)    # legend.position="top",    )
Edata <- goAll[,c(2,3, 5, 9,10)]
colnames(Edata) <- c("GO description", "GeneRatio", "pvalue" ,"Count", "GOType")

Edata$GeneRatio <- unlist(lapply(Edata$GeneRatio, function(x){eval(parse(text=x))}))
Edata$`GO description` <- paste0(Edata$`GO description`, "[" , Edata$GOType, "]")

p2 <- ggplot(Edata, aes(x=GeneRatio, y=`GO description`)) +
     geom_point(aes( size= Count , colour = -log10( pvalue ))  ) + scale_y_discrete(limits=Edata$`GO description`)+
     ggtitle("GO enrichment")  +  scale_color_gradient(low = 'green', high = 'red') + xlim(range(Edata$GeneRatio)) +
     theme(axis.text.x=element_text(angle=0,size=8, vjust=0.7), axis.text.y=element_text(angle=0,size=6, vjust=0.7),plot.title = element_text(lineheight=.8, face="bold", hjust=0.5, size =16), panel.background = element_rect(fill="white", colour='gray'), panel.grid.major = element_line(size = 0.05, colour = "gray"), panel.grid.minor.y = element_line(size=0.05, colour="gray"), panel.grid.minor.x = element_line(size=0.05, colour="gray")
)

ggsave("out_GO.pdf", p2, width = 8, height=7)
