
library(reshape2)
d <- read.table('sensitivity_IC50.xls', header=T, stringsAsFactors=F, sep='\t')
#   head(d[grep('drugid_51_', d[,1]),])
new.d <- d[grep('drugid_51_', d[,1]),]
cell_raw.data <- read.table('../result_data.xls', row.names=1, header=T, sep='\t', stringsAsFactors=F)
#   rownames(cell_raw.data)[1:5]

a <- colsplit(string= new.d[,1], pattern="_", names=c("Part1", "Part2", "Part3"))
#   print(head(new.d[a$Part3 %in% rownames(cell_raw.data),]))
##  print(a[1:10,3])
res.d <- new.d[a$Part3 %in% rownames(cell_raw.data),]
write.table(res.d, 'IC50_INFO.xls', quote = FALSE,row.names = F, col.names=T, sep="\t")

#   a <- "drugid_202_CAL-148"
#   strsplit(a, '_')[[1]][2]
#   substr(a, 12,18)

feature.dat <- read.table('../features_data.txt', header=T,sep='\t', stringsAsFactors=F, row.names=1)
new_feat_d <- feature.dat[match(a[,3] , rownames(feature.dat)), ]

#   print(head(new_feat_d, 10))
new_feat_d <- new_feat_d[!is.na(new_feat_d$class),]
#   print(nrow(res.d))
#   print(nrow(new_feat_d))

#   print(head(res.d[,1:3], 8))
#   print(head(new_feat_d[,45:50], 8))
#   print(ncol(new_feat_d))
#   print(head(new_feat_d[,2056:2060], 8))

new.d <- cbind(res.d[,1:3], new_feat_d[,45:2059])
new.d <- data.frame(new.d)
print(head(new.d[,1:9], 8))

#for (i in 4:ncol(new.d)) {
#    cor_t <- cor.test(new.d[,2] , new.d[,i],  method = "pearson", conf.level = 0.95)
#    cat(cor_t$estimate, cor_t$p.value, '\n', sep='\t')
#}

cor_d <- do.call("rbind", sapply(4:ncol(new.d), FUN=function(i){cor_t <- cor.test(new.d[,2] , new.d[,i],  method = "pearson", conf.level = 0.95); c(cor_t$estimate, cor_t$p.value, colnames(new.d)[i])}, simplify = FALSE))

#print(head(cor_d))

write.table(cor_d, 'IC50_pearson_cor.xls', quote = FALSE,row.names = F, col.names=T, sep="\t")

cor_d_spear <- do.call("rbind", sapply(4:ncol(new.d), FUN=function(i){cor_t <- cor.test(new.d[,2] , new.d[,i],  method = "spearman", conf.level = 0.95); c(cor_t$estimate, cor_t$p.value, colnames(new.d)[i])}, simplify = FALSE))

write.table(cor_d_spear, 'IC50_spearman_cor.xls', quote = FALSE,row.names = F, col.names=T, sep="\t")

