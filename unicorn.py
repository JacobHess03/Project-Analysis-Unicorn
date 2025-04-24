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

    inizio = data.sort_values('date_joined').groupby(['anno', 'industry', 'company']).first().reset_index()
    fine = data.sort_values('date_joined').groupby(['anno', 'industry', 'company']).last().reset_index()

    trend = pd.merge(inizio, fine, on=['anno', 'industry', 'company'], suffixes=('_inizio', '_fine'))
    return trend[['anno', 'industry', 'company', 'valuation_inizio', 'valuation_fine']]

if __name__ == '__main__':
    percorso_file = 'unicorns.csv'
    df = pulisci_dati(percorso_file)

    print("Top 10 aziende per valuation più alta:")
    print(top_aziende(df, 10))

    print("Top 10 aziende per valuation più bassa:")
    print(down_aziende(df, 10))

    print("Aziende con valuation più alta per paese:")
    print(aziende_top_per_paese(df))

    print("Industria con più aziende:")
    print(industria_piu_frequente(df).head(1))

    print("Andamento annuale delle aziende per industry:")
    print(andamento_annuale_per_industria(df).head(20))

    df.to_csv('unicorns_cleaned.csv', index=False)
    print("Dati puliti salvati in 'unicorns_cleaned.csv'")
