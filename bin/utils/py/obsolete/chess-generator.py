#!/usr/bin/python

import argparse
import random
import os, sys
import subprocess

COLORS = [ 'W', 'B' ]
X_LIMIT=8
Y_LIMIT=8

# number of points to generate for each cell
NUM_POINTS=5

TRAIN_RATIO=2.0/3

OUTPUT_DIR='../../../datasets'

RAND=random.SystemRandom(92832019)

def main():
    parser = argparse.ArgumentParser(description="R RandomForest parse" )
    parser.add_argument('-x', help="x-dimension of board",type=int,default=X_LIMIT)
    parser.add_argument('-y', help="y-dimension of board",type=int,default=Y_LIMIT)
    parser.add_argument('--points', '-p', help="number of random points in each cell",type=int,default=NUM_POINTS)
    parser.add_argument('--ratio', '-r', help="ratio from all data to generate train set",type=float,default=TRAIN_RATIO)
    parser.add_argument('--output', '-o', help="output directory",type=str,default=OUTPUT_DIR)
    parser.add_argument('--default', '-d', help="run with default")

    args = parser.parse_args()
    
    generate(args.output, args.x,args.y,args.points,args.ratio)

def points(x,y, num_points):
    global RAND

    p = []
    for c in range(0, num_points):
        p.append( (x+RAND.random(),y+RAND.random()) )

    return p

def write(f, point):
    f.write("%f,%f,%s\n" % point)

def write_header(f):
    f.write("x,y,color\n")

def generate(output_dir=OUTPUT_DIR,xlim=X_LIMIT,ylim=Y_LIMIT, num_points=NUM_POINTS, train_ration=TRAIN_RATIO):
    output = []
    cnt = 0
    for x in range(0, xlim):
        for y in range (0, ylim):
            color = COLORS[(x+y) % 2]
            for (x1,y1) in points(x,y,num_points): 
                output.append((x1,y1,color))
                cnt +=1

    random.shuffle(output)

    train_count = int(cnt*train_ration)
    test_count  = cnt - train_count
    
    # setup directories
    ds_name         = "chess_%sx%sx%s" % (xlim, ylim, num_points)
    ds_dirname      = "%s/chess_%sx%sx%s" % (output_dir,xlim, ylim, num_points)
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
    print "        X_LIMIT = %d" % xlim
    print "        Y_LIMIT = %d" % ylim
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

    print("Remaining: %s" % output)

    print("\n...launching weka transformation...")
    pathname = os.path.dirname(sys.argv[0])
    weka_script = "%s/../generate-dataset-arff.sh" % pathname

    subprocess.call([weka_script, ds_name])

if __name__ == '__main__':
    main()


