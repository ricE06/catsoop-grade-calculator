# catsoop-grade-calculator
Scrapes CAT-SOOP to calculate predicted grades for students in some MIT course 6 classes.

## Table of Contents

- [Preface](#preface)
- [Installation and Setup Instructions](#installation-and-setup)
  - [Package Installation](#installing-the-package)
  - [API Tokens](#setting-up-api-tokens)
- [Want to Contribute?](#contributing)
  - [Adding Courses](#adding-courses)
  - [Adding Features](#adding-features)
  - [Maintainence](#breaking-news)

## Preface
> "...\[6.101\] used to have a cumulative scoring system, but this meant
> that no one ever did the last few labs."
> 
> \- Adam Hartz, circa 2024

CAT-SOOP is a web-based LMS that hosts a variety of course 6 (EECS) classes
at MIT. For most classes, cumulative grades are unfortunately not displayed the student.
This could be because the grading system involves a series of complex
modifications applied at the end of the semester (I'm looking at you 6.390). Another good
reason is to dissuade students from doing tasks purely for the sake of maintaining
a grade. I am not here to argue against valid justifications for this choice, *however*:

All of the information needed to calculate a grade is *technically* there.

Enter **CATSOOPER**, the *CATSOOP gradE calculatoR*, which will scrape CAT-SOOP for your classes
and calculate your current grades. So whether you're concerned about passing, hoping to 
stay on a certain letter grade, or you're one of those freshmen on P/NR aspiring to become the next
Bare Minimum King, feel free to [install this package](#installation-and-setup) and enjoy.

A word of warning. Or rather, a series of warnings:

- This is NOT a real grade, nor is it indicative in any way of the grade you will
receive at the end of the class. Treat it like an estimate. However the course decides to
calculate your grade will always be final.
- This is a third party tool, and not developed by MIT or any of the courses within. While I 
tried to be as accurate as possible with aligning to grading policy, some parts are too
difficult or ambiguous to implement perfectly. For instance, the 6.101 calculator does not
take into account late extensions, and the 6.200 calculator uses rounded values (while the
course page keeps exact values internally). Whenever situations like these occur, I try to
estimate the grade on the *low* side, but don't count on it every time.
- This package makes a very, *very* volatile set of assumptions. While I tried the scraper
as robust as I can, it is possible that a formatting change in the "Progress" page may break
the scraper. It [shouldn't reasonably happen](#breaking-news)
(why someone would rename the term "PSet" is beyond me), 
but it is a possibility.
- This is a bodge thrown together in the span of a few hours. It is pre-alpha and may contain
bugs. Use common sense: if the output seems wrong, it probably is wrong. Please [let me know](#contributing)
of any issues you find.

As of version 0.1.0, CATSOOPER supports scraping for 6.101 and 6.200. If you're in another
class and would like to see support added for that, please consider [contributing](#adding-classes).
You don't need to know how to code, but I do need to see the format of the webpage and
the grading rules.

## Installation and Setup

### Installing the Package

Hopefully this section is accessible to beginners; please let me know and/or offer
improvements if it isn't.

First, you will need to install [Python](https://www.python.org/downloads/) version 3.10
or above. If you are on Windows or Mac, the easiest way is to go to the website, 
download the source, and follow their instructions. If you're on Linux, I'm going to
assume you know what you are doing.

Navigate to your command line:
- For Windows users, type `cmd` into the start menu. Alternatively, navigate to
a directory in File Explorer and type `cmd` into the path bar; this will take you
to that directory in your command line automatically as well.
- For MacOS users, open your Terminal app.

Check that Python is properly installed by typing `python` or `python3` into your
terminal. If it's installed properly, you should be taken to a python interactive
environment. Use `exit()` to get out of that.

Next, install the package. In your command line, enter the command:

```
pip install catsoop_grade_calculator
```

Open your interactive environment again with `python`/`python3`. If you've done
everything correctly, you should be able to type

```python
import catsoop_grade_calculator
```

and Python won't throw an error. If it goes through, hooray! The package is now
on your computer, ready to go.

### Setting up API Tokens

To actually access your grades, CATSOOPER will need an API token. For *each* of your
classes, perform the following steps:

- Navigate to the course homepage and log in with your MIT credentials.
- On the top right, click on your username and then click **Settings.**
- Go to **Manage API Tokens**.
- Generate a token and follow the instructions on the website. It should be a long
string containing only numbers and lowercase letters `a-f` (i.e. a hexadecimal number).

**DO NOT SHARE YOUR TOKEN WITH ANYONE!!!** CATSOOPER runs entirely on your local machine,
and I will not see your token if you use this package.

I recommend storing these tokens in one text file for convenience. For the purposes of this tutorial, 
we will assume that you have your tokens stored in a file `token.txt` with the following format:
```
6.101 --your-token-here--
6.200 --another-token-here--
x.xxx --yet-another-token-here--
etc.
```
where there is a space separating the class number and your token. 

Awesome! What next?

## Basic Usage and Examples

We're going to create a very simple Python file to get your grades and print out
a grade report for each of your classes. Create it in the same directory
that you stored your tokens. At the top, first import the package:

```python
from catsoop_grade_calculator import ScoreCalculator
```

Then, we need to give it your tokens. You could store these as variables 
directly, but I strongly recommend against it. Rather, use open and read your `token.txt`:

```python
tokens = {}
with open('token.txt', 'r') as file:
    for line in file:
        class_num, token = line.strip().split(' ')
        tokens[class_num] = token
```

However you decide to do it, you will need to initialize a dictionary, where each key
is a class number (`6.101`, `6.200`, etc.) and each value is a token string. 

Next, we will create an instance of the grade calculator, tell it to generate
a report for us, and print it into the terminal:

```python
sooper = ScoreCalculator(tokens)
report = sooper.report_all()
print(report)
```

Lastly, navigate to this directory in your command line and run the program:

```
python name-of-file.py
```

You should see your grade reports print to your terminal! They will look something
like this:

```
==================================
GRADE REPORT FOR 6.200:
==================================
OVERALL GRADE: ..........xx.xx%
....Points collected: ...xx.xx
....Points possible: ....xx.xx
ALTERNATIVE SCORE(S):
....xx.xx%
CATEGORY BREAKDOWN:
....lab............xx.xx%
....midterm........xx.xx%
....nanoquiz.......xx.xx%
....participation..xx.xx%
....pset...........xx.xx%
https://circuits.mit.edu/F24/progress
```

Note: some classes may not have alternative scores. This exists because some classes
have more than one grading scheme and take your best. This serves to see your theoretical
score under each possible scheme.

If instead of printing, you wanted to save the result into a text file, 
do the following:
```python
with open("output.txt", "w") as file:
    file.write(report)
```

All of the starter code described here is provided under `/examples/` in the 
[Github repo](https://github.com/ricE06/catsoop-grade-calculator),
so you can also download and use that if you wish.

## Contributing

If you enjoy this package and find it useful, **please consider contributing**!
It doesn't have to be through writing source code (although I would happily accept
pull requests if you do). As CAT-SOOPER only supports two classes right now, 
it would be wonderful if you could help by [providing relevant information](#adding-courses) about
different CAT-SOOP classes that could use a calculator as well.

You can open an issue on the [Github](https://github.com/ricE06/catsoop-grade-calculator),
email me at `ezzhaneri06@gmail.com`, or
contact me through Discord: my handle is `ricezcakes`.

### Adding Courses

If you are currently enrolled in an MIT class, and it satisfies the following criteria:

- It is hosted on CAT-SOOP.
- There is a single "Progress" page that tracks individual grades.
- A cumulative grade is not given to you.
- It is not already supported by CAT-SOOPER.

Then, we can work together to add it to CAT-SOOPER! The main thing is that I need 
to know what the format of the Progress page is like (so I can parse it properly),
and also the grading policies for your class. If you are willing, please reach out and share the relevant
information.

It may take some time, and unfortunately there is no way to really automate or generalize this
process, as each class and page format is so different. 
Feel free to contribute to the code yourself if you want as well; I apologize as
the documentation is a bit sparse as of now.

### Adding Features

There are a few important features that are planned (if there is sufficient
demand for them). They are, in no particular order:

- A GUI or web interface
- A shell script and command, rather than calling a Python file
- The ability to "test" current and future grades (technically possible,
but extremely cumbersome right now)
  - Storing *all* of the potential assignments and exams in a class to facilitate this
- URL "guessing", so we don't have to update new URLs every semester

 If you are interested in helping implement any of these, or have suggestions for
 new features, please [contact me](#contributing) or open a pull request! :)

 ### Breaking News

 There is always a possibility that an update to a course page will be *breaking*; that is,
 dramatic enough to throw off the parser. Please let me know if that happens, and I will
 roll out a change (or you can fix the code yourself if you wish). Sometimes, the issue
 may already be fixed, and you just need to upgrade the package to keep up:

```
pip install --upgrade catsoop_grade_calculator
```

A word on how the Progress page is actually parsed. The code goes line by line in the html,
removing any style or script elements (that is, extracting just the text). It also throws out
any line that doesn't contain a fixed set of substrings, so this reduces just to things
in headers, bullet points, tables, etc. This lowers the risk of extraneous text making it into
the parser. For each course, a set of keywords are given: it will look for these keywords 
in the line and for any numbers. If the keywords match, the program keeps track of the score
and which type of assignment (pset, lab, test, etc.) it belongs in.

Hence, small changes to the formatting (adding text, adding assignments, moving around the order)
won't break the parser. Even changing the names of assignments should be fine, within reason
(a pset should be identified by "pset", and it wouldn't make sense for them to call it "chicken
nuggets" anyways). It's always a possiblity, though, and thankfully the code structure allows
quick adaptation to any breaking changes.
