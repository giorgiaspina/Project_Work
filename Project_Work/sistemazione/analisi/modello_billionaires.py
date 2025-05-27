from modello_base import ModelloBase
import pandas as pd
from scipy.stats import chi2_contingency, contingency, spearmanr
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

colonne_da_rinominare = {
    "finalWorth": "patrimonio_finale",
    "personName": "nome_persona",
    "age": "eta",
    "country": "paese",
    "city": "citta",
    "source": "fonte_reddito",
    "industries": "industrie",
    "countryOfCitizenship": "paese_cittadinanza",
    "organization": "organizzazione",
    "selfMade": "self_made",
    "gender": "genere",
    "state": "stato"
}
variabili_da_drop =["date", "latitude_country","longitude_country",
                    "rank","birthMonth", "birthDay",
                    "gross_primary_education_enrollment_country",
                    "gross_tertiary_education_enrollment","status",
                    "birthDate", "lastName","firstName","birthYear",
                    "cpi_country", "cpi_change_country","title",
                    "gdp_country","life_expectancy_country",
                    "tax_revenue_country_country",
                    "total_tax_rate_country", "population_country",
                    "residenceStateRegion","category"]

variabili_da_drop_genere =["date", "latitude_country","finalWorth","state","selfMade","organization","industries",
                        "longitude_country", "rank","birthMonth", "birthDay", "countryOfCitizenship","source",
                        "gross_primary_education_enrollment_country","city","country","age",
                        "gross_tertiary_education_enrollment","status","birthDate", "lastName",
                        "firstName","birthYear", "cpi_country", "cpi_change_country","title",
                        "gdp_country","life_expectancy_country", "tax_revenue_country_country",
                        "total_tax_rate_country", "population_country", "residenceStateRegion","category","personName"]

variabili_da_drop_industrie =["date", "latitude_country","finalWorth","state","selfMade","organization","gender",
                        "longitude_country", "rank","birthMonth", "birthDay", "countryOfCitizenship","source",
                        "gross_primary_education_enrollment_country","city","country","age",
                        "gross_tertiary_education_enrollment","status","birthDate", "lastName",
                        "firstName","birthYear", "cpi_country", "cpi_change_country","title",
                        "gdp_country","life_expectancy_country", "tax_revenue_country_country",
                        "total_tax_rate_country", "population_country", "residenceStateRegion","category","personName"]


class ModelloBillionaires(ModelloBase):


    def __init__(self,dataset_path):
        self.dataframe=pd.read_csv(dataset_path)
        self.dataframe_sistemato= self.sistemazione_dataframe()
        self.dataframe_sistemato_genere = self.sistemazione_dataframe_genere()
        self.dataframe_sistemato_industrie = self.sistemazione_dataframe_industrie()



# metodo di istanza per sistemazione dataframe
    def sistemazione_dataframe(self):
        # drop colonne
        df_sistemato = self.dataframe.drop(variabili_da_drop, axis=1)

        #sostituzione valori nan colonna age con mediana
        df_sistemato["age"] = df_sistemato["age"].fillna(df_sistemato["age"].median())

        # rinomina colonne
        df_sistemato = df_sistemato.rename(columns= colonne_da_rinominare)

        # Creazione colonna "fascia_eta"
        bins = [0, 39, 60, df_sistemato["eta"].max()]
        labels = ["Under 40", "40-60", "Over 60"]
        df_sistemato["fascia_eta"] = pd.cut(df_sistemato["eta"], bins=bins, labels=labels, right=True)
        df_sistemato["codice_fascia_eta"] = df_sistemato["fascia_eta"].cat.codes

        #  conversione di tipo float in tipo int
        df_sistemato["eta"] = df_sistemato["eta"].astype(int)

        # sostituzione valori con id per industria e genere
        df_sistemato['genere'] = df_sistemato['genere'].map({'M': 1, 'F': 2})
        df_sistemato['industrie'] = df_sistemato['industrie'].map({'Fashion & Retail': 1,
                                                                   'Automotive': 2,
                                                                   'Technology': 3,
                                                                   'Finance & Investments': 4,
                                                                   'Media & Entertainment': 5,
                                                                   'Telecom': 6,
                                                                   'Diversified': 7,
                                                                   'Food & Beverage': 8,
                                                                   'Logistics': 9,
                                                                   'Gambling & Casinos': 10,
                                                                   'Manufacturing': 11,
                                                                   'Real Estate': 12,
                                                                   'Metals & Mining': 13,
                                                                   'Energy': 14,
                                                                   'Healthcare': 15,
                                                                   'Service': 16,
                                                                   'Construction & Engineering': 17,
                                                                   'Sports': 18, })

        return df_sistemato



    def sistemazione_dataframe_genere(self):
        # Rimuovo colonne che non servono
        # axis=1 indica che stiamo rimuovendo colonne
        df_sistemato = self.dataframe.drop(variabili_da_drop_genere, axis=1)

        # Prendiamo i valori unici della colonna "gender" dal dataframe pulito, escludendo i valori NaN (dropna())
        valori_univoci = df_sistemato["gender"].dropna().unique()

        # Creazione di un nuovo dataframe contenente solo la colonna "gender" con i valori unici estratti
        df_sistemato = pd.DataFrame(valori_univoci, columns=['gender'])
        return df_sistemato



    def sistemazione_dataframe_industrie(self):
        # Rimuovo colonne che non servono
        df_sistemato = self.dataframe.drop(variabili_da_drop_industrie, axis=1)

        # Estrazione dei valori unici dalla colonna "industries" del dataframe ripulito, eliminando eventuali valori NaN
        valori_univoci = df_sistemato["industries"].dropna().unique()

        # Creazione di un nuovo dataframe composto da una singola colonna "industries", contenente solo i valori unici estratti
        df_sistemato = pd.DataFrame(valori_univoci, columns=['industries'])
        return df_sistemato




    # metodo per ottenere tabelle di contingenze - test chi quadro e Cramer (correlazione variabili categoriali)
    def tabella_contingenza(self, column, target):
    # generazione e stampa della tabella di contingenza
        tabella_contingenza = pd.crosstab(self.dataframe_sistemato[column], self.dataframe_sistemato[target])
        print(f"\nTABELLA DI CONTINGENZA {column}--{target}:\n", tabella_contingenza,sep="\n")
    # test chi quadro e stampa esito
        chi2, p, dof, expected = chi2_contingency(tabella_contingenza)
        print(f"\nI p-value risultante dal test del chi quadro sulla tabella di contingenza {column}--{target} è: {p}")
        print(f"\nNotazione non scientifica del p- value -> {format(p,".53f")}") #limite massimo decimali
    # calcolo indice di cramer e stampa valore
        cramer = contingency.association(tabella_contingenza, method="cramer")
        print(f"\nL'indice di Cramer calcolato sulla tabella di contingenza {column}-{target} è pari a -> {cramer}")
        return tabella_contingenza



