#!/usr/bin/Rscript


.libPaths(c(.libPaths(), "D:\\Rlib"))

library(TCGAbiolinks)
library(EDASeq)

#barcodeFile <- "sample_barcodes.xls"

#dataBar <- read.table(barcodeFile, header=TRUE, stringsAsFactor =FALSE)

#dataTP <- dataBar$Tumor
#dataNT <- dataBar$Normal

#head(dataBar)
setwd("D:/R-Code")

barcodeDir <- "D:\\R-Code\\barcodes\\"

if (! dir.exists(barcodeDir)) {
    print("barcode Dir does not exist!")
    q(save="no")
}
 
AllProjects <- TCGAbiolinks:::getGDCprojects()$project_id
CancerProjects <- AllProjects[10:length(AllProjects)]   ## or you can use AllProjects[-(1:9)]

#CancerProjects <- c("TCGA-LAML", "TCGA-LIHC", "TCGA-PCPG")

DataDirectory <- "D:\\R-Code\\TCGA_data\\"

for (CancerProject in CancerProjects){
    ProjectResult <- paste0("result_", CancerProject, "_dataDEGs.xls")
    
    if (! file.exists(ProjectResult)){
    
        FileNameData <- paste0(DataDirectory, CancerProject, "_Norm_results",".rda")

        query <- NA

        query <- tryCatch(
            GDCquery(project = CancerProject,
                  data.category = "Transcriptome Profiling",
                  data.type = "Gene Expression Quantification", 
                  workflow.type = "HTSeq - Counts")

        , error=function(e) print("Something go wrong at checkDataCategoriesInput!") )

    #if(inherits(query, "error")) {next}

        if (! is.na(query)) {
            samplesDown <- getResults(query,cols=c("cases"))

            tissueDef <- getResults(query,cols=c("tissue.definition"))
        } else {
            next
        }

    # print(tissueDef)

        if(! is.na(query) && "Solid Tissue Normal" %in% tissueDef && "Primary solid Tumor" %in% tissueDef){

            dataSmTP <- TCGAquery_SampleTypes(barcode = samplesDown,
                                  typesample = "TP")

            dataSmNT <- TCGAquery_SampleTypes(barcode = samplesDown,
                                  typesample = "NT")

            NumTP <- ifelse(length(dataSmTP) > 25, 25, length(dataSmTP))
            NumNT <- ifelse(length(dataSmNT) > 25, 25, length(dataSmNT))

            num <- min(NumTP,NumNT)

            dataTP <- dataSmTP[1:num]
            dataNT <- dataSmNT[1:num]

        ### write barcodes of tumor

            TumorfileConn<-file(paste0(barcodeDir,CancerProject,"_Tumor.txt"))
            writeLines(dataTP, TumorfileConn)
            close(TumorfileConn)

        ### write barcodes of Normal
    
            NormalfileConn <- file(paste0(barcodeDir, CancerProject,"_Normal.txt"))
            writeLines(dataNT, NormalfileConn)
            close(NormalfileConn)

            q_Down <- GDCquery(project = CancerProject, 
                data.category = "Transcriptome Profiling",
                data.type = "Gene Expression Quantification", 
                workflow.type = "HTSeq - Counts",
                barcode = c(dataTP, dataNT))

            GDCdownload(query = q_Down,
                directory = DataDirectory)

            dataPrep_AD <- GDCprepare(query = q_Down, 
                       save = TRUE, 
                       directory =  DataDirectory,
                       save.filename = FileNameData)

            dataPrep <- TCGAanalyze_Preprocessing(object = dataPrep_AD, 
                                      cor.cut = 0.6,
                                      datatype = "HTSeq - Counts")

            dataNorm <- TCGAanalyze_Normalization(tabDF = dataPrep,
                                      geneInfo = geneInfoHT,
                                      method = "gcContent")

            dataFilt <- TCGAanalyze_Filtering(tabDF = dataNorm,
                                  method = "quantile", 
                                  qnt.cut =  0.25)

            dataDEGs <- tryCatch( TCGAanalyze_DEA(mat1 = dataFilt[,dataTP],
                            mat2 = dataFilt[,dataNT],
                            Cond1type = "Normal",
                            Cond2type = "Tumor",
                            fdr.cut = 0.01 ,
                            logFC.cut = 1,
                            method = "glmLRT"), error=function(e) {print("Something go wrong at TCGAanalyze_DEA");
                            ""
                            })
        ### write differential expression results to file
    
            ProjectResult <- paste0("result_", CancerProject, "_dataDEGs.xls")
            write.table(dataDEGs, file = ProjectResult, quote = FALSE, sep = "\t", row.names = FALSE)
        } else {
            print(paste(CancerProject, "does not contain TP and NT samples!", sep=" "))
        }
    }
            
            
  ##   => Add clinical information to samples
  ##   Add FFPE information. More information at:
  ##  => https://cancergenome.nih.gov/cancersselected/biospeccriteria
  ##  => http://gdac.broadinstitute.org/runs/sampleReports/latest/FPPP_FFPE_Cases.html

  ##  => Adding subtype information to samples
  ##  Subtype information from:doi:10.1038/nature11404
  ##  Downloading genome information (try:0) Using: Human genes (GRCh38.p10)
  ##  Loading from disk
  ##  From the 60483 genes we couldn't map 3520
  ##  Saving file:D:\R-Code\TCGA_data\TCGA-LUSC_Norm_results.rda
  ##  File saved
  ##  I Need about  36 seconds for this Complete Normalization Upper Quantile  [Proces
  ##  sing 80k elements /s]
  ##  Step 1 of 4: newSeqExpressionSet ...
  ##  Step 2 of 4: withinLaneNormalization ...
  ##  Step 3 of 4: betweenLaneNormalization ...
  ##  Step 4 of 4: .quantileNormalization ...
    ##  Batch correction skipped since no factors provided
    ##  ----------------------- DEA -------------------------------
    ##  there are Cond1 type Normal in  25 samples
    ##  there are Cond2 type Tumor in  25 samples
    ##  there are  17428 features as miRNA or genes
    ##  I Need about  29 seconds for this DEA. [Processing 30k elements /s]
    ##  Batch submitting query [====================-----------]  64% eta:  1m
            
            
}




