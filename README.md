# 🏏 IPL Win Probability Predictor

An AI-powered web application that predicts the win probability of IPL teams during a live match situation using Machine Learning.

## Project Overview

This project uses historical IPL match data to train a Machine Learning model that predicts the probability of the batting team winning based on live match conditions.

The model considers:
- Runs left
- Balls left
- Wickets remaining
- Current Run Rate (CRR)
- Required Run Rate (RRR)
- Target
- Venue
- Teams playing

## Tech Stack
- Python
- Pandas
- Scikit-learn
- Streamlit
- Joblib

## Features
- Real-time match input simulation
- Smart input validation
- Win probability prediction
- Clean and professional UI
- Match situation summary

## How It Works
1. User enters live match details
2. Features are engineered (CRR, RRR, balls_left, etc.)
3. Data is passed to trained ML pipeline
4. Model outputs win probability
5. UI displays insights visually
