#!/usr/bin/python
import ssdgen
import ggen

def main():
    circleGen = CircleGen.create()
    circleGen.generate()
    
COLORS = ['W', 'B']
DEFAULT_NUMBER_OF_POINTS=10000
DEFAULT_CIRCLE_RADIUS=0.5


class CircleGen(ssdgen.SSDGen):

    def __init__(self, outputDir, ratio, points, radius):
        (trainSize, testSize) = ssdgen.getTrainTestSizes(ratio, points)

        super(CircleGen, self).__init__(outputDir, trainSize, testSize)

        self._radius = radius
        self._radiusPow = radius*radius

    def genDsName(self):
        return 'circle_%s' % (self.getTotal())

    def genHeader(self):
        return ('x','y','color')

    def genPoint(self, idx):
        ''' Circle with center in [0,0] and specified 'radius'. 
        The generated dataset has a form of square (2*radius) x (2*radius) with center in [0,0].
        '''
        x = self._rand.uniform(-2*self._radius, 2*self._radius)
        y = self._rand.uniform(-2*self._radius, 2*self._radius)
        if x*x + y*y > self._radiusPow:
            color = COLORS[0]
        else:
            color = COLORS[1]

        return (x,y,color)

    def genGraph(self, f, train_ds_fname, test_ds_fname):
        f.write(ggen.getSimpleRGraph(train_ds_fname, 'train.pdf'))
        f.write(ggen.getSimpleRGraph(test_ds_fname, 'test.pdf'))

    @classmethod
    def getArgParser(clazz, description):
        parser = ssdgen.SSDGen.getDefaultArgParser(description)
        parser.add_argument('--points', '-p', help="total number of points to generate",type=int,default=DEFAULT_NUMBER_OF_POINTS)
        parser.add_argument('--radius', help="circle radius",type=int,default=DEFAULT_CIRCLE_RADIUS)
   
        return parser

    @classmethod
    def create(clazz):
        parser = clazz.getArgParser(
             """Generator producing circle dataset.
             Circle has a center point in [0,0] and the specified radius. 
             By default the radius is 0.5.
             """)

        args = parser.parse_args()
        chessGen = CircleGen(args.output, args.ratio, args.points, args.radius)

        return chessGen

#
# Static method
#
def getTotalPoints(nrow, ncols, pointsPerCell):
    return nrow*ncols*pointsPerCell

if __name__ == '__main__':
    main()


