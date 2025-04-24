import pandas as pd

def load_data(path: str):

    """
    Carica il file CSV in un DataFrame pandas.
    """
    df = pd.read_csv(path)
    data = df.copy()
    return data


def report_missing(df: pd.DataFrame):
    """
    Restituisce il numero di valori mancanti per ogni colonna.
    """
    missing = df.isnull().sum()
    print("Valori mancanti per colonna:")
    print(missing)
    return missing


def fill_city_with_country(df: pd.DataFrame, city_col: str = 'city', country_col: str = 'country'):
    """
    Sostituisce i valori nulli nella colonna 'city' con i rispettivi valori della colonna 'country'.
    """
    if city_col not in df.columns or country_col not in df.columns:
        raise KeyError(f"Colonne {city_col} o {country_col} non presenti nel DataFrame")
    df[city_col] = df[city_col].fillna(df[country_col])
    return df




def drop_duplicates(df: pd.DataFrame):
    """
    Rimuove le righe duplicate dal DataFrame.
    """
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)
    print(f"Righe prima: {before}, dopo drop duplicates: {after}")
    return df



def drop_missing_investors(df: pd.DataFrame, investors_col: str = 'select_investors'):
    """
    Rimuove le righe dove la colonna 'investors' è nulla.
    """
    if investors_col not in df.columns:
        raise KeyError(f"Colonna {investors_col} non presente nel DataFrame")
    before = len(df)
    df = df.dropna(subset=[investors_col])
    after = len(df)
    print(f"Righe prima: {before}, dopo drop investitori nulli: {after}")
    return df


def clean_dataframe(path: str):
    """
    Pipeline completa di caricamento, report missing, pulizia e rimozione duplicati.
    """
    df = load_data(path)
    report_missing(df)
    df = fill_city_with_country(df)
    df = drop_missing_investors(df)
    df = drop_duplicates(df)
    print("Pulizia completata.")
    return df



if __name__ == '__main__':
    
    file_path = 'unicorns.csv'
    df_clean = clean_dataframe(file_path)
    # Salva il DataFrame pulito su un nuovo CSV se desiderato
    df_clean.to_csv('unicorns_cleaned.csv', index=False)
    print("DataFrame pulito salvato in 'unicorns_cleaned.csv'")