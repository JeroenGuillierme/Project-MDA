import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import re
from shapely.geometry import Point
import seaborn as sns
from math import radians, cos, sin, asin, sqrt

# -----------------------------------------------------------------------------------------------------------------------
# Functions Notebook 1: Data Exploration and preprocessing
# -----------------------------------------------------------------------------------------------------------------------

# Function to correct latitude values
def correct_latitude(lat):
    '''
    Corrects and standardizes latitude values by ensuring they are numeric and properly formatted.
    :param lat: str, float or int
    The latitude value to be corrected.
    :return: float
    The corrected latitude value, or NaN if the input is NaN.
    '''
    if pd.isna(lat):
        return lat  # Return NaN as it is
    if isinstance(lat, (str, float, int)):
        lat_str = str(lat)
        # Remove any existing non-numeric characters (except -)
        lat_str = re.sub(r'[^0-9-]', '', lat_str)
        # Move the decimal point to ensure two digits before the decimal point
        if len(lat_str) > 2:
            lat_str = lat_str[:2] + '.' + lat_str[2:]
        return float(lat_str)
    return lat


# Function to correct longitude values
def correct_longitude(lon):
    '''
    Corrects and standardizes longitude values by ensuring they are numeric and properly formatted.
    :param lon: str, float or int
    The longitude value to be corrected.
    :return:float
    The corrected longitude value, or NaN if the input is NaN.
    '''
    if pd.isna(lon):
        return lon  # Return NaN as it is
    if isinstance(lon, (str, float, int)):
        lon_str = str(lon)
        # Remove any existing non-numeric characters (except -)
        lon_str = re.sub(r'[^0-9-]', '', lon_str)
        # Move the decimal point to ensure one digit before the decimal point
        if len(lon_str) > 1:
            lon_str = lon_str[:1] + '.' + lon_str[1:]
        return float(lon_str)
    return lon


# Function to filter rows based on coordinates falling within Belgium
def is_within_belgium(lat, lon):
    '''
    Checks if given latitude and longitude coordinates fall within Belgium's geographical boundaries.
    :param lat: float
    The latitude value to be checked.
    :param lon: float
    The longitude value to be checked.
    :return: bool
    True if the coordinates are within Belgium's boundaries, False otherwise.
    '''
    # Define the geographical boundaries of Belgium
    belgium_boundaries = {
        'min_latitude': 49.50,
        'max_latitude': 51.50,
        'min_longitude': 2.5,
        'max_longitude': 6.5
    }

    return (belgium_boundaries['min_latitude'] <= lat <= belgium_boundaries['max_latitude']) and \
        (belgium_boundaries['min_longitude'] <= lon <= belgium_boundaries['max_longitude'])


