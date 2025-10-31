---
title: "lect3-the-statistical-learning-framework-annotated"
date: "2025-01-16"
source: "inbox/lect3-the-statistical-learning-framework-annotated.pdf"
format: "PDF Document"
pages: "61"
converted: "2025-10-31 10:24:35"
---

# lect3-the-statistical-learning-framework-annotated

**Pages:** 61


## Page 1

The Statistical Learning 
Framework
CSE 251A Winter 2022
Instructor: Taylor Berg-Kirkpatrick
Based on notes by Sanjoy Dasgupta & Kamalika Chaudhuri

## Page 2

The Underlying Distribution
• The big question: in what situations does training 
data help us develop a model that will work well on 
future data?

## Page 3

The Underlying Distribution
• The big question: in what situations does training 
data help us develop a model that will work well on 
future data?
• What is the link between the two?

## Page 4

The Underlying Distribution
• The big question: in what situations does training 
data help us develop a model that will work well on 
future data?
• What is the link between the two?
• One such setting:  when the statistical learning 
assumption holds.

## Page 5

The Underlying Distribution
• The big question: in what situations does training 
data help us develop a model that will work well on 
future data?
• What is the link between the two?
• One such setting:  when the statistical learning 
assumption holds.
•Assumption: All data (past, present, and future) is 
drawn i.i.d. (independent and identically distributed) 
from some (unknown) underlying distribution on 
.𝒳 × 𝒴

## Page 6

The Underlying Distribution
• Call this distribution .P

## Page 7

The Underlying Distribution
• Call this distribution .P
•e.g. Want to predict whether ER waiting room 
patients have the ﬂy, based on age and temperature.

## Page 8

The Underlying Distribution
• Call this distribution .P
•e.g. Want to predict whether ER waiting room 
patients have the ﬂy, based on age and temperature.
: (age, temp)        x 𝒳 = {0,… ,100} × {97,98,… ,105}

## Page 9

The Underlying Distribution
• Call this distribution .P
•e.g. Want to predict whether ER waiting room 
patients have the ﬂy, based on age and temperature.
: (age, temp)        x 𝒳 = {0,… ,100} × {97,98,… ,105}
: 0 (no ﬂu) or 1 (ﬂu)            y 𝒴 = {0,1}

## Page 10

The Underlying Distribution
• Call this distribution .P
•e.g. Want to predict whether ER waiting room 
patients have the ﬂy, based on age and temperature.
: (age, temp)        x 𝒳 = {0,… ,100} × {97,98,… ,105}
: 0 (no ﬂu) or 1 (ﬂu)            y 𝒴 = {0,1}
As we get more training data, we 
get a better idea of .P
age
temp −
++
+
+++
+
+++
−−−
−
−
−
− −−
−
−

## Page 11

The Underlying Distribution
• Three ways to sample from P

## Page 12

The Underlying Distribution
• Three ways to sample from P
1. Draw (x, y) ∼ P

## Page 13

The Underlying Distribution
• Three ways to sample from P
1. Draw (x, y) ∼ P
2. Draw  according to its marginal distribution.         
Then draw  according to the conditional distribution 
of .
y
x
x| y

## Page 14

The Underlying Distribution
• Three ways to sample from P
1. Draw (x, y) ∼ P
2. Draw  according to its marginal distribution.         
Then draw  according to the conditional distribution 
of .
y
x
x| y
3. Draw  according to its marginal distribution.       
Then draw  according to the conditional distribution 
of .
x
y
y| x

## Page 15

The Underlying Distribution
• Deﬁne:
 distribution on μ : 𝒳
 conditional distribution η : y| x

## Page 16

The Underlying Distribution
• Deﬁne:
 distribution on μ : 𝒳
 conditional distribution η : y| x
• Example:
𝒴 = {0,1}
age
temp
105
97
0 100
𝒳 =

## Page 17

The Underlying Distribution
• Deﬁne:
 distribution on μ : 𝒳
 conditional distribution η : y| x
• Example:
Maybe:   : uniform distribution on   μ 𝒳 μ(x) = 1
900 ∀x ∈ 𝒳
𝒴 = {0,1}
age
temp
105
97
0 100
𝒳 =

## Page 18

The Underlying Distribution
• Deﬁne:
 distribution on μ : 𝒳
 conditional distribution η : y| x
• Example:
Maybe:   : uniform distribution on   μ 𝒳 μ(x) = 1
900 ∀x ∈ 𝒳
             η(x) = Pr(y = 1| x) ∈ [0,1]
