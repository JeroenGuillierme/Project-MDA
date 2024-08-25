import papermill as pm

# Paths to your notebooks
notebook_1 = "1. Data Exploration and preprocessing.ipynb"
notebook_2 = "2. Calculating distances.ipynb"
notebook_3 = "3. Response Time Analysis.ipynb"
notebook_4 = "4. AED Placement.ipynb"

# Define the parameters for the first notebook
pm.execute_notebook(
    notebook_1,
    output_path="Outputs/output_notebook_1.ipynb",
    parameters=dict(url="s3://mdaprojectdata2/",
                    url2="https://raw.githubusercontent.com/JeroenGuillierme/Project-MDA/main/Data/")
)

pm.execute_notebook(
    notebook_2,
    output_path="output_notebook_2.ipynb",
    parameters=dict(input_data_path="preprocessed_data.csv", output_data_path="updated_data.csv")
)

pm.execute_notebook(
    notebook_3,
    output_path="output_notebook_3.ipynb",
    parameters=dict(input_data_path="updated_data.csv", output_analysis_path="response_time_analysis.csv")
)

pm.execute_notebook(
    notebook_4,
    output_path="output_notebook_4.ipynb",
    parameters=dict(input_data_path="response_time_analysis.csv", output_final_path="spatial_clustering_results.csv")
)