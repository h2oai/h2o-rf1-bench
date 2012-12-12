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

def main():
    parser = argparse.ArgumentParser(description="R RandomForest parse" )
    parser.add_argument('-w', help="number of random points for W",type=int,default=NUM_POINTS)
    parser.add_argument('-b', help="number of random points for B",type=int,default=NUM_POINTS)
    parser.add_argument('--ratio', '-r', help="ratio from all data to generate train set",type=float,default=TRAIN_RATIO)
    parser.add_argument('--output', '-o', help="output directory",type=str,default=OUTPUT_DIR)

    args = parser.parse_args()
    
    generate(args.output, args.w, args.b, args.ratio)

def write(f, point):
    f.write("%f,%f,%s\n" % point)

def write_header(f):
    f.write("x,y,color\n")

def gen_point(color):
    x = random.random()
    y = random.random()
    return (x,y,color)
    
def generate(output_dir=OUTPUT_DIR,w=NUM_POINTS,b=NUM_POINTS,train_ratio=TRAIN_RATIO):
    output = []
    cnt = 0

    # Data generation
    for i in range(0, w):
        output.append(gen_point('W'))
        cnt +=1
    for i in range(0, b):
        output.append(gen_point('B'))
        cnt +=1
   
    random.shuffle(output)

    train_count = int(cnt*train_ratio)
    test_count  = cnt - train_count

    # setup directories
    ds_name         = "bad_%s_%s" % (w,b)
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
    print "        Points  = %d,%d" % (w,b)
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
        if train_ratio == 1:
            write(f,(1,1,'W'))

    print("Remaining: %s" % output)

    print("\n...launching weka transformation...")
    pathname = os.path.dirname(sys.argv[0])
    weka_script = "%s/../generate-dataset-arff.sh" % pathname

    subprocess.call([weka_script, ds_name])

if __name__ == '__main__':
    main()


