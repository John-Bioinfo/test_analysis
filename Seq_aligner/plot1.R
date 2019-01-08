
plot_table<- function(file_in){

    data.t <- read.table(file_in, header=T, row.names=1, sep='\t')

    min <- min(data.t)
    max <- max(data.t)	  		 
    ColorRamp <- colorRampPalette(c("skyblue","blue"))(100) 
			 
    ColorLevels <- seq(min, max, length=length(ColorRamp))
    pdf('sample_heatmap.pdf',width=10,height=8)	  
    layout(matrix(data=c(1,2), nrow=1, ncol=2), widths=c(10,1.5), heights=c(1,1))	
    par(mar = c(3,8,2.5,2))

    image(1:ncol(data.t), 1:nrow(data.t), t(data.t), col=ColorRamp,xlab="", ylab="", axes=FALSE)

    axis(BELOW<-1, at=1:ncol(data.t), labels=colnames(data.t), cex.axis=1.5)
    axis(LEFT <-2, at=1:nrow(data.t), labels=rownames(data.t), las= HORIZONTAL<-1,cex.axis=1.5)
    for(i in 1:ncol(data.t)){
        for(j in 1:ncol(data.t)){
            text(i, j, formatC(data.t[i,j],width=2,digits=2),cex = 1.5)
        }
    }

 # Color Scale
    par(mar = c(3,2.5,2.5,2))
    image(1, ColorLevels,matrix(data=ColorLevels, ncol=length(ColorLevels),nrow=1),
          col=ColorRamp,xlab="",ylab="",xaxt="n",cex.axis=1.5)
}

args=commandArgs(T)
datafile=args[1]

plot_table(datafile) 
