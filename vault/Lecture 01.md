---
title: "Lecture 01"
date: "2025-04-13"
source: "inbox/Lecture 01.pdf"
format: "PDF Document"
pages: "35"
converted: "2025-10-31 10:24:36"
---

# Lecture 01

**Pages:** 35


## Page 1

CSE 150A 250A
AI: Probabilistic Methods
Spring 2025
Instructor: Trevor Bonjour
Slides adapted from previous versions of the course (Prof. Lawrence, Prof. Alvarado, Prof Berg-Kirkpatrick) 

## Page 2

Agenda
• Course Logistics
• Syllabus Review
• Course Overview
• Probability Review

## Page 3

Course Websites
•Canvas 
• Syllabus, slides/notes, office hours, assignments, grades and 
podcasts are posted here. 
•Piazza
• Announcements, course related questions/discussions happen 
here. (Emails may be missed!)
•Gradescope 
• Submit your homework here.

## Page 4

Instructional Staff - TAs
Danlu
 Eric
 Mithil
 Ruolan
Sharanya
 Sohyun
 Tianyi

## Page 5

It’s a BIG class! We need to 
work together!
We are here to help!

## Page 6

Course enrollments are controlled by the 
department. 
• They don’t let me as an instructor directly approve EASY requests. 
• Please submit one – department will try to approve as many as they can. 
• The course is limited by TA capacity and room size. Can’t add more seats.

## Page 7

Prerequisites
• Programming
• Most HW assignments will involve coding.
• Also, basic data analysis and visualization
• Solutions accepted in any language!
• Most common languages are Python and MATLAB.
• We can help with algorithmic and conceptual issues. 
• We cannot help with installing, compiling, plotting, etc. 
Non-CS backgrounds are welcome. 

## Page 8

Prerequisites
• Elementary probability: 
• Random variables — discrete and continuous 
• Expected values (via sums and integrals) 
• Multivariable calculus: 
• Chain rule
• Gradients and partial derivatives
• Computing maxima and minima
• Constrained optimization with Lagrange multipliers 

## Page 9

Prerequisites
• Linear algebra
• Vectors and matrices
• Matrix multiplication, inverses, determinants 
• Systems of linear equations 
• Mathematical maturity
• Patience and persistence go a long way
• Willingness to fill in gaps

## Page 10

Readings and Lectures
• Readings
• No required texts.
• Some handouts (on Canvas). 
• Lectures
• Designed to be self-contained.
• Crucial for homework assignments. 
• Emphasis on mathematical development. 
• Slides will be posted. 
• Homework Discussions
• Announced on Piazza when HW is released.

## Page 11

Grading
• Homework: 50%
• Participation*: 10%
• Midterm: 20%
• Final: 20% (*could go up to 30% based on your participation)
• Academic dishonesty
• Neither ethical nor in your self-interest.
• Always credit your sources.
• Suspected plagiarism will be reported to campus. 

## Page 12

Homework: 50%
• Released on Tuesdays, due on Monday 11:59 PM the following week.
• No penalty for submissions that are up to 24hrs late. Beyond the 24hr 
grace period, we will not accept late homework.
• Submit on Gradescope.
• Typesetting (LaT eX) preferred, but we will accept neatly handwritten 
solutions. Be kind to the graders!
• TOP TIP: Start early, collaborate, reach out to the TAs for help.

## Page 13

Collaboration Encouraged!
• What is allowed?
• You may work in groups on problems.
• Write up all your own work.
• You may consult published texts (include citations as necessary).
• What is not allowed?
• Using old course materials.
• Copying from current or former students.
• Uploading current materials to archives.

## Page 14

Participation*: 10%
• In-class webclicker questions and online surveys (First survey is out!).
• Graded for completion, not correctness.
• Chance to engage in class and review your learning.
*Points lost on participation --> Final exam
• Scenario 1: You answer 100% of participation questions.
• You get the 10% for participation, and your final is worth 20% of your grade.
• Scenario 2: You do not answer any participation questions.
• Your final exam will be worth 30% of your final grade.

