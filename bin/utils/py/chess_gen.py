#!/usr/bin/python
import ssdgen

DEFAULT_NROWS=8
DEFAULT_NCOLS=8
DEFAULT_NPOINTS=10

def main():
    chessGen = ChessGen.create()
    chessGen.generate()
    

class ChessGen(ssdgen.SSDGen):

    def __init__(self, outputDir, ratio, ncols, nrows, pointsPerCell):
        total     = getTotalPoints(ncols, nrows, pointsPerCell)
        (trainSize, testSize) = ssdgen.getTrainTestSizes(ratio, total)

        super(ChessGen, self).__init__(outputDir, trainSize, testSize)
        self._COLORS  = [ 'W', 'B' ]
        self._ncols   = ncols
        self._nrows   = nrows
        self._pointsPerCell = pointsPerCell

    def genDsName(self):
        return 'chess_%sx%sx%s' % (self._ncols, self._nrows, self._pointsPerCell)

    def genHeader(self):
        return ('x','y','color')

    def genPoints(self):
        output = []
        for row in range(0, self._nrows):
            for col in range (0, self._ncols):
                color = self._COLORS[ (row+col) % 2 ]
                for i in range(0, self._pointsPerCell):
                    point = self.__genPoint(col, row, color)
                    output.append(point)

        return output
    
    def __genPoint(self, x, y, color):
         return (x+self._rand.random(),y+self._rand.random(), color)

    def genGraph(self, f, train_ds_fname, test_ds_fname):
        f.write('''
train<-read.table("%s", sep=",", header=T)

pdf('train.pdf')

plot(train$x, train$y, col=train$color)
box()
dev.off()

pdf('test.pdf')
test<-read.table("%s", sep=",", header=T)
plot(test$x, test$y, col=test$color)
box()
dev.off()''' % (train_ds_fname, test_ds_fname) )

    @classmethod
    def getArgParser(clazz, description):
        parser = ssdgen.SSDGen.getDefaultArgParser(description)
        parser.add_argument('--nrows', help="number of board rows",type=int,default=DEFAULT_NROWS)
        parser.add_argument('--ncols', help="number of board columns",type=int,default=DEFAULT_NCOLS)
        parser.add_argument('--points', '-p', help="number of points in each cell",type=int,default=DEFAULT_NPOINTS)
   
        return parser

    @classmethod
    def create(clazz):
        parser = ChessGen.getArgParser(
             """Generator producing chess board dataset NROWxNCOLS. Each cell contains POINTS. 
            Each rows is in form: x,y,color, where x,y are random float numbers, color is enum('W','B')
            """)

        args = parser.parse_args()
        chessGen = ChessGen(args.output, args.ratio, args.ncols, args.nrows, args.points)

        return chessGen

#
# Static method
#
def getTotalPoints(nrow, ncols, pointsPerCell):
    return nrow*ncols*pointsPerCell

if __name__ == '__main__':
    main()


