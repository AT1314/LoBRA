---
title: "lect5-logistic-regression-annotated"
date: "2025-02-03"
source: "inbox/lect5-logistic-regression-annotated.pdf"
format: "PDF Document"
pages: "30"
converted: "2025-10-31 10:24:36"
---

# lect5-logistic-regression-annotated

**Pages:** 30


## Page 1

Logistic regression

## Page 2

Uncertainty in prediction
Can we usually expect to get a perfect classiﬁer, if we have enough
training data?
Problem 1: Inherent uncertainty
The available features x do not contain enough information to
perfectly predict y, e.g.,
• x = complete medical record for a patient at risk for a disease
• y = will he/she contract the disease in the next 5 years?

## Page 3

Uncertainty in prediction
Can we usually expect to get a perfect classiﬁer, if we have enough
training data?
Problem 1: Inherent uncertainty
The available features x do not contain enough information to
perfectly predict y, e.g.,
• x = complete medical record for a patient at risk for a disease
• y = will he/she contract the disease in the next 5 years?

## Page 4

Uncertainty in prediction, cont’d
Can we usually expect to get a perfect classiﬁer, if we have enough
training data?
Problem 2: Limitations of the model class
The type of classiﬁer being used does not capture the decision
boundary, e.g. using linear classiﬁers with:


## Page 5

Conditional probability estimation for binary labels
• Given: data set of pairs ( x,y) with x ∈Rd and y ∈{−1,1}
• Return a classiﬁer that also gives probabilities Pr(y = 1|x)
Simplest case: using a linear function of x.


## Page 6

Conditional probability estimation for binary labels
• Given: data set of pairs ( x,y) with x ∈Rd and y ∈{−1,1}
• Return a classiﬁer that also gives probabilities Pr(y = 1|x)
Simplest case: using a linear function of x.


## Page 8

A linear model for conditional probability estimation
For data x ∈Rd , classify and return probabilities using a linear
function
w1x1 + w2x2 + ··· + wd xd + b = w ·x + b
where w = (w1,..., wd ).
The probability of y = 1:
• Increases as the linear function grows.
• Is 50% when this linear function is zero.
How can we convert w ·x + b into a probability?

## Page 9

The squashing function
s(z) = 1
1 + e−z


## Page 10

The logistic regression model
Binary labels y ∈{−1,1}. Model:
Pr(y = 1|x) = 1
1 + e−(w·x+b)
What is Pr(y = −1|x)?

## Page 11

Summary: logistic regression for binary labels
• Data x ∈Rd
• Binary labels y ∈{−1,1}
Model parametrized by w ∈Rd and b ∈R:
Prw,b(y|x) = 1
1 + e−y(w·x+b)
Learn parameters w,b from data

## Page 12

The learning problem
Given data ( x(1),y(1)),..., (x(n),y(n)) ∈Rd ×{−1,1}
Maximum-likelihood: pick w ∈Rd and b ∈R that maximize
n∏
i=1
Prw,b(y(i) |x(i))
Take log to get loss function
L(w,b) = −
n∑
i=1
ln Prw,b(y(i) |x(i)) =
n∑
i=1
ln(1 + e−y(i)(w·x(i)+b))
Goal: minimize L(w,b).
As with linear regression, can absorb b into w.
Yields simpliﬁed loss function L(w).

## Page 13

The learning problem
Given data ( x(1),y(1)),..., (x(n),y(n)) ∈Rd ×{−1,1}
Maximum-likelihood: pick w ∈Rd and b ∈R that maximize
n∏
i=1
Prw,b(y(i) |x(i))
Take log to get loss function
L(w,b) = −
n∑
i=1
ln Prw,b(y(i) |x(i)) =
n∑
i=1
ln(1 + e−y(i)(w·x(i)+b))
Goal: minimize L(w,b).
As with linear regression, can absorb b into w.
Yields simpliﬁed loss function L(w).

## Page 14

The learning problem
Given data ( x(1),y(1)),..., (x(n),y(n)) ∈Rd ×{−1,1}
Maximum-likelihood: pick w ∈Rd and b ∈R that maximize
n∏
i=1
Prw,b(y(i) |x(i))
Take log to get loss function
L(w,b) = −
n∑
i=1
ln Prw,b(y(i) |x(i)) =
n∑
i=1
ln(1 + e−y(i)(w·x(i)+b))
Goal: minimize L(w,b).
As with linear regression, can absorb b into w.
Yields simpliﬁed loss function L(w).

## Page 15

Convexity
• Bad news: no closed-form solution for w
• Good news: L(w) is convex in w
w
L ( w )
w ⇤
How to ﬁnd the minimum of a convex function? By local search.

## Page 16

Convexity
• Bad news: no closed-form solution for w
• Good news: L(w) is convex in w
w
L ( w )
w ⇤
How to ﬁnd the minimum of a convex function? By local search.

## Page 17

Gradient descent procedure for logistic regression
Given (x(1),y(1)),..., (x(n),y(n)) ∈Rd ×{−1,1}, ﬁnd
arg min
w∈Rd
L(w) =
n∑
i=1
ln(1 + e−y(i)(w·x(i)))
• Set w0 = 0
• For t = 0,1,2,... , until convergence:
wt+1 = wt + ηt
n∑
i=1
y(i)x(i) Prwt (−y(i)|x(i))  
doubtt (x(i),y(i))
,
where ηt is a “step size”

## Page 18

Toy example


## Page 19

Toy example


## Page 20

Toy example


## Page 21

