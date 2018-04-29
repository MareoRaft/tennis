# tennis

Jeff Sackmann has tons of open-source data about professional tennis on [his GitHub account](https://github.com/JeffSackmann).  Not only does he have a bunch of unanswered [questions about tennis](https://github.com/JeffSackmann/tennis_Research_Notes), I have a few of my own.

As an avid tennis player, I am both motivated to tackle this data and equipped to interpret results in an insightful way.

## Preliminary questions and analysis

### Question 1

Tennis is a mental game.  Can the current score within a game predict outcome?  When I watch tennis on TV, I notice that a score of 0-30 or 15-30 almost always results in the server winning the next point.  Am I correct or crazy?

![](score-to-win.png)

(data from `JeffSackmann/tennis_MatchChartingProject > charting-m-points.csv` which lists about 300,000 tennis points coming from about 2,000 men's matches)

The data says that I'm crazy!  But it also points out a surprising result.  Servers in the 40-AD situation are much more likely to lose the next point.  The sheer amount of data and the very low 40-AD probability is enough to conclude significance.  A Chi-squared test confirms this with a p-value so low that numpy rounds it down to 0.

The interesting thing about this is that the 40-AD score and the 30-40 score are arguably identical situations.  Both scores result in losing the game if the next point is lost, and both scores result in 40-40 if the next point is won.  But the data shows that these situations are psychologically different.  Servers in the 40-AD position have been serving for a longer amount of time and weren't able to close out the game sooner.  Returners in that position may be tough-customers who are chomping at the bit to steal the game from the server.

When I initially ran this graph, I only ran it on the first 200 data points.  The results were very different:

![](score-to-win-querrey-anderson.png)

These results seem to confirm my suspicion for servers reacting strongly to a 0-30 situation (but is inconclusive with a Chi-squared test p-value of 0.086).  It turns out that the first 200 data points correspond to a match between Sam Querrey and Kevin Anderson.  Sam Querrey is a very strong server.  Is it possible that this correlation holds for strong servers in general?  Can we find more patterns if we cluster our players into different categories?  This leads into the next question.

### Question 2

Do players cluster into nice 'player types', and are certain player clusters more successful?

For example, I predict that a heavier player is more likely to have a heavier racket and a one-handed backhand.  On the other hand, I predict a lighter player will have a two-handed backhand, be a faster runner and a better returner, and have a weaker serve.

Am I correct about the existance of these two clusters?  Are there more clusters?  There are many dimensions to consider, including weight, height, lefty/righty, one-handed-backhand/two-handed-backhand, racket weight, and racket string-pattern.  These dimensions can be split into two categories: the "independent" dimensions (like height) that are outside of the player's control, and the "dependent" dimensions (like racket string-pattern) that are the player's choice.

### Question 3

Is there a correlation between different player types / play styles and the types of injuries that those players get?  What exactly are those correlations?  I will probably not pursue this question because I have yet to find good data on tennis injuries.

### Question 4

Are serve-and-volleyers streakier than others?  This question was posed by Jeff Sackman in his [questions about tennis](https://github.com/JeffSackmann/tennis_Research_Notes).  This question may be easy to answer because it uses a lot of the same machinery as the score calculation above.

TODO: try the streakier result
TODO: try the cluster result

### Question 5

Going back to the "score to win-next-point" analysis and the thought that certain types of players (such as the "big server" Sam Querrey) may behave differently in certain situations, it gave me the idea to run a "score to ace" analysis in much the same way.

(NTS: are we looking at wrong Pts score?  I don't think so.  I think the Pts refers to the score BEFORE the point starts and Pts after refers to score AFTER end of point).

The results are again quite interesting.  Looking at all the matches,

![](score-to-ace.png)

there is a correlation between aces and the scores 30-0, 40-0, and 40-15.  This suggests that when the server is ahead, he is confident, more willing to take risks, and more likely to hit an ace.  (A Chi-squared test on the 40-0 situation yields a p-value near 0.)

Now, zooming in on the match between Sam Querrey and Kevin Anderson, we have some similarities and differences.

![](score-to-ace-querrey-anderson.png)

This time, there is a surprisingly high probability for 15-40, which suggests that Querrey is in a desperate/high-pressure situation, and willing to take risks.  There are also *no* aces for the 15-15 and 30-30 situations.  (A Chi-squared test on the 15-40 situation yields a p-value of 0.25, which is inconclusive.  Remember that there are only 200 data points in this match.  We could aggregate more data on Sam Querrey to get a conclusive answer.)




NTS: look at https://stackoverflow.com/questions/41710789/boolean-series-key-will-be-reindexed-to-match-dataframe-index#41715287
