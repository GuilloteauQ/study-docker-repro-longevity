#!/usr/bin/env Rscript

# Libraries:
library(tidyverse)

# Parsing command line arguments:
options = commandArgs(trailingOnly = TRUE)
filename = options[1]
table_header = options[-1]

# Loading files:
table = read.csv(filename, col_names = table_header, row.names = length(table_header)) # The last column of the table gives the timestamp, thus the row names

# Setting up the table so it can be plotted:
# Transposing for bar plotting:
table = t(as.matrix(table))

# Plotting:
barplot(table)
# legend("topright", legend = c("Level 1", "Level 2"), fill = c("red", "darkblue"))

# read.csv(filename, col_names = table_header, row.names = length(table_header) + 1) %>% # The last column of the table gives the timestamp, thus the row names
#     mutate(timestamp = as_date(as_datetime(timestamp))) %>% # Formatting the date
#     as.matrix() %>% # Converting to matrix to transpose
#     t() %>% # Transposing for bar plotting
#     barplot()