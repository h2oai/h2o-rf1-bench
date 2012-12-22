train<-read.table("train.csv", sep=",", header=T)

pdf('train.pdf')

plot(train$x, train$y, col=train$color)
box()
dev.off()

pdf('test.pdf')
test<-read.table("test.csv", sep=",", header=T)
plot(test$x, test$y, col=test$color)
box()
dev.off()