# p-value -> probabilità che la relazione osservata sia dovuta al caso. Più è basso, più è significativa l’associazione.
    # valore ottenuto -> 0.007421490591949356 -> Relazione significativa

        # > 0.05  -> Nessuna evidenza di relazione
        # ≤ 0.05  -> Relazione significativa
        # ≤ 0.01  -> Relazione molto significativa
        # ≤ 0.001 -> Altamente significativa

# CRAMER
    # risultato: 0.11471 correlazione bassa

        # 0-0.1   -> Correlazione debole
        # 0.1-0.3 -> Correlazione bassa -
        # 0.3-0.5 -> Correlazione moderata
        # 0.5-0.7 -> Correlazione alta
        # 0.7-0.9 -> Correlazione molto alta
        # 0.9-1   -> Correlazione perfetta



# metodo per ottenere correlazione di Spearman (correlazione tra variabile quantitativa e categoriale)
    def correlazione_spearman(self, column, target):
        spearman_corr, p = spearmanr(self.dataframe_sistemato[column],self.dataframe_sistemato[target])
        print(f"La correlazione di Spearman risultante tra {column} e {target} risulta pari a: {spearman_corr}")
        print(f"Il p value sulla correlazione di Spearman tra {column} e {target} risulta pari a: {p}")


 # SPEARMAN
    #risultato spearman: 0.10910788432541906 -> debole correlazione
    # risultato p-value : 1.9074197748833545e-08 -> correlazione debole ma significativa

        # -1 correlazione negativa perfette (quando una variabile aumenta, l’altra diminuisce sempre)
        # 0 nessuna correlazione (le variabili non si muovono insieme)
        # 1 correlazione positiva perfetta (quando una variabile aumenta, anche l'altra aumenta sempre)



# regressione lineare eta e patrimonio
    def regressione_lineare_semplice(self):
        # Definizione target e regressore
        y = self.dataframe_sistemato[["patrimonio_finale"]].values.reshape(-1, 1)  # TARGET
        x = self.dataframe_sistemato[["eta"]].values.reshape(-1, 1)  # REGRESSORE
        # Standardizzazione
        scaler = StandardScaler()
        x_scaled = scaler.fit_transform(x)
        # Creazione e addestramento del modello
        regressione = LinearRegression()
        regressione.fit(x_scaled, y)
        # Punteggio del modello
        print("\n****** PUNTEGGIO MODELLO REGRESSIONE *****")
        print(regressione.score(x_scaled, y))
        # Predizione della retta di regressione
        retta_regressione = regressione.predict(x_scaled)

        # Grafico
        plt.scatter(x, y, label="Osservazioni", s=10, color="steelblue")
        plt.plot(x, retta_regressione, color="darkred", label="Regressione Lineare", linewidth=1.5)
        plt.title("Regressione Lineare tra Età e Patrimonio")
        plt.xlabel("Età")
        plt.ylabel("Patrimonio Finale (milioni di dollari)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()






# UTILIZZO MODELLO

# utilizzo del dataset
modello = ModelloBillionaires("../dataset/billionaires_statistics_dataset.csv")

# analisi generali dataframe
# modello.analisi_generali(modello.dataframe_sistemato)
# modello.analisi_valori_univoci(modello.dataframe_sistemato)


# analisi statistica
#modello.tabella_contingenza("genere", "industrie")
modello.correlazione_spearman("codice_fascia_eta", "patrimonio_finale")
#modello.regressione_lineare_semplice()


# creazione file csv con modifiche fatte
#modello.dataframe_sistemato.to_csv("../dataset_sistemato/billionaires_sistemato.csv", index=False)
# modello.dataframe_sistemato_genere.to_csv("../dataset_sistemato/genere.csv", index=False)
# modello.dataframe_sistemato_industrie.to_csv("../dataset_sistemato/industria.csv", index=False)
