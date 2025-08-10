# Vehicle Registration Analysis Dashboard

An interactive dashboard built with Streamlit and Python to analyze vehicle registration data in India from an investor's perspective, as per the backend developer internship assignment.

## 🚀 Key Features

* [cite_start]**Interactive UI**: Clean, investor-friendly interface built with Streamlit. [cite: 18]
* [cite_start]**Growth Analysis**: Displays Year-over-Year (YoY) and Quarter-over-Quarter (QoQ) growth metrics. [cite: 15]
* [cite_start]**Dynamic Filtering**: Allows users to filter data by date range, vehicle category (2W/3W/4W), and manufacturer. [cite: 19, 20]
* [cite_start]**Rich Visualizations**: Includes charts for trends, market share, and percentage change to provide quick insights. [cite: 21]
* [cite_start]**Modular Codebase**: The code is separated into a data processing module and a UI module for readability and maintenance. [cite: 25]

## 💾 Data Assumptions

* **Data Source**: The Vahan Dashboard does not provide a public API or a direct data download feature. [cite_start]Therefore, this project uses a representative sample dataset named `sample_vehicle_data.csv`. [cite: 12]
* **Data Structure**: The data is assumed to have the following columns: `Date`, `State`, `Vehicle_Type`, `Manufacturer`, `Registrations`.
* **Data Granularity**: The sample data is aggregated on a monthly basis. The calculations for QoQ and YoY growth are based on resampling this monthly data into quarters.

## 🛠️ Setup and Installation

Follow these steps to set up and run the project on your local machine.

**1. Clone the repository:**
```bash
git clone <your-github-repo-url>
cd Vehicle-Dashboard