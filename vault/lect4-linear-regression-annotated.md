---
title: "lect4-linear-regression-annotated"
date: "2025-02-03"
source: "inbox/lect4-linear-regression-annotated.pdf"
format: "PDF Document"
pages: "40"
converted: "2025-10-31 10:24:35"
---

# lect4-linear-regression-annotated

**Pages:** 40


## Page 1

Linear regression

## Page 2

Linear regression
Fitting a line to a bunch of points.

## Page 3

Example: college GPAs
Distribution of GPAs of
students at a certain Ivy
League university.
What GPA to predict for a random student from this group?
• Without further information, predict the mean, 2.47.
• What is the average squared error of this prediction?
That is, E[((student’s GPA) −(predicted GPA))2]?
The variance of the distribution, 0.55.

## Page 4

Example: college GPAs
Distribution of GPAs of
students at a certain Ivy
League university.
What GPA to predict for a random student from this group?
• Without further information, predict the mean, 2.47.
• What is the average squared error of this prediction?
That is, E[((student’s GPA) −(predicted GPA))2]?
The variance of the distribution, 0.55.

## Page 5

Example: college GPAs
Distribution of GPAs of
students at a certain Ivy
League university.
What GPA to predict for a random student from this group?
• Without further information, predict the mean, 2.47.
• What is the average squared error of this prediction?
That is, E[((student’s GPA) −(predicted GPA))2]?
The variance of the distribution, 0.55.

## Page 6

Example: college GPAs
Distribution of GPAs of
students at a certain Ivy
League university.
What GPA to predict for a random student from this group?
• Without further information, predict the mean, 2.47.
• What is the average squared error of this prediction?
That is, E[((student’s GPA) −(predicted GPA))2]?
The variance of the distribution, 0.55.

## Page 7

Example: college GPAs
Distribution of GPAs of
students at a certain Ivy
League university.
What GPA to predict for a random student from this group?
• Without further information, predict the mean, 2.47.
• What is the average squared error of this prediction?
That is, E[((student’s GPA) −(predicted GPA))2]?
The variance of the distribution, 0.55.

## Page 8

Better predictions with more information
We also have SAT scores of all students.
Mean squared error
(MSE) drops to 0.43.
This is a regression problem with:
• Predictor variable: SAT score
• Response variable: College GPA

## Page 9

Better predictions with more information
We also have SAT scores of all students.
Mean squared error
(MSE) drops to 0.43.
This is a regression problem with:
• Predictor variable: SAT score
• Response variable: College GPA

## Page 10

Better predictions with more information
We also have SAT scores of all students.
Mean squared error
(MSE) drops to 0.43.
This is a regression problem with:
• Predictor variable: SAT score
• Response variable: College GPA

## Page 11

Better predictions with more information
We also have SAT scores of all students.
Mean squared error
(MSE) drops to 0.43.
This is a regression problem with:
• Predictor variable: SAT score
• Response variable: College GPA

## Page 12

Parametrizing a line
A line can be parameterized as y = ax + b (a: slope, b: intercept).

## Page 13

The line ﬁtting problem
Pick a line ( a,b) based on ( x(1),y(1)),..., (x(n),y(n)) ∈R ×R
• x(i),y(i) are predictor and response variables.
E.g. SAT score, GPA of ith student.
• Minimize the mean squared error,
MSE(a,b) = 1
n
n∑
i=1
(y(i) −(ax(i) + b))2.
This is the loss function.

## Page 14

Minimizing the loss function
Given (x(1),y(1)),..., (x(n),y(n)), minimize
L(a,b) =
n∑
i=1
(y(i) −(ax(i) + b))2.

## Page 16

Multivariate regression: diabetes study
Data from n = 442 diabetes patients.
For each patient:
• 10 features x = (x1,..., x10)
age, sex, body mass index, average blood pressure,
and six blood serum measurements.
• A real value y: the progression of the disease a year later.
Regression problem:
• response y ∈R
• predictor variables x ∈R10

## Page 17

Least-squares regression
Linear function of 10 variables: for x ∈R10,
f (x) = w1x1 + w2x2 + ··· + w10x10 + b = w ·x + b
where w = (w1,w2,..., w10).
Penalize error using squared loss (y −(w ·x + b))2.
Least-squares regression:
• Given: data (x(1),y(1)),..., (x(n),y(n)) ∈Rd ×R
• Return: linear function given by w ∈Rd and b ∈R
• Goal: minimize the loss function
L(w,b) =
n∑
i=1
(y(i) −(w ·x(i) + b))2.

