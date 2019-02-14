#!/usr/bin/env Rscript

p1 <- c(
       "pair_1910165.xlsx",
       "pair_1910176.xlsx",
       "pair_1910180.xlsx"
        )

s1 <- c( 
        "single_1910165.xlsx",
        "single_1910176.xlsx",
        "single_1910180.xlsx"
        )

library(readxl)
library(caret)
library(e1071)

lvs <- c("Mut", "Non")


for (i in seq(1, length(p1))) {
    dat <- data.frame(read_excel(s1[i], sheet=1))
    dat.p <- data.frame(read_excel(p1[i], sheet=1))

    dat$newCol <- do.call(paste, c(dat[c("Chr", "Start", "End")], sep="-"))
    dat.p$newCol <- do.call(paste, c(dat.p[c("Chr", "Start", "End")], sep="-"))


    all.snps <- unique( c(dat$newCol, dat.p$newCol))

    ## ref: http://www.r-tutor.com/r-introduction/vector/combining-vectors
    ## print(all.snps)

    pred <- factor(ifelse(all.snps %in% dat$newCol, "Mut", "Non"  ),      levels = lvs)
    t    <- factor(ifelse(all.snps %in% dat.p$newCol,   "Mut", "Non"  ),  levels = lvs)
    print(pred)
    print(t)

    xtab <- table(pred, t)
    print(confusionMatrix(xtab))
    # ref : https://www.rdocumentation.org/packages/caret/versions/6.0-81/topics/confusionMatrix

    print("===============================")
}

