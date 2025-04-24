import pandas as pd

def carica_dati(percorso):
    return pd.read_csv(percorso).copy()

def mostra_valori_nulli(df):
    print("Valori nulli per colonna:")
    print(df.isnull().sum())

def completa_city_con_country(df):
    df['city'] = df['city'].fillna(df['country'])
    return df

def rimuovi_righe_senza_investitori(df):
    return df.dropna(subset=['select_investors'])

def rimuovi_duplicati(df):
    return df.drop_duplicates()

def pulisci_dati(percorso):
    df = carica_dati(percorso)
    mostra_valori_nulli(df)
    df = completa_city_con_country(df)
    df = rimuovi_righe_senza_investitori(df)
    df = rimuovi_duplicati(df)
    # Assicuriamoci che valuation sia numerica e senza NaN
    # Prima di convertire, pulisci eventuali simboli di valuta o virgole
    if df['valuation'].dtype == object:
        df['valuation'] = df['valuation'].replace('[\$,]', '', regex=True)
    df['valuation'] = pd.to_numeric(df['valuation'], errors='coerce')
    df = df.dropna(subset=['valuation'])
    print("Pulizia completata. Valuation NaN rimosse.")
    return df

def top_aziende(df, n=10):
    return df.sort_values('valuation', ascending=False).head(n)

def down_aziende(df, n=10):
    return df.sort_values('valuation', ascending=True).head(n)

def aziende_top_per_paese(df):
    data = df.dropna(subset=['country', 'valuation'])
    idx = data.groupby('country')['valuation'].idxmax()
    return data.loc[idx].reset_index(drop=True)

def industria_piu_frequente(df):
    return df['industry'].value_counts()

def andamento_annuale_per_industria(df):
    data = df.copy()
    data['date_joined'] = pd.to_datetime(data['date_joined'], errors='coerce')
    data = data.dropna(subset=['date_joined'])
    data['valuation'] = pd.to_numeric(data['valuation'], errors='coerce')
    data = data.dropna(subset=['valuation', 'industry'])
    data['anno'] = data['date_joined'].dt.year

    # Questa parte è stata corretta per calcolare statistiche aggregate per anno e industria
    # invece di tentare di mescolare i dati di inizio e fine anno
    aggregazione = data.groupby(['anno', 'industry']).agg({
        'valuation': ['mean', 'count'],
        'company': 'nunique'
    })
    
    # Rinomino le colonne per chiarezza
    aggregazione.columns = ['valuation_media', 'valuation_count', 'num_aziende']
    
    # Reset dell'indice per avere un dataframe regolare
    return aggregazione.reset_index()

if __name__ == '__main__':
    try:
        percorso_file = 'unicorns.csv'
        df = pulisci_dati(percorso_file)

        print("\nTop 10 aziende per valuation più alta:")
        print(top_aziende(df, 10))

        print("\nTop 10 aziende per valuation più bassa:")
        print(down_aziende(df, 10))

        print("\nAziende con valuation più alta per paese:")
        print(aziende_top_per_paese(df))

        print("\nIndustria con più aziende:")
        print(industria_piu_frequente(df).head(1))

        print("\nAndamento annuale delle aziende per industry:")
        print(andamento_annuale_per_industria(df).head(20))

        df.to_csv('unicorns_cleaned.csv', index=False)
        print("Dati puliti salvati in 'unicorns_cleaned.csv'")
    except Exception as e:
        print(f"Si è verificato un errore: {e}")