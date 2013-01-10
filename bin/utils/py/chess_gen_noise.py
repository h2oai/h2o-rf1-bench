#!/usr/bin/python
import chess_gen
import ssdgen

DEFAULT_NOISY_COLS=1

def main():
    chessGen = ChessGenNoise.create()
    chessGen.generate()
    

class ChessGenNoise(chess_gen.ChessGen):

    def __init__(self, outputDir, ratio, ncols, nrows, pointsPerCell, noiseCol):
        super(ChessGenNoise, self).__init__(outputDir, ratio, ncols, nrows, pointsPerCell)
        self._noiseCol = noiseCol

    def genDsName(self):
        return 'chess_%sx%sx%s_noise%s' % (self._ncols, self._nrows, self._pointsPerCell, self._noiseCol)

    def genHeader(self):
        return ('x','y','color','n1')

    def _genPoint(self, x, y, color):
         return (x+self._rand.random(),y+self._rand.random(), color, self._rand.random())
    
    @classmethod
    def getArgParser(clazz, description):
        parser = chess_gen.ChessGen.getArgParser(description)
        parser.add_argument('--noise', help="number of noisy columns",type=int,default=DEFAULT_NOISY_COLS)
   
        return parser

    @classmethod
    def create(clazz):
        parser = ChessGenNoise.getArgParser(
             """Same as chess board generator, but for each row add noise columns.
            """)

        args = parser.parse_args()
        chessGen = ChessGenNoise(args.output, args.ratio, args.ncols, args.nrows, args.points, args.noise)

        return chessGen

#
# Static method
#
def getTotalPoints(nrow, ncols, pointsPerCell):
    return nrow*ncols*pointsPerCell

if __name__ == '__main__':
    main()


