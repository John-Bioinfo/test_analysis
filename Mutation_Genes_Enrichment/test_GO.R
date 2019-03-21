library("org.Hs.eg.db")
library("GSEABase")
library("GOstats")

genes <- c("AREG", "FKBP5", "CXCL13", "KLF9", "ZC3H12A","CCL5", "MCM6", "GCH1", "CAV1", "SLC20A1")

##GO BP enrichment analysis
goAnn <- get("org.Hs.egGO")
universe <- Lkeys(goAnn)

entrezIDs <- mget(genes, org.Hs.egSYMBOL2EG, ifnotfound=NA)
entrezIDs <- as.character(entrezIDs)

params <- new("GOHyperGParams",
                  geneIds=entrezIDs,
                 universeGeneIds=universe,
                 annotation="org.Hs.eg.db",
                 ontology="BP",
                 pvalueCutoff=0.01,
                 conditional=FALSE,
                 testDirection="over")

over <- hyperGTest(params)
library(Category)
glist <- geneIdsByCategory(over)
glist <- sapply(glist, function(.ids) {
	.sym <- mget(.ids, envir=org.Hs.egSYMBOL, ifnotfound=NA)
	.sym[is.na(.sym)] <- .ids[is.na(.sym)]
	paste(.sym, collapse=";")
	})

bp <- summary(over)
bp$Symbols <- glist[as.character(bp$GOBPID)]
head(bp)


dim(bp)

##KEGG enrichment analysis
keggAnn <- get("org.Hs.egPATH")
universe <- Lkeys(keggAnn)
params <- new("KEGGHyperGParams",
                    geneIds=entrezIDs,
                    universeGeneIds=universe,
                    annotation="org.Hs.eg.db",
                    categoryName="KEGG",
                    pvalueCutoff=0.01,
                    testDirection="over")
over <- hyperGTest(params)
kegg <- summary(over)
library(Category)
glist <- geneIdsByCategory(over)

glist <- sapply(glist, function(.ids) {
	.sym <- mget(.ids, envir=org.Hs.egSYMBOL, ifnotfound=NA)
	.sym[is.na(.sym)] <- .ids[is.na(.sym)]
	paste(.sym, collapse=";")
	})

kegg$Symbols <- glist[as.character(kegg$KEGGID)]
kegg

library("pathview")
gIds <- mget(genes, org.Hs.egSYMBOL2EG, ifnotfound=NA)
gEns <- unlist(gIds)
gene.data <- rep(1, length(gEns))
names(gene.data) <- gEns

for(i in 1:3){
    pv.out <- pathview(gene.data, pathway.id=as.character(kegg$KEGGID)[i], species="hsa", out.suffix="pathview", kegg.native=T)
}
