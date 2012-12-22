#!/usr/bin/python
import chess_gen

def main():
    gen = ChessPlusColumnGen.create()
    gen.generate()

class ChessPlusColumnGen(chess_gen.ChessGen):

    def __init__(self, outputDir, ratio, ncols, nrows, pointsPerCell):
        super(ChessPlusColumnGen, self).__init__(outputDir, ratio, ncols, nrows, pointsPerCell)

    def genDsName(self):
        return 'chess_%sx%sx%s_1f' % (self._ncols, self._nrows, self._pointsPerCell)

    def genHeader(self):
        return ('x','y','z','color')

    def __genPoint(self, x, y, color):
         return (x+self._rand.random(),y+self._rand.random(), self._rand.random(), color)

    @classmethod
    def create(clazz):
        parser = chess_gen.ChessGen.getArgParser(
             """Generator producing chess board dataset NROWxNCOLS. Each cell contains POINTS. 
            Each rows is in form: x,y,z,color, where x,y,z are random float numbers, color is enum('W','B')
            """)

        args = parser.parse_args()
        chessGen = ChessPlusColumnGen(args.output, args.ratio, args.ncols, args.nrows, args.points)

        return chessGen

#
# Static method
#
def getTotalPoints(nrow, ncols, pointsPerCell):
    return nrow*ncols*pointsPerCell

if __name__ == '__main__':
    main()


