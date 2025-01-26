# load libraries
library(nflfastR)
library(dplyr)
library(ggplot2)
library(tidyr)
library(purrr)
library(stringr)
library(readr)

# Load play by play data
pbp_24 <- load_pbp(2024)
pbp_23 <- load_pbp(2023)
pbp_22 <- load_pbp(2022)
pbp_21 <- load_pbp(2021)
pbp_20 <- load_pbp(2020)
pbp_19 <- load_pbp(2019)
pbp_18 <- load_pbp(2018)
pbp_17 <- load_pbp(2017)
pbp_16 <- load_pbp(2016)

# Look at heda of dataset
head(pbp_24)

# check structure
str(pbp_24)

# see last updated
max(pbp_24$game_date, na.rm = TRUE)

# column names
colnames(pbp_24)

# passer stats for 24 reg season total yards
passer_stats_24 <- pbp_24 %>%
  filter(season_type == "REG") %>%  # Filter for regular season games
  group_by(passer_id) %>%          # Group by passer_id
  summarise(total_passing_yards = sum(passing_yards, na.rm = TRUE)) %>%  # Sum passing yards
  arrange(desc(total_passing_yards))

# view head and verify stats match nfl site stats
head(passer_stats_24)

#Group by possesion team pass yards
team_passing_stats_24 <- pbp_24 %>%
  filter(season_type == "REG") %>%  # Filter for regular season games
  group_by(posteam) %>%            # Group by posteam
  summarise(total_passing_yards = sum(passing_yards, na.rm = TRUE)) %>%  # Sum passing yards
  arrange(desc(total_passing_yards))

head(team_passing_stats_24)


# Initialize an empty list to store the results
team_passing_list <- list()

# Loop through the years 2016 to 2024
for (year in 2016:2024) {
  # Dynamically get the pbp data frame name
  df_name <- paste0("pbp_", substr(year, 3, 4)) # e.g., "pbp_24", "pbp_16"
  pbp_data <- get(df_name)  # Retrieve the data frame from the environment
  
  # Group and summarize passing yards by team for season_type = "REG"
  team_passing_stats <- pbp_data %>%
    filter(season_type == "REG") %>%
    group_by(posteam) %>%
    summarise(total_passing_yards = sum(passing_yards, na.rm = TRUE)) %>%
    mutate(year = year)  # Add a column for the year
  
  # Add the result to the list
  team_passing_list[[as.character(year)]] <- team_passing_stats
}

# Combine all the yearly results into a single data frame
all_team_passing <- bind_rows(team_passing_list)

head(all_team_passing)

# Define the file path where you want to save the CSV file
output_file <- "team_passing_yards_2016_2024.csv"

# Export the data frame to a CSV file
write.csv(all_team_passing, file = output_file, row.names = FALSE)

# Confirm the file path
cat("Data exported to:", output_file)

