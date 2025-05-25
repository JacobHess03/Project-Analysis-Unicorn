Analysis and Cleaning of the Unicorn Companies Dataset

This project aims to analyze and clean a dataset containing information on unicorn companies (startups valued over $1 billion), to then derive a series of useful statistics and significant insights.
Objective

Through a set of functionalities, the program:

    Cleans the dataset of null values and duplicates.
    Enriches missing data.
    Analyzes the distribution and evolution of company valuations.
    Generates statistics by industry and country.

Expected Dataset

The program starts with a CSV file named unicorns.csv, which must contain at least the following columns:

    company
    industry
    city
    country
    valuation
    select_investors
    date_joined

Implemented Functionalities

Data Loading & Cleaning

    carica_dati(percorso)
    Loads data from a CSV file and creates an independent copy.

    mostra_valori_nulli(df)
    Prints the number of null values for each column.

    completa_city_con_country(df)
    Replaces missing values in the city column with those from the country column.

    rimuovi_righe_senza_investitori(df)
    Removes rows that do not indicate investors (select_investors are null).

    rimuovi_duplicati(df)
    Removes any duplicate rows in the dataset.

    pulisci_dati(percorso)
    Executes the entire cleaning pipeline:
        Loading
        Displaying nulls
        Completing cities
        Removing rows without investors
        Removing duplicates
        Converting the valuation column to numeric
        Deleting rows with missing valuation

Statistical Analysis

    top_aziende(df, n=10)
    Returns the top n companies with the highest valuation.

    down_aziende(df, n=10)
    Returns the n companies with the lowest valuation.

    aziende_top_per_paese(df)
    Returns the highest-valued company for each country.

    industria_piu_frequente(df)
    Returns a count of companies by industry, sorted in descending order.

    andamento_annuale_per_industria(df)
    Returns a DataFrame showing the annual evolution of company valuations for each industry and company.

Program Execution
Bash

    python main

Authors: Giacomo Visciotti, Simone Verrengia, Giuseppe Del Vecchio
