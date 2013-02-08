rf.ds.name   <- "covtype"
rf.seed      <- 1235098019
rf.train.dsf <- "/home/bench/prg/h2o-bench/datasets/covtype/R/train.csv"
rf.test.dsf  <- "/home/bench/prg/h2o-bench/datasets/covtype/R/test.csv"
rf.pred.class.idx  <- 55

rf.ntrees          <- XXXTREEXXX
rf.r.mtry          <- 7
rf.sampling.ratio  <- XXXSAMPLEXXX
rf.column.ignores  <- c(2,3,7,8,9)

rf.output.analysis <- "/home/bench/tmp/runs/R-covtype-analysis-XXXTREEXXXtree-XXXSAMPLEXXXsampling.txt"

library(randomForest)
#library(party)


# This code is copied from R -implementation
"rfprint" <-
function(x, ...) {
  #cat("\nCall:\n", deparse(x$call), "\n")
  cat("               Type of random forest: ", x$type, "\n", sep="")
  cat("                     Number of trees: ", x$ntree, "\n",sep="")
  cat("No. of variables tried at each split: ", x$mtry, "\n\n", sep="")
  if(x$type == "classification") {
    if(!is.null(x$confusion)) {
      cat("        OOB estimate of  error rate: ",
          round(x$err.rate[x$ntree, "OOB"]*100, digits=2), "%\n", sep="")
      cat("Confusion matrix:\n")
      print(x$confusion)
      if(!is.null(x$test$err.rate)) {
        cat("                Test set error rate: ",
            round(x$test$err.rate[x$ntree, "Test"]*100, digits=2), "%\n",
            sep="")
        cat("Confusion matrix:\n")
        print(x$test$confusion)
      }
    }
  }
}

tslog<-
function(m) {
  cat(sprintf("[%s] %s\n", Sys.time(), m))
} 

getTreeDepth <- function(tree, idx) {
    node <- tree[idx,]
    if (node$status == -1)
        return(0);

    ld <- getTreeDepth(tree, as.integer(node["left daughter"]))
    rd <- getTreeDepth(tree, as.integer(node["right daughter"]))

    if (ld > rd) 
        return (ld+1)
    else
        return (rd+1)
}

sink(file=rf.output.analysis, split=TRUE)

# Configure time precision
options(digits.secs=4)

cat("\n======== Train data ========\n")
# Load train dataset
tslog("Train datasets loading....")
train.ds <- read.table(rf.train.dsf, header=TRUE,sep=",")
train.ds <- na.omit(train.ds)
tslog("...FINISHED")

train.numcol <- ncol(train.ds)
train.cols   <- setdiff(c(1:train.numcol), c(rf.pred.class.idx))
train.cols   <- setdiff(train.cols, rf.column.ignores)
train.col.with.class <- c(rf.pred.class.idx)
cat("X= ", train.cols, "\n")
cat("Y= ", train.col.with.class, "\n")
cat("Ignores: ",rf.column.ignores , "\n")

set.seed(rf.seed)
params <- list(x=train.ds[,train.cols],
               y=train.ds[,train.col.with.class],
                importance=TRUE,
                ntree=rf.ntrees,
                replace=FALSE,
                keep.forest=TRUE,
                na.action=na.omit,
                mtry=rf.r.mtry)

if (exists('rf.sampling.ratio')) {
    cat(rf.sampling.ratio)
    sr <- ceiling(rf.sampling.ratio / 100 * nrow(train.ds))
    params <- c(params, sampsize=sr)
}

tslog("Calling random forest...")
sstarttime<-Sys.time()
starttime<-proc.time()
train.ds.rf <- do.call(randomForest,params)
endtime<-proc.time()
sendtime<-Sys.time()
tslog("...FINISHED")

rfprint(train.ds.rf)
# NOTE: To see randomForest function call please uncomment following line:
#print(train.ds.rf)
train.ds.oob <- mean(train.ds.rf$err.rate[,"OOB"])
cat("\nSize of train dataset: ", nrow(train.ds))
cat("\n       Start/End time: ", sprintf("%s", sstarttime), " / ", sprintf("%s", sendtime))
cat("\n             Run time: \n")
endtime-starttime

tslog("Saving RF model...")
save(train.ds.rf, file='rfmodel-ds.data')
tslog("...FINISHED")
cat("\n\n======== Test data ========\n\n")
# Load train dataset
tslog("Test datasets loading....")
test.ds  <- read.table(rf.test.dsf, header=TRUE,sep=",")
test.ds  <- na.omit(test.ds)
tslog("...FINISHED")

tslog("Validation...")
sstarttime<-Sys.time()
starttime<-proc.time()
test.cols <- train.cols
cat("X= ", test.cols, "\n")
test.ds.pred <- predict(train.ds.rf, newdata=test.ds[,test.cols])

# Get comparison table
t <- table(observed=test.ds[,train.col.with.class], predict=test.ds.pred)

# Compute classification error
tsum<-apply(t, 1, sum)
tesum<-tsum-diag(t)
class.error <- tesum/tsum

observations <- sum(tsum)
errors       <- sum(tesum)
overall.class.err <- errors / observations
endtime<-proc.time()
sendtime<-Sys.time()
tslog("...FINISHED")

cat("Classification error (err / observations): ", overall.class.err*100, "% \n")
cat("                Total number of instances: ", observations, "\n")
cat("           Correctly classified instances: ", observations-errors, "\n")
cat("         Incorrectly classified instances: ", errors, "\n")
cat("                     Size of test dataset: ", nrow(test.ds), "\n")
cat("                           Start/End time: ", sprintf("%s",sstarttime), " / ", sprintf("%s",sendtime), "\n")
cat("                                 Run time: \n")
endtime-starttime

# Append classification error to original table
cat("\nConfusion matrix:\n")
cbind(t,class.error)

