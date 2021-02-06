# Tennis Capstone Project

This is the repo for my Tennis Capstone Project for The Data Incubator.  The actual [**deployed web app** is here](http://162.243.168.182:5001/).  The repo for the [backend is here](https://github.com/MareoRaft/tennis-backend).    Please go to the [developer README](https://github.com/MareoRaft/tennis-frontend-tdi/blob/master/README.dev.md) if you want to actually develop or deploy the app.  Read on for an in-depth description of the project.




## Business Objective

Bring insightful tennis stats to tennis fans.

Tennis is the 4th most popular sport in the world [[1]](https://www.totalsportek.com/most-popular-sports/).  The objective is to bring valuable information and insights about professional players to fans.

Information is valuable.  We will provide both data and predictions to people through interactive visualizations.  In addition to tennis hobbyists, people who gamble on tennis would find the info particularly beneficial.  Professional tennis players themselves would find the info helpful in developing potential weaknesses to improve or exploit.

The [web app](http://162.243.168.182:5001/) could be monetized by offering basic features for free and charging for advanced features.  For example, the basic version may only allow you to compare at most 5 players, but the advanced version may allow you to compare 14.



## Data Ingestion

Data will be combined, processed, and updated periodically.

The data comes from two CSV files that are posted at [[2]](https://github.com/JeffSackmann/tennis_MatchChartingProject).  I plan to add match-level stats in the future which will require additional data from [[2]](https://github.com/JeffSackmann/tennis_MatchChartingProject), [[3]](https://github.com/JeffSackmann/tennis_wta), [[4]](https://github.com/JeffSackmann/tennis_atp), [[5]](https://github.com/JeffSackmann/tennis_slam_pointbypoint), or [[6]](https://github.com/JeffSackmann/tennis_pointbypoint).

The data is loaded with pandas, widdled down, combined, and processed into the information we need.  In particular, text-splitting and regular expressions are used to pull player info out of 1 column [here](https://github.com/MareoRaft/tennis-backend/blob/master/data_ingestion/ingest_points.py#L31); maps are used to create new columns from existing column combinations; and then data is aggregated per-player [here](https://github.com/MareoRaft/tennis-backend/blob/master/analysis/stat.py#L9).  For the [PageRank](https://en.wikipedia.org/wiki/PageRank) algorithm (see code [here](https://github.com/MareoRaft/tennis-backend/blob/master/analysis/pagerank.py)), point result information is aggregated per player-pair and a weighted directed graph is created.  Networkx then computes the pagerank.

The ingestion pipeline is fully automated (it is enough to run [this function](https://github.com/MareoRaft/tennis-backend/blob/master/data_ingestion/ingest_points.py#L82)) and I plan to rerun it periodically on the latest-and-greatest professional tennis data (the source data is updated every few months).



## Visualizations

The project contains a bar chart which is used for both the stats-comparisons and the PageRank comparison.  There exist 6 controls for interacting with the data as well as the zoom-interactivity of the amChart itself.  You can view it [here](http://162.243.168.182:5001/).



## Interactive Website

Users interact with the project via a website.  Users explore the data by choosing a (1) statistic, (2) normalization, (3) gender, and some other options.  Users can click on info buttons to get explanations of the various choices and methods used to compute the data.  Users can click and drag on the chart to see cross sections of the view.

The user interactivity is client-side, and the client will make calls to the server to update the data as necessary.  Tools used to achieve this include [JavaScript](https://www.w3schools.com/js/default.asp), [React](https://create-react-app.dev/), [Material-UI](https://material-ui.com/), [amCharts](https://www.amcharts.com/), [Python](https://www.python.org/) 3, [Flask](https://palletsprojects.com/p/flask/), [Pandas](https://pandas.pydata.org/), and [Networkx](https://networkx.org/).



## Deliverable

The above already describes the work done on the capstone, the tools used, and the data ingestion; but not the analysis and results.  I will include those below.  The deliverable is this very [repository](https://github.com/MareoRaft/tennis-frontend-tdi) and this very README.md file.  Point 3 includes a link to the visualizations.



## Analysis and Results

The statistics are calculated as follows:

"**Points won**" is the number of points a player has won.  When normalized by percentage, it is divided by the number of points they have played.  **Service points won** is the number of points a player won when serving.  As a percentage, the denominator is the total number of service points they played.  **Aces** is the number of aces a player hit.  As a percentage, the denominator is the number of service points they played.  **Double faults** is the number of double faults the player had.  As a percentage, the denominator is the number of service points they played.

**The GOAT algorithm** is the Google PageRank algorithm applied to the following graph definition:  Each player is represented by exactly 1 node.  If `A` and `B` are nodes, then the directed edge `(A, B)` has an integer weight which is the number of points that player A lost to player B.

The **time decay** normalization is the same as the percentage normalization with the following difference:  More recent points are weighted higher than points that happened a long time ago.  We use a 1-year half-life exponential decay function, so that a point that occurred 1 year ago is only worth half as much as a point that happened today.  In the **percent** normalization, a single point contributes 1 to the denominator and either 1 or 0 to the numerator.  In the **time decay** normalization, a single point that occured `y` years ago contributes `(1/2)^y` to the denominator and either `(1/2)^y` or `0` to the numerator.

The following are some selected results from the analysis:

stat: | aces | double-faults | points-won | The GOAT Algorithm
---:|---:|---:|---:|---:
normalization: | percent | percent | percent | raw count
`#1` player: | Ivo Karlovic `13.5%` |  Goran Ivanisevic `4.1%` | Evgeny Donskoy `55.7%` | Roger Federer `4.5%`
`#2` player: | Goran Ivanisevic `9.7%` | Noah Rubin `4.0%` | Thomas Muster `54.6%` | Rafael Nadal `3.1%`
`#3` player: | John Isner `9.7%` | Matthew Ebden `4.0%` | Igor Sijsling `54.5%` | Novak Djokovic `2.7%`



