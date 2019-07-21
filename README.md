# personER
PoC code of Entity Resolution solutions.

##  How to install
Install packages in the `requirements.txt`

You may also need to install `NLTK` if you want to run DeepChecker.

##  Usage
To run from code, look at the tests to get started.

###  To run LexicalChecker from commandline:
```
python personER.py -na 'Mr. Wade JR Smith' -nb 'Mr. Smith JR Wade' -ua 'http://wade-smith.com' -ub 'http://www.wade-smith0.com/index.html'
```


###  To run LexicalChecker from commandline:
Just add a `-deep` flag to switch to the DeepChecker.
```
python personER.py -deep -na 'Tang Nan' -nb 'Dr. Nan Tang' -ua 'https://www.hbku.edu.qa/en/staff/dr-nan-tang' -ub 'http://da.qcri.org/ntang/index.html'
```