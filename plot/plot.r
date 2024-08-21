#!/usr/bin/env Rscript

# Libraries:
library(reshape2)
library(tidyverse)

# Parsing command line arguments:
options = commandArgs(trailingOnly = TRUE)
plot_type = options[1]
input = options[2]
output = options[3]
table_header = options[-1:-2:-3]

pdf(output)

read_csv(input, col_names = table_header) %>%
    mutate(timestamp = as_date(as_datetime(timestamp))) %>% # Formatting the date
    melt(id.vars = "timestamp", variable.name = "category", value.name = "amount") %>% # Formatting the table to plot each category
    {
        if (plot_type == "bar")
            ggplot(data = ., aes(x = timestamp, y = amount, fill = category)) + geom_bar(stat = "identity")
        else if (plot_type == "line")
            ggplot(data = ., aes(x = timestamp, y = amount)) + geom_line(aes(color = category))
    }
