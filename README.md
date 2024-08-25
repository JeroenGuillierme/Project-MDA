# Project-MDA
## Goal
The primary goal of this project is to enhance survival rates in cases of sudden heart attacks by optimizing the placement of Automatic External Defibrillators (AEDs). While cardiopulmonary resuscitation (CPR) is often the most critical intervention, the availability and accessibility of AEDs can significantly impact survival outcomes.

## Geocoding & Preprocessing
The project begins with geocoding the addresses of AED and Mobile Urgent Care (MUG) locations into latitude and longitude coordinates. Next, one large dataset is created with all the variables needed (inclusive new ones) and saved for further analysis.

## Response Time Analysis
The first analysis conducted is a Response Time Analysis (RTA). In this step, outliers are removed, and missing values are imputed. Subsequently, average response times are compared across different variables, including vector type, province, and event severity level.

## AED Optimization
The second analysis involves spatial clustering to identify high-risk areas for cardiac events. These areas are defined based on several thresholds and are then clustered using the DBSCAN algorithm. New AED locations are proposed at the centers of the identified clusters.

## Papermill
To automate the execution of the notebooks, Papermill is utilized. Copies of the original notebooks were made and parameterized within the Papermill folder, allowing the Python script to run the notebooks sequentially. The outputs and results generated are consistent with those from the original notebooks and are saved seperately in the Papermill folder.

## Web Application
A web application was developed to visualize the results and dynamically adjust clustering thresholds and parameters. The code and resources for the app are located in a separate GitHub repository, which includes its own requirements.txt file.