## Page 15

Exams
• Midterm (20%)
• Date: Week 6 (Mon – Sat)
• Time: Self-schedule slot with Triton T esting Center (TTC) – Schedule ASAP
• Where: - TTC - AP&M or TTC - Pepper Canyon Hall (OSD-approved accommodations)
• Computer based, closed book, no notes. TTCs policies are the policy for this course. Take a photo ID!
• Final (20% - 30%)
• Date: Week 10 - Thursday, Jun 5 (Please IGNORE date on Webreg)
• Time: 3:30 PM – 4:50 PM (Usual class time)
• Where: WLH 2001 (Usual classroom)
• Paper based, closed book, but you can bring one sheet of handwritten notes (8.5" x 11" standard paper, 
front and back).

## Page 16

Course Overview
• What we do cover: 
• Inference and learning in Bayesian networks
• Markov decision processes for reinforcement learning (RL) 
• What we don’t cover (not exhaustive): 
• Neural architectures (though we will talk about deep learning) 
• Purely logical reasoning
• Heuristic search (A*)
• Theorem proving 
• Genetic algorithms Philosophy of AI 

## Page 17

Course Overview
• What we do cover: 
• Inference and learning in Bayesian networks
• Markov decision processes for reinforcement learning (RL) 
      Why these topics? 

## Page 18

Modern AI
(ChatGPT, LLMs)
Neural Networks 
(Deep Learning)
Probabilistic Methods
(Bayesian Networks)
Skyscraper
Beams/Columns
Foundation
(THIS COURSE)

## Page 19

“Judea Pearl is credited 
with the invention of Bayesian 
networks, a mathematical 
formalism for defining complex 
probability models, as well as the 
principal algorithms used for 
inference in these models. This 
work not only revolutionized the 
field of AI but also became an 
important tool for many other 
branches of engineering and the 
natural sciences.”
Turing Award 2011
Turing Award Citation:
Image Source: Lex Freidman Podcast

## Page 20

Probability and Neural Nets
Image Source: Prof Berg-Kirkpatrick
“a classy synthwave apartment on mars, digital art”
“an intricate line drawing of new your subway station full of 
trumpet players”

## Page 21

Probability and Neural Nets


## Page 22

Breakthrough in RL

## Page 23

Probability Review

## Page 24

Probability in AI
Probability Theory == "How knowledge affects belief" (Poole and 
Mackworth)
What is the 
probability that it is 
raining out? 
How much do I 
believe that it is 
raining out? 
Viewing probability as measuring belief (rather than frequency of events) is known as the 
Bayesian view of probability (as opposed to the frequentist view).
24

## Page 25

Discrete Random Variables
Discrete random variables, denoted with capital letters: e.g., 𝑋
Domain of possible values for a variable, denoted with lowercase 
letters: e.g., 𝑥1, 𝑥2, 𝑥3, … , 𝑥𝑛
Example: Weather 𝑊 ; 𝑤1 = 𝑠𝑢𝑛𝑛𝑦, 𝑤2 = 𝑐𝑙𝑜𝑢𝑑𝑦
25

## Page 26

Unconditional (prior) Probability
𝑃 𝑋 = 𝑥
e.g., What is the probability that the weather is sunny?
𝑃 𝑊 = 𝑤1
26

## Page 27

Axioms of Probability
𝑃 𝑋 = 𝑥  ≥ 0
෍
𝑖=1
𝑛
𝑃 𝑋 = 𝑥𝑖 = 1
𝑃 𝑋 = 𝑥𝑖 𝑜𝑟 𝑋 = 𝑥𝑗 = 𝑃 𝑋 = 𝑥𝑖 + 𝑃 𝑋 = 𝑥𝑗  𝑖𝑓 𝑥𝑖 ≠ 𝑥𝑗
Mutually Exclusive!
27

