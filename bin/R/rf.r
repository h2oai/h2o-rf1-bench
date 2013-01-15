library(randomForest)

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

sink(file=rf.output.analysis)

# Load datasets
train.ds <- read.table(rf.train.dsf, header=TRUE,sep=",")
test.ds  <- read.table(rf.test.dsf, header=TRUE,sep=",")

cat("\n======== Train data ========\n")
set.seed(rf.seed)
params <- list(formula=rf.pred.formula,
                data=train.ds, 
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

starttime<-Sys.time()
train.ds.rf <- do.call(randomForest,params)
endtime<-Sys.time()

print(train.ds.rf)
train.ds.oob <- mean(train.ds.rf$confusion)
cat("\nSize of train dataset: ", nrow(train.ds))

cat("\n======== Test data ========\n\n")
test.ds.pred <- predict(train.ds.rf, newdata=test.ds)
#tree<-getTree(iris.rf,1)
#d<-as.dendrogram(tree)

# Get comparison table
t <- table(observed=test.ds[,rf.pred.class.name], predict=test.ds.pred)

# Compute classification error
tsum<-apply(t, 1, sum)
tesum<-tsum-diag(t)
class.error <- tesum/tsum

observations <- sum(tsum)
errors       <- sum(tesum)
overall.class.err <- errors / observations

cat("Classification error (err / observations): ", overall.class.err*100, "% \n")
cat("                Total number of instances: ", observations, "\n")
cat("           Correctly classified instances: ", observations-errors, "\n")
cat("         Incorrectly classified instances: ", errors, "\n")
cat("                     Size of test dataset: ", nrow(test.ds), "\n\n")
# Append classification error to original table
cat("Confusion matrix:\n")
cbind(t,class.error)

cat(sprintf("\n\nRun time: %.5f sec\n\n", endtime - starttime))
#pt = prop.table(t,1)
#print(pt)

## print(iris.rf$err.rate)
#print(iris.rf$votes)
# Print all trees
depths <- c()
for(i in 1:rf.ntrees) {
    t <- getTree(train.ds.rf,i,labelVar=TRUE)
    depths <- append(depths, getTreeDepth(t,1))
}
leaves=treesize(train.ds.rf,terminal=TRUE)
nodes=treesize(train.ds.rf,terminal=FALSE)

cat("\n")
#cat(sprintf(" Nodes summary (Min/Mean/Max): %.1f / %.1f / %.1f\n", min(nodes), mean(nodes),  max(nodes)))
cat(sprintf("Depths summary (Min/Mean/Max): %.1f / %.1f / %.1f\n", min(depths), mean(depths), max(depths)))
cat(sprintf("Leaves summary (Min/Mean/Max): %.1f / %.1f / %.1f\n", min(leaves), mean(leaves), max(leaves))) 
cat(sprintf("Run time: %.5f sec\n", endtime - starttime))

result <- c(rf.ntrees, rf.r.mtry, min(leaves), mean(leaves), max(leaves), min(depths), mean(depths), max(depths), nrow(train.ds), train.ds.oob, nrow(test.ds), overall.class.err)

cat(result,sep=',')
cat("\n")

# print trees to a separated file
if (rf.print.trees) {
    sink(file=rf.output.trees)
    # Print all trees
    for(i in 1:rf.ntrees) {
        t <- getTree(train.ds.rf,i,labelVar=TRUE)
        print(t)
    }
}


#png(paste(".", formatC(i, digits=3, flag="0"), ".jpg", sep=""))
#plot(t, col="gray"); 
#text(t, cex=.8)
#dev.off()