## Page 18

Least-squares regression
Linear function of 10 variables: for x ∈R10,
f (x) = w1x1 + w2x2 + ··· + w10x10 + b = w ·x + b
where w = (w1,w2,..., w10).
Penalize error using squared loss (y −(w ·x + b))2.
Least-squares regression:
• Given: data (x(1),y(1)),..., (x(n),y(n)) ∈Rd ×R
• Return: linear function given by w ∈Rd and b ∈R
• Goal: minimize the loss function
L(w,b) =
n∑
i=1
(y(i) −(w ·x(i) + b))2.

## Page 19

Least-squares regression
Linear function of 10 variables: for x ∈R10,
f (x) = w1x1 + w2x2 + ··· + w10x10 + b = w ·x + b
where w = (w1,w2,..., w10).
Penalize error using squared loss (y −(w ·x + b))2.
Least-squares regression:
• Given: data (x(1),y(1)),..., (x(n),y(n)) ∈Rd ×R
• Return: linear function given by w ∈Rd and b ∈R
• Goal: minimize the loss function
L(w,b) =
n∑
i=1
(y(i) −(w ·x(i) + b))2.

## Page 20

Back to the diabetes data
• No predictor variables: mean squared error (MSE) = 5930
• One predictor (’bmi’): MSE = 3890
• Two predictors (’bmi’, ’serum5’): MSE = 3205
• All ten predictors: MSE = 2860

## Page 21

Back to the diabetes data
• No predictor variables: mean squared error (MSE) = 5930
• One predictor (’bmi’): MSE = 3890
• Two predictors (’bmi’, ’serum5’): MSE = 3205
• All ten predictors: MSE = 2860

## Page 22

Back to the diabetes data
• No predictor variables: mean squared error (MSE) = 5930
• One predictor (’bmi’): MSE = 3890
• Two predictors (’bmi’, ’serum5’): MSE = 3205
• All ten predictors: MSE = 2860

## Page 23

Back to the diabetes data
• No predictor variables: mean squared error (MSE) = 5930
• One predictor (’bmi’): MSE = 3890
• Two predictors (’bmi’, ’serum5’): MSE = 3205
• All ten predictors: MSE = 2860

## Page 24

Least-squares solution 1
Linear function of d variables given by w ∈Rd and b ∈R:
f (x) = w1x1 + w2x2 + ··· + wd xd + b = w ·x + b
Assimilate the intercept b into w:
• Add a new feature that is identically 1: let ˜x = (1,x) ∈Rd+1
(
4 0 2 ··· 3
)
=⇒
(
1 4 0 2 ··· 3
)
• Set ˜w = (b,w) ∈Rd+1
• Then f (x) = w ·x + b = ˜w ·˜x
Goal: ﬁnd ˜w ∈Rd+1 that minimizes
L( ˜w) =
n∑
i=1
(y(i) −˜w ·˜x(i))2

## Page 25

Least-squares solution 1
Linear function of d variables given by w ∈Rd and b ∈R:
f (x) = w1x1 + w2x2 + ··· + wd xd + b = w ·x + b
Assimilate the intercept b into w:
• Add a new feature that is identically 1: let ˜x = (1,x) ∈Rd+1
(
4 0 2 ··· 3
)
=⇒
(
1 4 0 2 ··· 3
)
• Set ˜w = (b,w) ∈Rd+1
• Then f (x) = w ·x + b = ˜w ·˜x
Goal: ﬁnd ˜w ∈Rd+1 that minimizes
L( ˜w) =
n∑
i=1
(y(i) −˜w ·˜x(i))2

## Page 26

Least-squares solution 2
Write
X =


←−−−−˜x(1) −−−−→
←−−−−˜x(2) −−−−→
...
←−−−−˜x(n) −−−−→

, y =


y(1)
y(2)
...
y(n)


Then the loss function is
L( ˜w) =
n∑
i=1
(y(i) −˜w ·˜x(i))2 = ∥y −X ˜w∥2
and it minimized at ˜w = (X T X )−1(X T y).

## Page 27

