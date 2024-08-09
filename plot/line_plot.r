#!/usr/bin/env Rscript

# Libraries:
library(reshape2)
library(tidyverse)

# Parsing command line arguments:
options = commandArgs(trailingOnly = TRUE)
filename = options[1]
table_header = options[-1]

read_csv(filename, col_names=table_header) %>%
    mutate(timestamp = as_date(as_datetime(timestamp))) %>% # Formatting the date
    melt(id.vars = "timestamp", variable.name = "category", value.name = "amount") %>% # Formatting the table to plot each category
    ggplot(aes(x = timestamp, y = amount)) +
    geom_line(aes(color = category))
