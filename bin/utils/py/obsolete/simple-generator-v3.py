#!/usr/bin/python

import argparse
import random
import os, sys
import subprocess

COLORS = [ 'W', 'B' ]

# number of points to generate for each cell
NUM_POINTS=100

TRAIN_RATIO=1

OUTPUT_DIR='../../../datasets/'

CENTRAL_POINT=1

DEFAULT_ERROR_X=0
DEFAULT_ERROR_Y=0
DEFAULT_ERROR_Z=0

def main():
    parser = argparse.ArgumentParser(description="R RandomForest parse" )
    parser.add_argument('-x', help="number of random points for region X",type=int,default=NUM_POINTS)
    parser.add_argument('-y', help="number of random points for region Y",type=int,default=NUM_POINTS)
    parser.add_argument('-z', help="number of random points for region Z",type=int,default=NUM_POINTS)
    parser.add_argument('-xe', help="number of errorneous random points in region X",type=int,default=DEFAULT_ERROR_X)
    parser.add_argument('-ye', help="number of errorneous random points in region Y",type=int,default=DEFAULT_ERROR_Y)
    parser.add_argument('-ze', help="number of errorneous random points in region Z",type=int,default=DEFAULT_ERROR_Z)
    parser.add_argument('--ratio', '-r', help="ratio from all data to generate train set",type=float,default=TRAIN_RATIO)
    parser.add_argument('--output', '-o', help="output directory",type=str,default=OUTPUT_DIR)

    args = parser.parse_args()
    
    generate(args.output, args.x, args.y, args.z, args.ratio, args.xe, args.ye, args.ze)

def write(f, point):
    f.write("%f,%s\n" % point)

def write_header(f):
    f.write("x,color\n")

def gen_point(base, color):
    r = random.random()
    return (base+r, color)
    
def generate(output_dir=OUTPUT_DIR,x=NUM_POINTS,y=NUM_POINTS,z=NUM_POINTS,train_ration=TRAIN_RATIO,xe=DEFAULT_ERROR_X,ye=DEFAULT_ERROR_Y,ze=DEFAULT_ERROR_Z):
    output = []
    cnt = 0

    # Data generation
    for i in range(0, x):
        output.append(gen_point(0, 'W'))
        cnt +=1
    for i in range(0, y):
        output.append(gen_point(1, 'B'))
        cnt +=1
    for i in range(0, z):
        output.append(gen_point(2, 'W'))
        cnt +=1
    
    # Error generation
    for i in range(0,xe):
        output.append(gen_point(0, 'B'))
        cnt +=1
    for i in range(0,ye):
        output.append(gen_point(1, 'W'))
        cnt +=1
    for i in range(0,ze):
        output.append(gen_point(2, 'B'))
        cnt +=1

    random.shuffle(output)

    train_count = int(cnt*train_ration)
    test_count  = cnt - train_count

    # setup directories
    ds_name         = "simple_%sp%sp%s_%se%se%s" % (x,y,z,xe,ye,ze)
    ds_dirname      = "%s/%s" % (output_dir,ds_name)
    ds_R_dirname    = "%s/R" % ds_dirname
    ds_h2o_dirname  = "%s/h2o" % ds_dirname
    ds_weka_dirname = "%s/weka" % ds_dirname
    if not os.path.exists(ds_R_dirname):
        os.makedirs(ds_R_dirname, 0775)
    if not os.path.exists(ds_h2o_dirname):
        os.symlink('./R', ds_h2o_dirname)
    if not os.path.exists(ds_weka_dirname):
        os.makedirs(ds_weka_dirname, 0775)

    print "======================"
    print "        Points  = %d,%d,%d" % (x,y,z)
    print "        Errors  = %d,%d,%d" % (xe,ye,ze)
    print "Generated items = %d" % cnt
    print "    Train items = %d" % train_count
    print "     Test items = %d" % test_count
    print "          R dir = %s" % ds_R_dirname
    print "       weka dir = %s" % ds_weka_dirname
    print "        h2o dir = %s" % ds_h2o_dirname
    print "======================"
    
    # generate files
    trainfname = "%s/%s" % (ds_R_dirname,'train.csv')
    with open(trainfname, 'w') as f:
        write_header(f)
        for i in range(0, train_count):
            point = output.pop()
            write(f,point)

    testfname = "%s/%s" % (ds_R_dirname,'test.csv')
    with open(testfname, 'w') as f:
        write_header(f)
        for i in range(0, test_count):
            point = output.pop()
            write(f,point)
        write(f,(1,'W'))

    print("Remaining: %s" % output)

    print("\n...launching weka transformation...")
    pathname = os.path.dirname(sys.argv[0])
    weka_script = "%s/../generate-dataset-arff.sh" % pathname

    subprocess.call([weka_script, ds_name])

if __name__ == '__main__':
    main()


