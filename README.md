## Stock analysis software that analyzes historical stock data and recommends trading strategies using ChatGPT 3.5 Model Turbo 
Calculates the covariance, correlation, and cointegration between stock pairs using the Engle-Granger two step method using ADF-test to test if the pair is stationary and an OLS regression model to determine the linear relationship between the pairs.

## To avoid wanting to shoot your own foot off :)
After forking or pulling the project into your own repo, I highly recommend you use [miniconda](https://docs.conda.io/projects/miniconda/en/latest/index.html) or [conda](https://www.anaconda.com/download/) to set-up the development environment.

For windows users, please run this command top-to-bottom to get started with the development environment
```
scripts/ps1/venv.ps1
pip install .
```

For macOS users:
```
scripts/bash/venv.sh
pip3 install .
```

## Requirements:
Must have Docker software installed on your computer. If you are using macOS, then you must have the homebrew installed correctly and the brew docker casket installed on your computer in order for my script to work.

AS OF RIGHT NOW, if you pull the current codebase, you *MUST* provide your own OpenAI API key and save it as keys.env in the src directory. Please follow this [guide](https://platform.openai.com/docs/api-reference/authentication) to learn more about how to do this. 

<!-- View current progress on our [Jira.](https://jgrady15.atlassian.net/jira/core/projects/SP/board) -->

<!-- Use Python for:
Loading and preprocessing the stock price data (handling dates, null values, etc)
Calculating covariance, and correlation between the stock returns
Handling any API calls to obtain data
Plotting charts and visualizations

Use C++ for:
Analyzing the spread time series (volatility, mean reversion)
Performing the Engle-Granger two-step method for cointegration, which uses
OLS Regression and the ADF test for regression residuals
Efficiently calculating the ratio between stock prices
Computing the rolling means for the spread time series
Performing linear regression to quantify mean reversion speed
Any core math-heavy computations that require speed

Use ChatGPT for:
Evaluating criteria and determining if stocks qualify as a tradable pair -->
