ds<-read.table("R/train.csv", sep=",", header=T)

pdf("train.pdf")

plot(ds$x, ds$y, col=ds$color, xlab='x', ylab='y')
box()
dev.off()
ds<-read.table("R/test.csv", sep=",", header=T)

pdf("test.pdf")

plot(ds$x, ds$y, col=ds$color, xlab='x', ylab='y')
box()
dev.off()
