import papermill as pm

# Paths to your notebooks
notebook_1 = "1_Data_preprocessing.ipynb"
notebook_2 = "2_Calculating_distances.ipynb"
notebook_3 = "3_Response_Time_Analysis.ipynb"
notebook_4 = "4_AED_Placement.ipynb"

url2 = "https://raw.githubusercontent.com/JeroenGuillierme/Project-MDA/main/Data/"

# Define the parameters for the first notebook
pm.execute_notebook(
    notebook_1,
    output_path="Outputs/1_output_data_preprocessing.ipynb",
    parameters=dict(url="s3://mdaprojectdata2/",
                    url2=url2,
                    output_data_path='Results/preprocessed_data.csv')
)

pm.execute_notebook(
    notebook_2,
    output_path="Outputs/2_output_calculating_distances.ipynb",
    parameters=dict(input_data_path="Results/preprocessed_data.csv",
                    url2=url2,
                    output_data_path="Results/preprocessed_data_with_distances.csv")
)

pm.execute_notebook(
    notebook_3,
    output_path="Outputs/3_output_RTA.ipynb",
    parameters=dict(input_data_path="Results/preprocessed_data_with_distances.csv",
                    url2=url2,
                    output_rta_path="Results/rta_data.csv")
)

pm.execute_notebook(
    notebook_4,
    output_path="Outputs/4_output_AED_Placement.ipynb",
    parameters=dict(input_data_path1='Results/preprocessed_data_with_distances.csv',
                    input_data_path2='Results/rta_data.csv',
                    url2=url2,
                    output_aed_path='Results/new_aed_locations.csv')
)
