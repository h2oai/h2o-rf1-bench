library(plyr)
rvar_pt<-ddply(sps, c('Tree','SplitVar'), function(x) { c(in_how_many_splits=nrow(x), sum_affected_leaves=sum(x$AffectedLeaves)) }, .progress='text' )
rpoint_pt<-ddply(sps, c('Tree','SplitPoint'), function(x) { c(in_how_many_splits=nrow(x), sum_affected_leaves=sum(x$AffectedLeaves)) }, .progress='text' )

rpoint<-ddply(sps, c('SplitPoint'), function(x) { c(in_how_many_splits=nrow(x), sum_affected_leaves=sum(x$AffectedLeaves)) }, .progress='text' )
#top_total_usages<-head(r[with(r, order(-sum_usages)),], 10)

#top_total_ranking<-head(r[with(r, order(sum_ranking)),], 10)

#top_total_tree_usage<-head(r[with(r, order(-count, sum_ranking)),], 10)

