# Tommy John Surgery Prediction

Trying to predict if which pitchers need Tommy John in the future 
and/or develop a metric to determine which pitchers are most at risk.

## TODO List

### Todo

- [ ] Stats (2 weeks)
  - [ ] Fetching all necessary stats associated with a player from statcast
    - Possible factors that can influence TJ:
      - Std of release point
      - Average fastball velocity
      - Spin rate
      - % of pitches thrown as breaking
      - IP
      - Pitch Tempo
      - Previous injury history
      - Days missed due to injury
      - Previous TJS flag
      - Average length of outing (IP/game; pitches/game)
- [ ] Model (2 weeks)
  - [ ] Research what model to use
    - Initial thoughts:
      - Decision trees? <-- prob most likely to use
      - Regression?
      - Naive Bayes?
      - SVM?
      - Even neural nets/deep learning if I'm feeling it
 

### In Progress

- [ ] Stats

### Done ✓

- [x] Injury Dataset (at MVP level)
  - [x] Scraped all injuries (i.e., determined when players were placed on ILs) 
        since 2008 season
  - [x] Developed NLP model to get injury types + type of IL
    - 96.9% accuracy
  - [x] Featurized the injury dataset
  - [x] Cross-referenced players to their bbref id
  - [x] Got amount of time on IL ("relinquished" data minus "acquired" date)

### Further refining needed
- [ ] Injury Dataset
  - [ ] Improving NLP Model

