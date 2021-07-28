# Formula 1 Data Visualization
An interactive dashboard built to display and explore Formula 1 data.

Access the app [here](https://share.streamlit.io/adenhaus/f1-data-viz/main/main.py).

This web app is built in the [Streamlit](https://streamlit.io) framework and accesses the [Ergast](http://ergast.com/mrd/) Formula 1 API. Some of the API calls are handled by weiranyu's pyErgast module, others are done in async via aiohttp.

### Run the App Yourself
After installing all dependencies run the app in a browser by typing `streamlit run main.py` in your terminal.

## Features
- Interactive line charts that show how driver and constructor points progressed over any given season.
- Interactive pie charts showing drivers' and constructors' share of points at the end of a season.
- Interactive drivers and constructors championship standings tables for each race in a season.

### Coming soon
- Historical stats snapshots for drivers and constructors.
  - Total races, wins, poles, points, podiums, championships won etc.
- All-time rankings of top 50 drivers and constructors.
  - Most wins, points, races, championships won etc.
- A world map of popular F1 tracks showing how many races have taken place at each.
- And anything else I can think of!

### pyErgast Issues
I created a file for the pyErgast code (ergastpy.py) and included it in my source because there are issues in the module that the developer, weiranyu, has not fixed (which are fixed in my version). I cannot import the module until said bugs are fixed. I might write my own API connectors and stop using pyErgast altogether.
