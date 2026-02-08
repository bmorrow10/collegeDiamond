library(DBI)
library(RSQLite)
library(ggplot2)

con <- dbConnect(RSQLite::SQLite(), "college_baseball.db")

df <- dbGetQuery(con, "
  SELECT p.name, b.hr
  FROM players p
  JOIN batting_stats b ON p.id = b.player_id
")

ggplot(df, aes(x=reorder(name, hr), y=hr)) +
  geom_bar(stat="identity") +
  coord_flip() +
  labs(title="Home Runs Leaderboard")
