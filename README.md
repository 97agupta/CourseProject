# CourseProject

Please fork this repository and paste the github link of your fork on Microsoft CMT. Detailed instructions are on Coursera under Week 1: Course Project Overview/Week 9 Activities.

# NYT Corpus folder structure

In order to run the PLSA algorithm, the NYT corpus structure has to be '../CourseProject/data/<month>/<day>'

# Stock data folder structure

We save the stock prices from May 2000 to Oct 2000 as htm files in the format of '<Month>_2000.htm' in a folder called 'stock_data'.
The htm files can be saved from https://iemweb.biz.uiowa.edu/pricehistory/pricehistory_SelectContract.cfm?market_ID=29

# Code content

- `plsa_without_prior.py`: initial run of PLSA without any priors
- `plsa_with_prior.py`: subsequent PLSA runs with priors determined from Granger and Pearson tests
- `word_retriever.py`: retrieves various info required such as word frequency per day
- `analysis.py`: contains code for running the Granger and Pearson coefficient tests

- `main.py`:
1. Retrieve and normalize stock data
2. Initially run PLSA without prior, and run the analysis (Granger and Pearson coefficient tests) to retrieve priors
3. Using the priors retrieved above, iterate with the PLSA with prior until the desired convergence is achieved.

# How to run code

Once the data files are saved in the structure defined above, you should be able to run `python3 main.py` which will converge
after a desired convergence has been retrieved.