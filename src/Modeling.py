import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.compose import make_column_transformer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.model_selection import cross_validate
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import FunctionTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import (
    OneHotEncoder,
    StandardScaler,
)

def transform(df, word_features, categorical_features, numeric_features):
    """
    Transform and preprocess a DataFrame with different types of features.

    Parameters:
    - df (pandas.DataFrame): The input DataFrame containing the features to be transformed.
    - word_features (list of str): List of column names corresponding to text features in the DataFrame.
    - categorical_features (list of str): List of column names corresponding to categorical features in the DataFrame.
    - numeric_features (list of str): List of column names corresponding to numeric features in the DataFrame.

    Returns:
    - numpy.ndarray: The transformed array containing the preprocessed features.
    """
    
    # drop_features = ['Status', 'BusinessSubType', 'FOLDERYEAR', 'LicenceRSN', 'LicenceNumber', 'LicenceRevisionNumber',
    #     'BusinessName', 'BusinessTradeName', 'IssuedDate', 'ExpiredDate', 
    #     'Unit', 'UnitType', 'House', 'Street', 'ExtractDate', 'Geom', 'geo_point_2d']
    
    word_transformer = make_pipeline(
        SimpleImputer(strategy="most_frequent"),
        FunctionTransformer(np.reshape, kw_args={'newshape':-1}),
        CountVectorizer(binary=True)
    )

    categorical_transformer = make_pipeline(
        SimpleImputer(strategy="most_frequent"),
        OneHotEncoder(drop="if_binary", sparse_output=False, handle_unknown='ignore')
    )

    numeric_transformer = make_pipeline(
        SimpleImputer(strategy="median"),
        StandardScaler()
    )
    
    word_trans_arr = word_transformer.fit_transform(df[word_features])
    categorical_trans_arr = categorical_transformer.fit_transform(df[categorical_features])
    numeric_trans_arr = numeric_transformer.fit_transform(df[numeric_features])
    
    return np.hstack((word_trans_arr.toarray(), categorical_trans_arr, numeric_trans_arr))


def split_x_y(df, word_features, categorical_features, numeric_features):
    """
    Extracts features (X) and target variable (y) from a DataFrame.

    Parameters:
    - df (pandas.DataFrame): The input DataFrame containing both features and the target variable.
    - word_features (list of str): List of column names corresponding to text features in the DataFrame.
    - categorical_features (list of str): List of column names corresponding to categorical features in the DataFrame.
    - numeric_features (list of str): List of column names corresponding to numeric features in the DataFrame.

    Returns:
    - X (pandas.DataFrame): The features extracted from the input DataFrame.
    - y (pandas.Series): The target variable extracted from the "survival_status" column of the input DataFrame.

    Usage:
    >>> X, y = split_x_y(df, word_features, categorical_features, numeric_features)
    """

    X = df[word_features + categorical_features + numeric_features]
    y = df["survival_status"]
    return X, y