#!/usr/bin/env Rscript

# Libraries:
library(ggplot2)
library(reshape2)

# Parsing command line arguments:
options = commandArgs(trailingOnly = TRUE)
filename = options[1]
table_header = options[-1]

# Loading files:
table = read.csv(filename, header = FALSE)

# Setting up the table so it can be plotted:
colnames(table) = table_header
melted_table = melt(table, id.vars = "timestamp", variable.name = "category")

# Plotting:
ggplot(melted_table, aes(timestamp, value)) + geom_line(aes(colour = category))