#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  2 07:09:11 2025

@author: christopher_taylor
"""

import random
import numpy as np
from datetime import datetime, timedelta

def account_number_generator (n):
    """
    Generate a list of randomized account numbers. Can be useful for testing
    purposes when building scripts.
    
    Parameters
    ----------
    n : int
        Number of account numbers to be generated.

    Returns
    -------
    numbers : List 
        List of n 16-digit numbers.

    """
    numbers = [random.randint(10 ** 15, 10 ** 16 - 1) for _ in range(n)]
    
    return numbers 
    
    
def general_ledger_generator (n):
    """
    Generate a list of randomized general ledger numbers. Can be useful for 
    testing purposes when building scripts. 

    Parameters
    ----------
    n : int
        Number of general ledger accounts to generate.

    Returns
    -------
    numbers : list
        List of n general ledger accounts.

    """
    numbers = [random.randint(700000, 799999) for _ in range(n)]
    
    return numbers


def filter_out_general_ledgers (df, column):
    """
    Filter out accounts with less than 16 digits, usually general ledgers used 
    to pay vendors

    Parameters
    ----------
    df : dataframe
        Dataframe containing data.
    column : str
        Name of column containing the account numbers

    Returns
    -------
    df_filtered : dataframe

    """
    df_filtered = df[df[column].astype(str).str.len() >= 16]
    
    return df_filtered

    
def generate_random_dates(n, start_date, end_date):
    """
    Generate sequence of random dates

    Parameters
    ----------
    n : int
        Number of dates to generate.
    start_date : datetime
        datetime(year, month, day).
    end_date : datetime
        datetime(year, month, day).

    Returns
    -------
    list
        Randomly generated datesß.

    """
    return [
        start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        for _ in range(n)
    ]
    
    
def identify_outliers (df, column):
    """
    Identify outliers using interquartile range 

    Parameters
    ----------
    df : dataframe 
        Dataframe containing data to be examined 
    column : str

    Returns 
    ----------
    outliers : dataframe 
        Dataframe of outliers with same columns as the dataframe entered into the function
    """
    Q1 = np.percentile(df[column], 25)
    Q3 = np.percentile(df[column], 75)
    IQR = Q3 - Q1 

    # Define thresholds
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR 

    # Identify outliers
    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]

    return outliers