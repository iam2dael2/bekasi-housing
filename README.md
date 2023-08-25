# Bekasi Property Trends: Predicting House Prices with Data Technology
Data science project using web scraping, machine learning, and web application

## Overview
For this project, I want to build web app that will predict house price in Bekasi by using specified features. This project was made to help any house owner and/or buyer. This can help house owner to set right house price in Bekasi, and beneficial. Also, this can help house buyer to support his/her decision to save money for buy any house in Bekasi. This is the underlying model for building something with those capabilities.

I was able to get the model to predict the Bekasi Houses' Price with a R Squared score of 77% after model selection and cross validation. For most of the cases this would meet the need of an end user of the app. To get these results I used hyperparameter tuning of GridSearchCV on Random Forest Classifier. This created time efficiencies and solid results.
<br><br>
<img width="581" alt="Screenshot 2023-08-25 142845" src="https://github.com/iam2dael2/bekasi-housing/assets/99378048/2a4abd47-a767-4e60-a855-cc7ff1540b28">

## Notes
This notebook takes you through the process of creating an image classifer for various types of sports balls. To make this project run on your computer, follow all steps in next chapter.

## Steps
1. Run <a href="https://github.com/iam2dael2/bekasi-housing/blob/main/web-scraping.py">web-scraping.py</a>
2. Run <a href="https://github.com/iam2dael2/bekasi-housing/blob/main/data-preprocessing.ipynb">data-preprocessing.py</a>
3. Run <a href="https://github.com/iam2dael2/bekasi-housing/blob/main/data-analysis.ipynb">data-analysis.py</a>
4. Run <a href="https://github.com/iam2dael2/bekasi-housing/blob/main/model-building.ipynb">model-building.py</a>
5. Run <a href="https://github.com/iam2dael2/bekasi-housing/blob/main/app/app.py">app/app.py</a>

## Data
I used web scraping to gather house prices and other variable from <a href="https://www.rumah123.com/">rumah123.com</a>
