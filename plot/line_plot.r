#!/usr/bin/env Rscript

# Libraries:
library(ggplot2)
library(reshape2)

# Parsing command line arguments:
options <- commandArgs(trailingOnly = TRUE)

# Loading files:
table = read.csv(options[1], header = FALSE)

colnames(table) = c("dpkg", "pip", "git", "misc", "timestamp")

melted_table = melt(table, id.vars = "timestamp", variable.name = "category")

# Plotting:
ggplot(melted_table, aes(timestamp, value)) + geom_line(aes(colour = category))