Generalization behavior of least-squares regression
Given a training set (x(1),y(1)),..., (x(n),y(n)) ∈Rd ×R, ﬁnd a
linear function, given by w ∈Rd and b ∈R, that minimizes the
squared loss
L(w,b) =
n∑
i=1
(y(i) −(w ·x(i) + b))2.
Is training loss a good estimate of future performance?
• If n is large enough: maybe.
• Otherwise: probably an underestimate.

## Page 28

Generalization behavior of least-squares regression
Given a training set (x(1),y(1)),..., (x(n),y(n)) ∈Rd ×R, ﬁnd a
linear function, given by w ∈Rd and b ∈R, that minimizes the
squared loss
L(w,b) =
n∑
i=1
(y(i) −(w ·x(i) + b))2.
Is training loss a good estimate of future performance?
• If n is large enough: maybe.
• Otherwise: probably an underestimate.

## Page 29

Example


## Page 30

Example


## Page 31

Example


## Page 32

Example


## Page 33

Better error estimates
Recall: k-fold cross-validation
• Divide the data set into k equal-sized groups S1,..., Sk
• For i = 1 to k:
• Train a regressor on all data except Si
• Let Ei be its error on Si
• Error estimate: average of E1,..., Ek
A nagging question:
When n is small, should we be minimizing the squared loss?
L(w,b) =
n∑
i=1
(y(i) −(w ·x(i) + b))2

## Page 34

Better error estimates
Recall: k-fold cross-validation
• Divide the data set into k equal-sized groups S1,..., Sk
• For i = 1 to k:
• Train a regressor on all data except Si
• Let Ei be its error on Si
• Error estimate: average of E1,..., Ek
A nagging question:
When n is small, should we be minimizing the squared loss?
L(w,b) =
n∑
i=1
(y(i) −(w ·x(i) + b))2

## Page 35

Ridge regression
Minimize squared loss plus a term that penalizes “complex” w:
L(w,b) =
n∑
i=1
(y(i) −(w ·x(i) + b))2 + λ∥w∥2
Adding a penalty term like this is called regularization.
Put predictor vectors in matrix X and responses in vector y:
w = (X T X + λI )−1(X T y)

## Page 36

Ridge regression
Minimize squared loss plus a term that penalizes “complex” w:
L(w,b) =
n∑
i=1
(y(i) −(w ·x(i) + b))2 + λ∥w∥2
Adding a penalty term like this is called regularization.
Put predictor vectors in matrix X and responses in vector y:
w = (X T X + λI )−1(X T y)

## Page 37

Toy example
Training, test sets of 100 points
• x ∈R100, each feature xi is Gaussian N(0,1)
• y = x1 + ··· + x10 + N(0,1)
λ training MSE test MSE
0.00001 0.00 585.81
0.0001 0.00 564.28
0.001 0.00 404.08
0.01 0.01 83.48
0.1 0.03 19.26
1.0 0.07 7.02
10.0 0.35 2.84
100.0 2.40 5.79
1000.0 8.19 10.97
10000.0 10.83 12.63

## Page 38

Toy example
Training, test sets of 100 points
• x ∈R100, each feature xi is Gaussian N(0,1)
• y = x1 + ··· + x10 + N(0,1)
λ training MSE test MSE
0.00001 0.00 585.81
0.0001 0.00 564.28
0.001 0.00 404.08
0.01 0.01 83.48
0.1 0.03 19.26
1.0 0.07 7.02
10.0 0.35 2.84
100.0 2.40 5.79
1000.0 8.19 10.97
10000.0 10.83 12.63

## Page 39

The lasso
Popular “shrinkage” estimators:
• Ridge regression
L(w,b) =
n∑
i=1
(y(i) −(w ·x(i) + b))2 + λ∥w∥2
2
• Lasso: tends to produce sparse w
L(w,b) =
n∑
i=1
(y(i) −(w ·x(i) + b))2 + λ∥w∥1
Toy example:
Lasso recovers 10 relevant features plus a few more.

## Page 40

The lasso
Popular “shrinkage” estimators:
• Ridge regression
L(w,b) =
n∑
i=1
(y(i) −(w ·x(i) + b))2 + λ∥w∥2
2
• Lasso: tends to produce sparse w
L(w,b) =
n∑
i=1
(y(i) −(w ·x(i) + b))2 + λ∥w∥1
Toy example:
Lasso recovers 10 relevant features plus a few more.