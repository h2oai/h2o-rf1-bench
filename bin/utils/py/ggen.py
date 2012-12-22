def getSimpleRGraph(dataset_file, pdf_file):
    ''' Returns R-code generating a graph from a dataset
    containing x,y,color columns
    '''
    return '''train<-read.table("%s", sep=",", header=T)

pdf("%s")

plot(train$x, train$y, col=train$color)
box()
dev.off()
''' % (dataset_file, pdf_file)