## Page 28

Conditional Probability
𝑃 𝑋 = 𝑥𝑖|𝑌 = 𝑦𝑗
"What is my belief that 𝑋 = 𝑥𝑖 if I already know 𝑌 = 𝑦𝑗"
Sometimes, knowing Y gives you information about X, i.e., changes 
your belief in X.  In this case X and Y are said to be dependent.
𝑃 𝑋 = 𝑥𝑖|𝑌 = 𝑦𝑗 ≠ 𝑃 𝑋 = 𝑥𝑖
28

## Page 29

Webclicker 
Course code: GJLOWD
Link: https://webclicker.web.app/ 
Login using UCSD 
Google account
If NO UCSD account – 
Use a personal Google 
account
Carefully enter PID
Used to give you credit for 
participation.

## Page 30

Marginal Independence
𝑃 𝑋 = 𝑥𝑖|𝑌 = 𝑦𝑗 = 𝑃 𝑋 = 𝑥𝑖
Sometimes knowing Y does not change your belief in X.  In this 
case, X and Y are said to be independent.
𝑃 𝑊 = 𝑤𝑖|𝑌 = 𝑦𝑗 = 𝑃 𝑊 = 𝑤𝑖
For which variable Y is the above statement most likely true?
A.  Y = The weather yesterday
B.  Y = The day of the week
C.  Y = The temperature
30
Course code: GJLOWD

## Page 31

More independence
What is the most logical relationship between 𝑃 𝑅 = 1  and 𝑃 𝑅 = 1 𝑆 = 1 ?
A. 𝑃 𝑅 = 1 = 𝑃 𝑅 = 1|𝑆 = 1
B. 𝑃 𝑅 = 1 > 𝑃 𝑅 = 1|𝑆 = 1
C. 𝑃 𝑅 = 1 < 𝑃 𝑅 = 1|𝑆 = 1
Consider two similar students Roberto and Sabrina, who both took the 
same test.  Define the following random variables:
R = Roberto aced the test
S = Sabrina aced the test
31
Course code: GJLOWD

## Page 32

Conditional Independence
R and S are conditionally independent given T.  I.e., if you already 
know T, knowing S does not give you additional information about R.
What if you also know the test was easy (variable T)?
A. 𝑃 𝑅 = 1|𝑇 = 1 = 𝑃 𝑅 = 1|𝑇 = 1, 𝑆 = 1
B. 𝑃 𝑅 = 1|𝑇 = 1 > 𝑃 𝑅 = 1|𝑇 = 1, 𝑆 = 1
C. 𝑃 𝑅 = 1|𝑇 = 1 < 𝑃 𝑅 = 1|𝑇 = 1, 𝑆 = 1
32
Course code: GJLOWD

## Page 33

More independence
Consider two events: 
B = A burglar breaks into your apartment 
E = An earthquake occurs
Are these events independent or dependent?  (i.e., does knowing that one 
happened change your belief in the other?)
A. They are independent because knowing that one happened does not 
change your belief that the other happened.
B. They are dependent, because knowing that one happened changes your 
belief that the other happened.
33
Course code: GJLOWD

## Page 34

Conditional dependence
Now consider a third event: 
A = Your alarm goes off
Which of the following relationships best models beliefs about the world?
A. 𝑃 𝐵 = 1|𝐴 = 1 = 𝑃 𝐵 = 1|𝐴 = 1, 𝐸 = 1
B. 𝑃 𝐵 = 1|𝐴 = 1 > 𝑃 𝐵 = 1|𝐴 = 1, 𝐸 = 1
C. 𝑃 𝐵 = 1|𝐴 = 1 < 𝑃 𝐵 = 1|𝐴 = 1, 𝐸 = 1
𝑃 𝐵 = 1 = 𝑃 𝐵 = 1|𝐸 = 1 = 𝑃 𝐵 = 1|𝐸 = 0
34
Course code: GJLOWD

## Page 35

That’s all folks!