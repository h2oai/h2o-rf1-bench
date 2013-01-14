#!/usr/bin/python
from ssdgen import TestType
from ssdgen import SSDGen
from ssdgen import getTrainTestSizes
import ggen

def main():
    unbalancedGen = UnbalancedGen.create()
    unbalancedGen.generate()
    
COLORS = ['W', 'B']
DEFAULT_NUMBER_OF_POINTS=10000
DEFAULT_MINOR=1
DEFAULT_MAJOR=9
DEFAULT_NOISE_RATIO=000.0

'''
Datase tgenerator for stratified sampling.
For example:
minor:major = 1:5 represents rectangle:

+1+2-3-4-5-6+
|W|B B B B B|
+-----------+

'''
class UnbalancedGen(SSDGen):

    def __init__(self, outputDir, ratio, points, minor, major, noise_ratio):
        (trainSize, testSize) = getTrainTestSizes(ratio, points)

        super(UnbalancedGen, self).__init__(outputDir, trainSize, testSize)

        self._minor      = minor
        self._major      = major
        self._minorCoef  = 1. * minor / (minor+major)
        self._majorCoef  = 1 - self._minorCoef
        self._length     = minor+major
        self._noiseRatio = noise_ratio
        self._noiseInTrain = (self._majorCoef * self._trainSize) * noise_ratio
        self._noiseInTest  = (self._majorCoef * self._testSize) * noise_ratio

        self._genTrainNoise = 0
        self._genTestNoise  = 0

    def genDsName(self):
        return 'unbalanced_%sx%s_%s' % (self._minor, self._major, self._total)

    def genHeader(self):
        return ('x','y','color')

    def genPoint(self, test_target, idx, total):
        minorPoints = self._minorCoef * total

        y = self._rand.random()
        if idx < minorPoints: 
            x = self._rand.uniform(0, self._minor)
            color = COLORS[0]
        else:
            if (test_target == TestType.TRAIN):
                noise = 0 # self._noiseInTrain
            else:
                noise = self._noiseInTest

            if (idx - minorPoints) < noise:
                x = self._rand.uniform(0, self._minor)
                print "NOISE"
                #self._genTrainNoise += 1
            else:
                x = self._minor + self._rand.uniform(0, self._major)

            color = COLORS[1]

        return (x,y,color)

    def genGraph(self, f, ds_fname):
        f.write(ggen.getSimpleRGraph(ds_fname))

    def printInfo(self):
        print "       minor:major = %s : %s" % (self._minor, self._major)
        print "Train: minor:major points = %s : %s" % (self._minor * self._trainSize/self._length, self._major * self._trainSize/self._length)
        print "Test : minor:major points = %s : %s" % (self._minor * self._testSize/self._length, self._major * self._testSize/self._length)
        print "             \nnoise ratio = %s" % (self._noiseRatio)
        #print "traint:test noise points = %s : %s" % (self._noiseInTrain, self._noiseInTest)
        #print "      noise points = %s" % (self._noisePoints)

    @classmethod
    def getArgParser(clazz, description):
        parser = SSDGen.getDefaultArgParser(description)
        parser.add_argument('--points', '-p', help="total number of points to generate",type=int,default=DEFAULT_NUMBER_OF_POINTS)
        parser.add_argument('--minor', help="total ratio of points in minor class",type=int,default=DEFAULT_MINOR)
        parser.add_argument('--major', help="total ratio of points in major class",type=int,default=DEFAULT_MAJOR)
        parser.add_argument('--noise_ratio', help="ratio of total majority points which are noisy (means that they are generated in minority section)",type=float,default=DEFAULT_NOISE_RATIO)
   
        return parser

    @classmethod
    def create(clazz):
        parser = clazz.getArgParser(
             """Generator producing unbalanced dataset.
             It is a rectangle of <points> point 
             """)

        args = parser.parse_args()
        chessGen = UnbalancedGen(args.output, args.ratio, args.points, args.minor, args.major, args.noise_ratio)

        return chessGen

#
# Static method
#
def getTotalPoints(nrow, ncols, pointsPerCell):
    return nrow*ncols*pointsPerCell

if __name__ == '__main__':
    main()


