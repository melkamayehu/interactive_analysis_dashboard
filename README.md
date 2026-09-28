# Interactive Analytics Dashboard

A simple interactive dashboard for exploring sales and profit data using the Superstore dataset.

I built this project to practice working with **Pandas, Plotly, and Streamlit** and to turn a dataset into something that can be explored through an interactive dashboard.

## What the dashboard shows

The dashboard helps explore:

* Total sales
* Total profit
* Total orders
* Average order value
* Profit margin
* Sales over time
* Sales by category
* Profit by category
* Sales by region
* Sales by customer segment
* Top 10 products by sales
* Monthly sales and profit trends
* Sales vs. profit by category

## Interactive Filters

The sidebar allows the data to be filtered by:

* Region
* Category
* Customer Segment
* Sub-Category
* Date range

There is also a **Reset Filters** button to return to the full dataset.

## Tools Used

* **Python** – main programming language
* **Pandas** – loading, filtering, grouping, and analyzing the data
* **Plotly** – creating interactive charts
* **Streamlit** – building the dashboard interface
* **Excel / xlrd** – reading the `.xls` dataset

## Project Structure

```text
interactive-analytics-dashboard/
│
├── data/
│   └── sample_-_superstore.xls
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## How to Run

Clone the repository and move into the project folder:

```bash
cd interactive-analytics-dashboard
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Start the Streamlit dashboard:

```bash
python -m streamlit run app.py
```

The dashboard will then open in your browser.

## What I Learned

This project helped me understand how different Python tools work together in a data application.

I used **Pandas** to work with the data, **Plotly** to create interactive visualizations, and **Streamlit** to turn the analysis into a dashboard that users can interact with.

I also practiced filtering data, creating KPIs, grouping data for analysis, and presenting results in a more useful way than a notebook alone.

## Future Improvements

Some things I would like to add in the future include:

* More advanced business metrics
* Additional filters
* Better dashboard styling
* Deployment so the dashboard can be accessed online
* More detailed product and customer analysis