𝒴 = {0,1}
age
temp
105
97
0 100
𝒳 =

## Page 19

The Underlying Distribution
• Deﬁne:
 distribution on μ : 𝒳
 conditional distribution η : y| x
• Example:
Maybe:   : uniform distribution on   μ 𝒳 μ(x) = 1
900 ∀x ∈ 𝒳
             η(x) = Pr(y = 1| x) ∈ [0,1]
•Why isn't  either 0 or 1?η(x)
𝒴 = {0,1}
age
temp
105
97
0 100
𝒳 =

## Page 20

The Underlying Distribution
• Deﬁne:
 distribution on μ : 𝒳
 conditional distribution η : y| x
• Example:
Maybe:   : uniform distribution on   μ 𝒳 μ(x) = 1
900 ∀x ∈ 𝒳
             η(x) = Pr(y = 1| x) ∈ [0,1]
•Why isn't  either 0 or 1?η(x)
•Sometimes it is -- e.g. MNIST digit classiﬁcation
𝒴 = {0,1}
age
temp
105
97
0 100
𝒳 =

## Page 21

The Underlying Distribution
• Deﬁne:
 distribution on μ : 𝒳
 conditional distribution η : y| x
• Example:
Maybe:   : uniform distribution on   μ 𝒳 μ(x) = 1
900 ∀x ∈ 𝒳
             η(x) = Pr(y = 1| x) ∈ [0,1]
•Why isn't  either 0 or 1?η(x)
•Sometimes it is -- e.g. MNIST digit classiﬁcation
•In other cases, there is inherent uncertainty.
𝒴 = {0,1}
age
temp
105
97
0 100
𝒳 =

## Page 22

Risk
• Classiﬁer:   h : 𝒳 → 𝒴

## Page 23

Risk
• Classiﬁer:   h : 𝒳 → 𝒴
• Risk:    R(h) = Pr(x,y)∼P(h(x) ≠ y)

## Page 24

Risk
• Classiﬁer:   h : 𝒳 → 𝒴
• Risk:    R(h) = Pr(x,y)∼P(h(x) ≠ y)
• Bayes-optimal classiﬁer:    with smallest 
possible risk
h* : 𝒳 → 𝒴

## Page 25

