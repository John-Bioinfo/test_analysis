#!/usr/bin/env Rscript


p1 <- c( "pair_1824453.xlsx",
       "pair_1824459.xlsx",
       "pair_1910165.xlsx",
       "pair_1910176.xlsx",
       "pair_1910180.xlsx",
       "pair_1920085.xlsx" )


s1 <- c( "single_1824453.xlsx",
        "single_1824459.xlsx",
        "single_1910165.xlsx",
        "single_1910176.xlsx",
        "single_1910180.xlsx",
        "single_1920085.xlsx" )

library(readxl)

for (i in seq(1, length(p1))) {

    dat <- data.frame(read_excel(s1[i], sheet=1))
    dat.p <- data.frame(read_excel(p1[i], sheet=1))

    dat$newCol <- do.call(paste, c(dat[c("Chr", "Start", "End")], sep="-"))
    dat.p$newCol <- do.call(paste, c(dat.p[c("Chr", "Start", "End")], sep="-"))

    a <- dat$newCol
    #a <- sort(dat$newCol, decreasing=T)
    b <- dat.p$newCol
    #b <- sort(dat.p$newCol, decreasing=T)

#    print(dat$T.Freq)
#    print(dat.p$T.Freq)

    mi <- match(a, b)
    if (length(b) < length(mi)){
	
	d <- data.frame("single"=a, "match_pair"=b[mi], "S_freq"=dat$T.Freq, "P_freq"=dat.p$T.Freq[mi])
	print(b)
        print(s1[i])
        print(p1[i])

	write.table(d, file=paste0(substr(p1[i], 1, 12), '.diff') , row.names=F, quote=F, sep='\t')
    }

    print("===============================")
}

