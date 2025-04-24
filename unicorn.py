import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
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

def boxplot_valuation_per_industria(df):
    """
    Mostra la distribuzione della valuation per industria con un boxplot.
    """
    df_plot = df.dropna(subset=['industry', 'valuation'])
    
    # Prendiamo solo le industrie più rappresentate
    top_industrie = df_plot['industry'].value_counts().head(10).index
    df_plot = df_plot[df_plot['industry'].isin(top_industrie)]
    
    plt.figure(figsize=(14, 8))
    sns.boxplot(data=df_plot, x='valuation', y='industry', palette='coolwarm', showfliers=False)
    plt.title('Distribuzione della Valuation per Industria (Top 10)')
    plt.xlabel('Valuation (miliardi $)')
    plt.ylabel('Industria')
    plt.tight_layout()
    plt.show()


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


# Aggiungi questa nuova funzione per le previsioni
def previsioni_valuation(df):
    # 1) Preparazione dei dati
    data = andamento_annuale_per_industria(df)
    data = data[['anno', 'industry', 'valuation_media']].dropna()
    
    # Se non ci sono dati, esci
    if data.empty:
        print("Nessun dato disponibile per le previsioni.")
        return
    
    # 2) Definizione del range di anni futuri
    max_anno = data['anno'].max()
    # Qui creiamo un array colonna con gli anni max_anno+1...max_anno+5
    anni_futuri = np.arange(max_anno + 1, max_anno + 6).reshape(-1, 1)
    
    # Imposto dimensioni del grafico
    plt.figure(figsize=(14, 8))
    
    # 3) Selezione delle top 5 industrie
    #    in base alla valuation_media media storica
    top_industrie = data\
        .groupby('industry')['valuation_media']\
        .mean()\
        .nlargest(5)\
        .index
    
    # 4) Ciclo su ciascuna delle top industrie
    for industria in top_industrie:
        # Filtra solo i dati di quest’industria
        industria_data = data[data['industry'] == industria]
        
        # Serve almeno 3 punti per adattare un polinomio di grado 2
        if len(industria_data) < 3:
            continue
        
        # X = anni (es. [[2015], [2016], ...]); y = valuation_media di quell’anno
        X = industria_data[['anno']].values
        y = industria_data['valuation_media'].values
        
        # 5) Costruzione e training del modello
        #    Pipeline che trasforma x → [1, x, x²] + regressione lineare
        model = make_pipeline(PolynomialFeatures(2), LinearRegression())
        model.fit(X, y)
        
        # 6) Generazione delle previsioni
        #    - unisco i valori storici X.flatten() con gli anni futuri
        anni_totali = np.concatenate([X.flatten(), anni_futuri.flatten()])
        #    - riformo in colonna per predict()
        previsioni = model.predict(anni_totali.reshape(-1, 1))
        
        # 7) Plot dei risultati
        #    • Storico: punti e linee per gli anni passati
        plt.plot(industria_data['anno'], y, 'o-', label=f'{industria} Storico')
        #    • Previsioni: gli ultimi 5 valori calcolati sul polinomio
        plt.plot(anni_futuri, previsioni[-5:], 's--', label=f'{industria} Previsioni')
    
    # 8) Rifinitura del grafico
    plt.title(f'Previsioni Valuation 5 Anni ({max_anno + 1}-{max_anno + 5}) - Top Industrie')
    plt.xlabel('Anno')
    plt.ylabel('Valuation Media (Miliardi $)')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    plt.show()



def mostra_menu():
    print("\n" + "="*50)
    print("MENU VISUALIZZAZIONE GRAFICI")
    print("="*50)
    print("1. Top 10 aziende per valuation")
    print("2. Distribuzione della valuation per industria (boxplot)")
    print("3. Aziende top per paese")
    print("4. Industrie più frequenti")
    print("5. Andamento annuale per industria")
    print("6. Previsioni future per industria per i prossimi 5 anni")
    print("7. Esci")
    return input("Seleziona un'opzione (1-7): ")

def genera_grafico(df, scelta):
    if scelta == "1":
        plt.figure(figsize=(12, 7))
        data = top_aziende(df, 10)
        sns.barplot(x='valuation', y='company', data=data, palette='rocket')
        plt.title('Top 10 Aziende per Valuation')
        plt.xlabel('Valuation (miliardi $)')
        plt.ylabel('')
        plt.tight_layout()
        plt.show()
        
    elif scelta == "2":
        boxplot_valuation_per_industria(df)
        
    elif scelta == "3":
        plt.figure(figsize=(12, 7))
        data = aziende_top_per_paese(df).sort_values('valuation', ascending=False).head(15)
        sns.barplot(x='valuation', y='country', data=data, palette='viridis')
        plt.title('Aziende con Valuation più Alta per Paese (Top 15)')
        plt.xlabel('Valuation (miliardi $)')
        plt.ylabel('Paese')
        plt.tight_layout()
        plt.show()
        
    elif scelta == "4":
        plt.figure(figsize=(12, 7))
        data = industria_piu_frequente(df).head(10)
        sns.barplot(x=data.values, y=data.index, palette='flare')
        plt.title('Top 10 Industrie più Frequenti')
        plt.xlabel('Numero di Aziende')
        plt.ylabel('Industria')
        plt.tight_layout()
        plt.show()
        
    elif scelta == "5":
        plt.figure(figsize=(12, 7))
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
                
                previsioni_valuation(df)
            
            if scelta == "7":
                print("Grazie per aver utilizzato il sistema!")
                break
                
            if scelta in ["1", "2", "3", "4", "5"]:
                genera_grafico(df, scelta)
            else:
                print("Opzione non valida. Riprovare.")
                
        
        
    except Exception as e:
        print(f"Si è verificato un errore: {e}")