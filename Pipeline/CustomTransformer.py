import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.impute import KNNImputer
from sklearn.base import BaseEstimator, TransformerMixin


# Custom Transformer to Split DataFrame into NaN and Non-NaN DataFrames
class DataFrameSplitter(BaseEstimator, TransformerMixin):
    def __init__(self, column):
        self.column = column

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        self.without_nan = X[~X[self.column].isna()]
        self.with_nan = X[X[self.column].isna()]
        return self.without_nan, self.with_nan


# Custom Transformer to Apply Isolation Forest and Filter Inliers
class IsolationForestFilter(BaseEstimator, TransformerMixin):
    def __init__(self, column, random_state=45):
        self.column = column
        self.random_state = random_state

    def fit(self, X, y=None):
        self.IsoFo = IsolationForest(n_estimators=100, contamination='auto', random_state=self.random_state)
        self.IsoFo.fit(X[[self.column]])
        return self

    def transform(self, X):
        y_labels = self.IsoFo.predict(X[[self.column]])
        self.filtered_data = X[y_labels == 1]
        self.discarded_data = X[y_labels == -1]
        return self.filtered_data


# Custom Transformer to Impute Missing Values Based on Vector Type
class KNNImputerByGroup(BaseEstimator, TransformerMixin):
    def __init__(self, group_column, feature_groups, n_neighbors=5):
        self.group_column = group_column
        self.feature_groups = feature_groups
        self.n_neighbors = n_neighbors

    def fit(self, X, y=None):
        self.knn_imputer = KNNImputer(n_neighbors=self.n_neighbors)
        return self

    def transform(self, X):
        imputed_groups = []
        for group, features in self.feature_groups.items():
            group_data = X[X[self.group_column] == group]
            if not group_data.empty:
                imputed_values = self.knn_imputer.fit_transform(group_data[features])
                imputed_df = pd.DataFrame(imputed_values, columns=features, index=group_data.index)
                group_data.loc[:, features] = imputed_df[features]
                imputed_groups.append(group_data)
        return pd.concat(imputed_groups, axis=0)