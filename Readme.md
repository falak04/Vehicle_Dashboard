# Vehicle Registration Analysis Dashboard 🇮🇳

An interactive dashboard built with Python and Streamlit to analyze vehicle registration data in India from an investor's perspective. This project fulfills all technical requirements of the backend developer internship assignment, including modular code structure, use of SQL for data manipulation, and clear documentation.

## ✨ Key Features

* **SQL-Powered Backend**: All data filtering is performed using an in-memory SQLite database, demonstrating SQL proficiency.
* **Dynamic Filtering**: Users can filter data by date range, vehicle category (2W/3W/4W), and manufacturer.
* **Growth Analysis**: Automatically calculates and displays Year-over-Year (YoY) and Quarter-over-Quarter (QoQ) growth metrics.
* **Rich Visualizations**: Includes multiple charts for analyzing registration trends, market share evolution, and growth percentages to provide quick, actionable insights.
* **Modular Codebase**: The code is separated into a data processing module (`data_processor.py`) and a UI module (`app.py`) for readability and maintenance.

## 🚀 Live Demo

*[A live version of this dashboard can be accessed here: (Link to your deployed Streamlit app)]*

## 📊 Dashboard Preview

**

## 🛠️ Technical Stack

* **Language**: Python
* **Dashboarding**: Streamlit
* **Data Manipulation**: Pandas
* **Database**: SQLite (via Python's `sqlite3` module)
* **Plotting**: Plotly Express

## ⚙️ Setup and Installation

Follow these steps to set up and run the project on your local machine.

1.  **Clone the Repository**
    ```bash
    git clone <your-github-repo-url>
    cd Vehicle-Dashboard
    ```

2.  **Create and Activate a Virtual Environment** (Recommended)
    ```bash
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install Required Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Streamlit Application**
    ```bash
    streamlit run app.py
    ```
    The application should now be open and running in your web browser.

## 📁 Code Structure

The project is structured to be modular and readable:

* `app.py`: The **frontend** of the application. It handles the user interface (UI) components and makes calls to the data processor.
* `data_processor.py`: The **backend** logic module. It manages the SQLite database, executes all SQL queries, and contains the functions for calculating growth metrics.
* `sample_vehicle_data.csv`: The **data layer**, containing manually extracted data from the Vahan dashboard.
* `DATA_COLLECTION.md`: A detailed document explaining the manual data collection process.
* `requirements.txt`: Lists all necessary Python packages for the project.

## 📈 Data Source and Collection

A detailed document outlining the manual data collection process from the Vahan Dashboard is provided in **`DATA_COLLECTION.md`**. This approach was chosen due to the technical challenges and restrictions associated with automated scraping of the official dashboard.

## 💡 Key Investor Insights

* **The Growth vs. Stability Dilemma**: The dashboard clearly visualizes the core conflict in the current auto market. Newer EV players like "Ather" and "EV Innovate" show explosive YoY growth, representing a high-risk, high-reward investment. In contrast, legacy players like "Maruti Suzuki" offer stability and dominant market share but have much slower growth.
* **Market Share Erosion**: The "Market Share Evolution" chart shows the slow but steady encroachment of new players on the territory of established leaders, providing a real-time view of market disruption.

## 🛣️ Future Roadmap

* **Automated Data Pipeline**: Develop a robust web scraper using Selenium or Playwright to automate the data ingestion process.
* **State-wise Analysis**: Add filters and charts to compare registration trends across different states in India.
* **Predictive Forecasting**: Integrate time-series forecasting models (like ARIMA or Prophet) to predict future registration volumes.

## 📹 Video Walkthrough

*[Link to your 5-minute video walkthrough on YouTube or Google Drive]*
