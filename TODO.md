# TODO List

### Todo

- [ ] Injury Dataset (1 week)
  - [ ] Use NLP model to get injury types + type of IL
    - Maybe even severity of injury -- like if surgery was needed
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

- [ ] Injury Dataset
  - [ ] Cross-referencing players to their bbref id
  - [ ] Get amount of time on IL ("relinquished" data minus "acquired" date)

### Done ✓

- [x] Scraped all injuries (i.e., determined when players were placed on ILs) 
      since 2008 season