Example: Sentiment data
Data set: sentences from reviews on Amazon, Yelp, IMDB.
Each labeled as positive or negative.
• Needless to say, I wasted my money.
• He was very impressed when going from the
original battery to the extended battery.
• I have to jiggle the plug to get it to line up
right to get decent volume.
• Will order from them again!
2500 training sentences, 500 test sentences

## Page 22

Handling text data
Bag-of-words: vectorial representation of text sentences (or
documents).
 It was the best of times, it was the 
worst of times, it was the age of 
wisdom, it was the age of foolishness, 
it was the epoch of belief, it was the 
epoch of incredulity, it was the 
season of Light, it was the season of 
Darkness, it was the spring of hope, 
it was the winter of despair, we had 
everything before us, we had nothing 
before us, we were all going direct to 
Heaven, we were all going direct the 
other way – in short, the period was 
so far like the present period, that 
some of its noisiest authorities 
insisted on its being received, for 
good or for evil, in the superlative 
degree of comparison only.
despair
evil
happiness
foolishness1
1
0
2
• Fix V = some vocabulary.
• Treat each sentence (or document) as a vector of length |V |:
x = (x1,x2,..., x|V |),
where xi = # of times the ith word appears in the sentence.

## Page 23

Handling text data
Bag-of-words: vectorial representation of text sentences (or
documents).
 It was the best of times, it was the 
worst of times, it was the age of 
wisdom, it was the age of foolishness, 
it was the epoch of belief, it was the 
epoch of incredulity, it was the 
season of Light, it was the season of 
Darkness, it was the spring of hope, 
it was the winter of despair, we had 
everything before us, we had nothing 
before us, we were all going direct to 
Heaven, we were all going direct the 
other way – in short, the period was 
so far like the present period, that 
some of its noisiest authorities 
insisted on its being received, for 
good or for evil, in the superlative 
degree of comparison only.
despair
evil
happiness
foolishness1
1
0
2
• Fix V = some vocabulary.
• Treat each sentence (or document) as a vector of length |V |:
x = (x1,x2,..., x|V |),
where xi = # of times the ith word appears in the sentence.

## Page 24

A logistic regression approach
Code positive as +1 and negative as −1.
Prw,b(y |x) = 1
1 + e−y(w·x+b)
Given (x(1),y(1)),..., (x(n),y(n)) ∈Rd ×{−1,1}, loss function
L(w,b) =
n∑
i=1
ln(1 + e−y(i)(w·x(i)+b))
Convex problem with many solution methods, e.g.
• gradient descent, stochastic gradient descent
• Newton-Raphson, quasi-Newton
All converge to the optimal solution.

## Page 25

Local search in progress
Look at how loss function L(w,b) changes over iterations of
stochastic gradient descent.
Final model: test error 0.21.

## Page 26

Local search in progress
Look at how loss function L(w,b) changes over iterations of
stochastic gradient descent.
Final model: test error 0.21.

## Page 27

Some of the mistakes
Not much dialogue, not much music, the whole ﬁlm was shot as
elaborately and aesthetically like a sculpture. 1
This ﬁlm highlights the fundamental ﬂaws of the legal process, that it’s
not about discovering guilt or innocence, but rather, is about who
presents better in court. 1
You need two hands to operate the screen. This software interface is
decade old and cannot compete with new software designs. -1
The last 15 minutes of movie are also not bad as well. 1
If you plan to use this in a car forget about it. -1
If you look for authentic Thai food, go else where. -1
Waste your money on this game. 1

## Page 28

Margin and test error
Margin on test pt x =
⏐⏐⏐⏐Prw,b(y = 1|x) −1
2
⏐⏐⏐⏐ .


## Page 29

Margin and test error
Margin on test pt x =
⏐⏐⏐⏐Prw,b(y = 1|x) −1
2
⏐⏐⏐⏐ .


## Page 30

Interpreting the model
Words with the most positive coeﬃcients
’sturdy’, ’able’, ’happy’, ’disappoint’, ’perfectly’, ’remarkable’, ’animation’,
’recommendation’, ’best’, ’funny’, ’restaurant’, ’job’, ’overly’, ’cute’, ’good’, ’rocks’,
’believable’, ’brilliant’, ’prompt’, ’interesting’, ’skimp’, ’deﬁnitely’, ’comfortable’,
’amazing’, ’tasty’, ’wonderful’, ’excellent’, ’pleased’, ’beautiful’, ’fantastic’,
’delicious’, ’watch’, ’soundtrack’, ’predictable’, ’nice’, ’awesome’, ’perfect’, ’works’,
’loved’, ’enjoyed’, ’love’, ’great’, ’happier’, ’properly’, ’liked’, ’fun’, ’screamy’,
’masculine’
Words with the most negative coeﬃcients
’disappointment’, ’sucked’, ’poor’, ’aren’, ’not’, ’doesn’, ’worst’, ’average’,
’garbage’, ’bit’, ’looking’, ’avoid’, ’roasted’, ’broke’, ’starter’, ’disappointing’, ’dont’,
’waste’, ’ﬁgure’, ’why’, ’sucks’, ’slow’, ’none’, ’directing’, ’stupid’, ’lazy’,
’unrecommended’, ’unreliable’, ’missing’, ’awful’, ’mad’, ’hours’, ’dirty’, ’didn’,
’probably’, ’lame’, ’sorry’, ’horrible’, ’fails’, ’unfortunately’, ’barking’, ’bad’, ’return’,
’issues’, ’rating’, ’started’, ’then’, ’nothing’, ’fair’, ’pay’