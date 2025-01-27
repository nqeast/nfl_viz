# NFL Team Passing Yards Rank Progression Visualization

An example **Dash application** visualizing the rank progression of NFL teams based on their total passing yards from 2016 to 2024. This project demonstrates interactive data visualization using Python, Dash, and Plotly.

---

## Features

- **Team Comparison**: Select two NFL teams and compare their rank passing yards rank progression over time.
- **Interactive Animation**: Watch an animated line graph showing rank changes year by year.

---

## Demo
![Passing Yards Comparison](https://github.com/nqeast/nfl_viz/blob/master/Viz_movie-ezgif.com-video-to-gif-converter.gif)


## Code Overview

### Main Components:
- **`app.py`**: The Dash application containing:
  - Dropdowns for team selection.
  - Animated Plotly graph for rank visualization.
- **Dataset**: `team_passing_yards_2016_2024.csv`, which includes:
  - `posteam`: Team name.
  - `year`: Season year.
  - `total_passing_yards`: Passing yards data for each team.
  - `rank`: Rank based on passing yards.

---

### Acknowledgments
- NFLverse/nflfastR: Dataset source.
- Dash and Plotly for making interactive data visualization easy.
