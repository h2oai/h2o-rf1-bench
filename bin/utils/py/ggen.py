import os

def getSimpleRGraph(dataset_file):
    ''' Returns R-code generating a graph from a dataset
    containing x,y,color columns
    '''
    pdf_file = os.path.basename(dataset_file).replace('.csv','.pdf')
    return '''ds<-read.table("%s", sep=",", header=T)

pdf("%s")

plot(ds$x, ds$y, col=ds$color, xlab='x', ylab='y', pch='.')
box()
dev.off()
''' % (dataset_file, pdf_file)

