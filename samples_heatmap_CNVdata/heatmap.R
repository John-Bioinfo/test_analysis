library(pheatmap)

d_cnv <- read.table("out1.xls",sep="\t",header=T, row.names=1)
m <- as.matrix(d_cnv)
m[m>=2] <- 2
df <- as.data.frame(m)

bk <- c(seq(0,2.0,by=0.02))

t_data <- t(df)

pdf("heatmap_CNV_1.pdf", width= 6, height=8)
pheatmap(t_data, cluster_row=F, cluster_col=F, na.exclude=T, color=colorRampPalette(c("#79CDCD", "#FFFFFF", "#FF6347"))(100),
         legend_breaks=seq(-1,2.1,0.5), breaks=bk)
dev.off()
