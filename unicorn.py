import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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

    aggregazione = data.groupby(['anno', 'industry']).agg({
        'valuation': ['mean', 'count'],
        'company': 'nunique'
    })
    
    aggregazione.columns = ['valuation_media', 'valuation_count', 'num_aziende']
    return aggregazione.reset_index()

def mostra_menu():
    print("\n" + "="*50)
    print("MENU VISUALIZZAZIONE GRAFICI")
    print("="*50)
    print("1. Top 10 aziende per valuation")
    print("2. Bottom 10 aziende per valuation")
    print("3. Aziende top per paese")
    print("4. Industrie più frequenti")
    print("5. Andamento annuale per industria")
    print("6. Esci")
    return input("Seleziona un'opzione (1-6): ")

def genera_grafico(df, scelta):
    plt.figure(figsize=(12, 7))
    
    if scelta == "1":
        data = top_aziende(df, 10)
        sns.barplot(x='valuation', y='company', data=data, palette='rocket')
        plt.title('Top 10 Aziende per Valuation')
        plt.xlabel('Valuation (miliardi $)')
        plt.ylabel('')
        
    elif scelta == "2":
        data = down_aziende(df, 10)
        sns.barplot(x='valuation', y='company', data=data, palette='mako')
        plt.title('Bottom 10 Aziende per Valuation')
        plt.xlabel('Valuation (miliardi $)')
        plt.ylabel('')
        
    elif scelta == "3":
        data = aziende_top_per_paese(df).sort_values('valuation', ascending=False).head(15)
        sns.barplot(x='valuation', y='country', data=data, palette='viridis')
        plt.title('Aziende con Valuation più Alta per Paese (Top 15)')
        plt.xlabel('Valuation (miliardi $)')
        plt.ylabel('Paese')
        
    elif scelta == "4":
        data = industria_piu_frequente(df).head(10)
        sns.barplot(x=data.values, y=data.index, palette='flare')
        plt.title('Top 10 Industrie più Frequenti')
        plt.xlabel('Numero di Aziende')
        plt.ylabel('Industria')
        
    elif scelta == "5":
        data = andamento_annuale_per_industria(df)
        sns.lineplot(x='anno', y='valuation_media', hue='industry', 
                    data=data, marker='o', palette='tab20')
        plt.title('Andamento Valuation Medio per Industria')
        plt.xlabel('Anno')
        plt.ylabel('Valuation Media (miliardi $)')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    try:
        percorso_file = 'unicorns.csv'
        df = pulisci_dati(percorso_file)
        df.to_csv('unicorns_cleaned.csv', index=False)
        print("Dati puliti salvati in 'unicorns_cleaned.csv'")
        
        while True:
            scelta = mostra_menu()
            
            if scelta == "6":
                print("Grazie per aver utilizzato il sistema!")
                break
                
            if scelta in ["1", "2", "3", "4", "5"]:
                genera_grafico(df, scelta)
            else:
                print("Opzione non valida. Riprovare.")
                
        df.to_csv('unicorns_cleaned.csv', index=False)
        print("Dati puliti salvati in 'unicorns_cleaned.csv'")
        
    except Exception as e:
        print(f"Si è verificato un errore: {e}")