
library(clusterProfiler)
library(org.Hs.eg.db)

## genelist <- c("AHNAK2", "AQP7", "DNAH11" , "FLG", "HNRNPCL2", "HRNR" , "KMT2C",
#                "KMT2D", "MST1L", "MUC12", "MUC16", "MUC17", "MUC19", "MUC3A", 
#                "MUC4", "MUC5B", "MUC6", "PABPC3", "PDE4DIP", "PLEC" , "TTN",
#                "ANKRD36", "FCGBP", "HERC2", "IGFN1", "KRT18", "SLC25A5", "SYNE2",
#                "RYR1", "TNS1", "DST", "SYNE1", "TSNARE1", "NBPF19", "NBPF26",
#                "PRKCB", "ADGRG1", "OPCML")


d1 <- read.table("genenames.txt", header=T, stringsAsFactor =F)
genelist <- d1$GeneName
entID <-  mapIds(org.Hs.eg.db, genelist, 'ENTREZID', 'SYMBOL')

kk <- enrichKEGG(entID, 'hsa', pvalueCutoff = 0.02, qvalueCutoff=0.1 )

## dotplot(kk,title="Enrichment KEGG_dot")

dotplot(kk,title="KEGG Pathway Enrichment", color="pvalue")
write.table(as.data.frame(kk), file="test_enrichRes.xls", quote = TRUE, sep = "\t", eol = "\n", na = "NA", dec = ".", row.names = FALSE,col.names = TRUE)