Risk
• Classiﬁer:   h : 𝒳 → 𝒴
• Risk:    R(h) = Pr(x,y)∼P(h(x) ≠ y)
• Bayes-optimal classiﬁer:    with smallest 
possible risk
h* : 𝒳 → 𝒴
When ,   𝒴 = {0,1} h*(x) = {
1 if η(x) ≥ 1
2
0 otherwise

## Page 26

Risk
• Classiﬁer:   h : 𝒳 → 𝒴
• Risk:    R(h) = Pr(x,y)∼P(h(x) ≠ y)
• Bayes-optimal classiﬁer:    with smallest 
possible risk
h* : 𝒳 → 𝒴
When ,   𝒴 = {0,1} h*(x) = {
1 if η(x) ≥ 1
2
0 otherwise
Bayes' risk:    R* = R(h*) = 𝔼[ min (η(x),1 − η(x))]

## Page 27

Consistency
• Let's say we have a learning algorithm that returns 
classiﬁer  after seeing  training pointshn n

## Page 28

Consistency
• Let's say we have a learning algorithm that returns 
classiﬁer  after seeing  training pointshn n
• The algorithm is consistent iff  as R(hn) → R* n → ∞

## Page 29

Consistency
• Let's say we have a learning algorithm that returns 
classiﬁer  after seeing  training pointshn n
• The algorithm is consistent iff  as R(hn) → R* n → ∞
• Example: Nearest neighbor classiﬁcation

## Page 30

Consistency
• Let's say we have a learning algorithm that returns 
classiﬁer  after seeing  training pointshn n
• The algorithm is consistent iff  as R(hn) → R* n → ∞
• Example: Nearest neighbor classiﬁcation
• Pick  points at random from n P = (μ, η)

## Page 31

Consistency
• Let's say we have a learning algorithm that returns 
classiﬁer  after seeing  training pointshn n
• The algorithm is consistent iff  as R(hn) → R* n → ∞
• Example: Nearest neighbor classiﬁcation
• Pick  points at random from n P = (μ, η)
• Let  be the 1-NN classiﬁer trained on this datahn

## Page 32

Consistency
• Let's say we have a learning algorithm that returns 
classiﬁer  after seeing  training pointshn n
• The algorithm is consistent iff  as R(hn) → R* n → ∞
• Example: Nearest neighbor classiﬁcation
• Pick  points at random from n P = (μ, η)
• Let  be the 1-NN classiﬁer trained on this datahn
• Is  consistent?hn

## Page 33

Consistency
• Example: Nearest neighbor classiﬁcation

## Page 34

Consistency
• Example: Nearest neighbor classiﬁcation
• Is  consistent?hn

## Page 35

Consistency
• Example: Nearest neighbor classiﬁcation
• Is  consistent?hn
No! e.g. consider the follow distribution:

## Page 36

Consistency
• Example: Nearest neighbor classiﬁcation
• Is  consistent?hn
No! e.g. consider the follow distribution:
, ,  is uniform on ,  everywhere𝒳 = [0,1] 𝒴 = {0,1} μ 𝒳 η = 1
4

## Page 37

Consistency
• Example: Nearest neighbor classiﬁcation
• Is  consistent?hn
No! e.g. consider the follow distribution:
, ,  is uniform on ,  everywhere𝒳 = [0,1] 𝒴 = {0,1} μ 𝒳 η = 1
4
Bayes' optimal classiﬁer:     ,    Risk h* = 0 R* = 1
4

## Page 38

Consistency
• Example: Nearest neighbor classiﬁcation
• Is  consistent?hn
No! e.g. consider the follow distribution:
, ,  is uniform on ,  everywhere𝒳 = [0,1] 𝒴 = {0,1} μ 𝒳 η = 1
4
Bayes' optimal classiﬁer:     ,    Risk h* = 0 R* = 1
4
1-NN classiﬁer:  error two coins of bias 1/4 disagree  Pr( ) = Pr( )

## Page 39

Consistency
• Example: Nearest neighbor classiﬁcation
• Is  consistent?hn
No! e.g. consider the follow distribution:
, ,  is uniform on ,  everywhere𝒳 = [0,1] 𝒴 = {0,1} μ 𝒳 η = 1
4
Bayes' optimal classiﬁer:     ,    Risk h* = 0 R* = 1
4
1-NN classiﬁer:  error two coins of bias 1/4 disagree  Pr( ) = Pr( )
= 2 ⋅ 3
4 ⋅ 1
4 = 3
8 > R*

## Page 40

Consistency
• Example: Nearest neighbor classiﬁcation
• Is  consistent?hn
No! e.g. consider the follow distribution:
, ,  is uniform on ,  everywhere𝒳 = [0,1] 𝒴 = {0,1} μ 𝒳 η = 1
4
Bayes' optimal classiﬁer:     ,    Risk h* = 0 R* = 1
4
1-NN classiﬁer:  error two coins of bias 1/4 disagree  Pr( ) = Pr( )
= 2 ⋅ 3
4 ⋅ 1
4 = 3
8 > R*
In fact, can show , at most twice Bayes' 
risk.
R(hn) → 2R*(1 − R*)

## Page 41

Consistency of k-NN
• But k-NN is consistent if  grows with k n

## Page 42

Consistency of k-NN
• But k-NN is consistent if  grows with k n
• Theorem:

## Page 43

Consistency of k-NN
• But k-NN is consistent if  grows with k n
• Theorem:
• Let  be a metric space.𝒳

## Page 44

Consistency of k-NN
• But k-NN is consistent if  grows with k n
• Theorem:
• Let  be a metric space.𝒳
• Let  be the k-NN classiﬁer based on  training pointshn,k n ∼ P

## Page 45

Consistency of k-NN
• But k-NN is consistent if  grows with k n
• Theorem:
• Let  be a metric space.𝒳
• Let  be the k-NN classiﬁer based on  training pointshn,k n ∼ P
• Suppose:

## Page 46

Consistency of k-NN
• But k-NN is consistent if  grows with k n
• Theorem:
• Let  be a metric space.𝒳
• Let  be the k-NN classiﬁer based on  training pointshn,k n ∼ P
• Suppose:
•  is a growing function of  with k n k → ∞, k
n → 0

## Page 47

Consistency of k-NN
• But k-NN is consistent if  grows with k n
• Theorem:
• Let  be a metric space.𝒳
• Let  be the k-NN classiﬁer based on  training pointshn,k n ∼ P
• Suppose:
•  is a growing function of  with k n k → ∞, k
n → 0
•  is continuousη

## Page 48

Consistency of k-NN
• But k-NN is consistent if  grows with k n
• Theorem:
• Let  be a metric space.𝒳
• Let  be the k-NN classiﬁer based on  training pointshn,k n ∼ P
• Suppose:
•  is a growing function of  with k n k → ∞, k
n → 0
•  is continuousη
• Then: 

## Page 49

Consistency of k-NN
• But k-NN is consistent if  grows with k n
• Theorem:
• Let  be a metric space.𝒳
• Let  be the k-NN classiﬁer based on  training pointshn,k n ∼ P
• Suppose:
•  is a growing function of  with k n k → ∞, k
n → 0
•  is continuousη
• Then: 
• R(hn,k) → R*

## Page 50

Consistency of k-NN
• Proof sketch:  Pick any point .  We'll show that x ∈ 𝒳
hn,k(x) → h*(x)

## Page 51

Consistency of k-NN
• Proof sketch:  Pick any point .  We'll show that x ∈ 𝒳
hn,k(x) → h*(x)
(i) If , it doesn't matter what we predict. So, 
without loss of generality, let 
η(x) = 1
2
η(x) < 1
2

## Page 52

Consistency of k-NN
• Proof sketch:  Pick any point .  We'll show that x ∈ 𝒳
hn,k(x) → h*(x)
(i) If , it doesn't matter what we predict. So, 
without loss of generality, let 
η(x) = 1
2
η(x) < 1
2
(ii) By continuity,  in some ball  around . η < 1
2 B x
B
x

## Page 53

Consistency of k-NN
• Proof sketch:  Pick any point .  We'll show that x ∈ 𝒳
hn,k(x) → h*(x)
(i) If , it doesn't matter what we predict. So, 
without loss of generality, let 
η(x) = 1
2
η(x) < 1
2
(ii) By continuity,  in some ball  around . η < 1
2 B x
random point falls in BPr( ) = μ(B)
B
x

## Page 54

Consistency of k-NN
• Proof sketch:  Pick any point .  We'll show that x ∈ 𝒳
hn,k(x) → h*(x)
(i) If , it doesn't matter what we predict. So, 
without loss of generality, let 
η(x) = 1
2
η(x) < 1
2
(ii) By continuity,  in some ball  around . η < 1
2 B x
random point falls in BPr( ) = μ(B)
(iii) As :n → ∞
B
x

## Page 55

Consistency of k-NN
• Proof sketch:  Pick any point .  We'll show that x ∈ 𝒳
hn,k(x) → h*(x)
(i) If , it doesn't matter what we predict. So, 
without loss of generality, let 
η(x) = 1
2
η(x) < 1
2
(ii) By continuity,  in some ball  around . η < 1
2 B x
random point falls in BPr( ) = μ(B)
(iii) As :n → ∞
• k-NN of  fall in Pr( x B) → 1
B
x

## Page 56

Consistency of k-NN
• Proof sketch:  Pick any point .  We'll show that x ∈ 𝒳
hn,k(x) → h*(x)
(i) If , it doesn't matter what we predict. So, 
without loss of generality, let 
η(x) = 1
2
η(x) < 1
2
(ii) By continuity,  in some ball  around . η < 1
2 B x
random point falls in BPr( ) = μ(B)
(iii) As :n → ∞
• k-NN of  fall in Pr( x B) → 1
• majority vote of their labels is 0Pr( ) → 1
B
x

## Page 57

Consistency of k-NN 
• Interesting question:
• How does k-NN behave on a non-metric space? 

## Page 58

Limitations of the Framework
• Central assumption:  All data is i.i.d. from a ﬁxed, 
unknown, distribution over .𝒳 × 𝒴
• When might this not hold?

## Page 59

Limitations of the Framework
• Central assumption:  All data is i.i.d. from a ﬁxed, 
unknown, distribution over .𝒳 × 𝒴
• When might this not hold?
• Shifting distribution

## Page 60

Limitations of the Framework
• Central assumption:  All data is i.i.d. from a ﬁxed, 
unknown, distribution over .𝒳 × 𝒴
• When might this not hold?
• Shifting distribution
(i)  changing,  ﬁxed:  e.g. different handwriting / speech 
distributions
μ η

## Page 61

Limitations of the Framework
• Central assumption:  All data is i.i.d. from a ﬁxed, 
unknown, distribution over .𝒳 × 𝒴
• When might this not hold?
• Shifting distribution
(i)  changing,  ﬁxed:  e.g. different handwriting / speech 
distributions
μ η
(ii)  both change:    e.g. document categorization 
(politics, sports, etc.)
μ, η