def assign_province(df, boundaries):
    '''
    Assigns (correct) province name to certain set of coordinates, using a shapefile of Belgium with the province boundaries.
    :param df: pandas dataframe containing the columns 'Latitude' and 'Longitude'
    :return: pandas dataframe
    Extended dataframe with extra column containing the Province names.
    '''
    # Create a GeoDataFrame from the input DataFrame
    geometry = [Point(xy) for xy in zip(df['Longitude'], df['Latitude'])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

    # Perform spatial join to determine the province for each point
    joined_gdf = gpd.sjoin(gdf, boundaries, how="left", predicate="intersects")

    # Extract the province name and assign it to a new column 'Province'
    df['Province'] = joined_gdf['NAME_2']

    return df


def assign_nearest_province(df, belgium_with_provinces_boundary):
    '''
    Assigns the nearest province name to points that lie just outside of Belgium.
    :param df: pandas DataFrame containing the columns 'Latitude' and 'Longitude'
    :param belgium_with_provinces_boundary: GeoDataFrame containing Belgium's provinces boundaries
    :return: pandas DataFrame
    Extended DataFrame with an extra column containing the Province names.
    '''

    # Create a GeoDataFrame from the input DataFrame
    geometry = [Point(xy) for xy in zip(df['Longitude'], df['Latitude'])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

    # Perform the initial spatial join using 'intersects'
    joined_gdf = gpd.sjoin(gdf, belgium_with_provinces_boundary, how="left", predicate="intersects")

    # Extract the province name and assign it to a new column 'Province'
    df['Province'] = joined_gdf['NAME_2']

    # Identify points that were not assigned a province
    unassigned_gdf = gdf[df['Province'].isnull()].copy()

    if not unassigned_gdf.empty:
        # Reproject both unassigned points and provinces to a projected CRS (e.g., EPSG:31370)
        projected_gdf = unassigned_gdf.to_crs(epsg=31370)
        projected_provinces = belgium_with_provinces_boundary.to_crs(epsg=31370)

        # Calculate the nearest province for each unassigned point
        nearest_provinces = []

        for idx, point in projected_gdf.iterrows():
            # Calculate distance to each province
            distances = projected_provinces.geometry.distance(point.geometry)
            # Find the index of the nearest province
            nearest_idx = distances.idxmin()
            # Get the province name of the nearest province
            nearest_province = projected_provinces.loc[nearest_idx, 'NAME_2']
            nearest_provinces.append(nearest_province)

        # Assign the nearest province to the unassigned points
        unassigned_gdf['Province'] = nearest_provinces

        # Update the original dataframe with these values
        df.loc[unassigned_gdf.index, 'Province'] = unassigned_gdf['Province']

    return df


# Function to convert time formats like %d%b%y:%H:%M:%S to date time
def convert_format1(time1):
    return pd.to_datetime(time1, format='%d%b%y:%H:%M:%S')


# Function to convert time formats like %Y-%m-%d %H:%M:%S.%f to date time
def convert_format2(time2):
    return pd.to_datetime(time2, format='%Y-%m-%d %H:%M:%S.%f')


# Function to convert time formats like %Y-%m-%d %H:%M:%S.%f %z to date time
def convert_format3(time3):
    return pd.to_datetime(time3, format='%Y-%m-%d %H:%M:%S.%f %z', dayfirst=True)


# Define a function to extract the numeric part using regex
def extract_numeric(text):
    '''
    Extracts the first numeric part from a given text using regular expressions.
    :param text: str
    The text from which to extract the numeric part.
    :return: int or float
    The extracted numeric value, or NaN if no numeric part is found.
    '''
    match = re.search(r'\d+', text)
    return int(match.group()) if match else np.nan


# Function to convert Timedelta to minutes
def timedelta_to_minutes(td):
    '''
    Converts a pandas Timedelta object to minutes.
    :param td: pd.TimeDelta
    The Timedelta object to be converted.
    :return: float
    The total duration in minutes.
    '''
    return td.total_seconds() / 60


# Setting the style for the plots
sns.set(style="whitegrid")


# Function to draw histograms
def draw_histograms(df, variables, n_rows, n_cols):
    fig = plt.figure()
    for i, var_name in enumerate(variables):
        ax = fig.add_subplot(n_rows, n_cols, i + 1)
        sns.histplot(df[var_name], bins=100, ax=ax).set(title=var_name + " Distribution")
    fig.tight_layout()  # Improves appearance a bit.
    plt.show()


# -----------------------------------------------------------------------------------------------------------------------
# Functions Notebook 2: Calculating Distances
# -----------------------------------------------------------------------------------------------------------------------

# Haversine formula
def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in (kilo)meters
    return c * r


# -----------------------------------------------------------------------------------------------------------------------
# Functions Notebook 4: AED Placement Optimization
# -----------------------------------------------------------------------------------------------------------------------

# Function to calculate cell size in decimal degrees based on desired grid area and latitude
def calculate_cell_size(grid_area_km2, latitude_degrees):
    '''
    This function calculates the cell size in degrees based on a given grid size in km² and the latitude coordinate.
    :param grid_area_km2: Wanted grid are in km².
    :param latitude_degrees: The latitude coordinate at which the grid size in degrees need to be calculated.
    :return: The degrees of the cell size used to split Belgium up in different grids of given area in km².
    '''
    # Convert latitude to radians for trigonometric functions
    latitude_rad = np.radians(latitude_degrees)

    # Conversion factor from meters to decimal degrees for latitude
    meters_to_degrees = 1 / (111.32 * 1000 * np.cos(latitude_rad))

    # Calculate width of the square grid cell in meters
    width_meters = np.sqrt(grid_area_km2 * 1000000)

    # Calculate cell size in decimal degrees
    cell_size_degrees = width_meters * meters_to_degrees

    return cell_size_degrees