from abc import ABC

# definizione di una classe astratta per la centralizzazione operazioni comuni

class ModelloBase(ABC):

    #metodo per ottenimento informazioni generali
    @staticmethod
    def analisi_generali(df):
        print("\n******* ANALISI GENERALI DATAFRAME ********")
        print("\nPrime cinque osservazioni", df.head().to_string(), sep="\n")
        print("\nUltime cinque osservazioni", df.tail().to_string(), sep="\n")
        print("\nInformazioni generali Dataframe:")
        df.info()

    # METODO CONTROLLO VALORI UNIVOCI
    @staticmethod
    def analisi_valori_univoci(df,variabili_da_droppare=None):
        print("\n******* VALORI UNIVOCI DATAFRAME ********")
        if variabili_da_droppare:
            df =df.drop(variabili_da_droppare,axis=1)
        for col in df.columns:
            print(f"\nIn colonna {col} abbiamo {df[col].nunique()} valori univoci\n")
            for value in df[col].unique():
                print(value)
