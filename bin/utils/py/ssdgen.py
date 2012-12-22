#
# Simple Synthesised Datasets Generator
#
import argparse
import random
import os, sys
import subprocess
import math

#
# Defined constants.
#
DEFAULT_OUTPUT_DIR='../../../datasets/'
DEFAULT_TRAIN_RATIO=2/3.

#
# Helper methods
#
def getTrainTestSizes(ratio, total):
    train_count = int(total*ratio)
    test_count  = total - train_count
    return (train_count, test_count)

def getTestSize(ratio, total):
    (train, test) = getTestTrainSizes(ratio, total)
    return test

def getTrainSize(ratio, total):
    (train, test) = getTestTrainSizes(ratio, total)
    return train

#
# Simple Synthesised Datasets Generator
#
class SSDGen(object):

    def __init__(self, outputDir, trainSize, testSize, seed=92832019):
        self._outputDir = outputDir
        self._trainSize = trainSize
        self._testSize  = testSize
        self._total     = trainSize + testSize

        self._rand      = random.SystemRandom(seed)

    def generate(self):
        output = self.genPoints()
        random.shuffle(output)

        self.__writeDataset(output)

    def genPoints(self):
        output = []
        cnt    = self._total
        
        # Data generation
        for i in range(0, cnt):
            output.append(self.genPoint(i))

        return output

    def __writeDataset(self, output):
        # setup directories
        ds_name         = self.genDsName()
        ds_dirname      = "%s/%s" % (self._outputDir,ds_name)
        ds_R_dirname    = "%s/R" % ds_dirname
        ds_h2o_dirname  = "%s/h2o" % ds_dirname
        ds_weka_dirname = "%s/weka" % ds_dirname
        ds_header       = self.genHeader()

        if not os.path.exists(ds_R_dirname):
            os.makedirs(ds_R_dirname, 0775)
        if not os.path.exists(ds_h2o_dirname):
            os.symlink('./R', ds_h2o_dirname)
        if not os.path.exists(ds_weka_dirname):
            os.makedirs(ds_weka_dirname, 0775)
        
        print "======================"
        print "Generated points = %d" % self._total
        print "     Train items = %d" % self._trainSize
        print "      Test items = %d" % self._testSize
        print "     Dataset dir = %s" % ds_dirname
        print "          Header = %s" % str(ds_header)
        print "======================"

        # write files
        trainfname = "%s/%s" % (ds_R_dirname,'train.csv')
        with open(trainfname, 'w') as f:
            self.__writeHeader(f, ds_header)
            for i in range(0, self._trainSize):
                point = output.pop()
                self.__writePoint(f,point)

        testfname = "%s/%s" % (ds_R_dirname,'test.csv')
        with open(testfname, 'w') as f:
            self.__writeHeader(f, ds_header)
            for i in range(0, self._testSize):
                point = output.pop()
                self.__writePoint(f,point)
            # write some point where test data set is empty


        # write dataset configuration
        self.__writeRfConf(ds_dirname)

        # write dataset visualization script
        self.__writeRGraph(ds_dirname, 'R/train.csv', 'R/test.csv')

    def __writePoint(self, f, point):
        f.write(','.join(map(str,point)))
        f.write('\n')
    
    def __writeHeader(self, f, header):
        f.write(','.join(map(str,header)))
        f.write('\n')

    def __writeRfConf(self, ds_dirname):
        rfconfname = "%s/%s" % (ds_dirname, "rf.conf")
        header     = self.genHeader()
        mtry       = self.getMtry(header)
        with open(rfconfname, 'w') as f:
            f.write("RF_PRED_FORMULA='%s ~ .'\n"  % ( self.getClassColumnName(header)) )
            f.write("RF_PRED_CLASS_NAME=\"%s\"\n" % ( self.getClassColumnName(header)) )
            f.write("RF_PRED_CLASS_IDX=%s\n"      % ( self.getClassColumnIdx(header) + 1 ) )
            f.write("RF_PRED_CLASS_IDX_H2O=%s\n"  % ( self.getClassColumnIdx(header) ) )
            f.write("RF_R_MTRY=%d\n"              % ( mtry ) )
            f.write("RF_WEKA_MTRY=%d\n"           % ( mtry ) )

    def __writeRGraph(self, ds_dirname, train_ds_fname, test_ds_fname):
        gfname = "%s/%s" % (ds_dirname, "graph.r")
        with open(gfname, 'w') as f:
            self.genGraph(f, train_ds_fname, test_ds_fname)

    # zero-based class column
    def getClassColumnIdx(self, header):
        return len(header)-1

    def getClassColumnName(self, header):
        idx    = self.getClassColumnIdx(header)
        return header[idx]

    def getMtry(self, header):
        mtry = math.sqrt(len(header)-1)
        return mtry

    def getTotal(self):
        return self._total

    #
    # Methods to be override
    #
    def genDsName(self):
        pass

    def genPoint(self, idx):
        pass

    def genHeader(self):
        pass

    def genGraph(self, f, train_ds_fname, test_ds_fname):
        pass
    
    #
    # Static methods
    #
    @classmethod
    def getDefaultArgParser(clazz, description):
        parser = argparse.ArgumentParser(description=description)
        parser.add_argument('--ratio', '-r', help="ratio from all data to generate train set",type=float,default=DEFAULT_TRAIN_RATIO)
        parser.add_argument('--output', '-o', help="output directory",type=str,default=DEFAULT_OUTPUT_DIR)
        
        return parser

