#!/usr/bin/env Rscript

# Parsing command line arguments:
options = commandArgs(trailingOnly = TRUE)
filename = options[1]
table_header = options[-1]

# Loading files:
table = read.csv(filename, header = FALSE, row.names = length(table_header) + 1) # The last column of the table gives the timestamp, thus the row names

# Setting up the table so it can be plotted:
colnames(table) = table_header
# Transposing for bar plotting:
table = t(as.matrix(table))

# Plotting:
barplot(table)