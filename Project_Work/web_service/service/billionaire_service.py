from web_service.repository.repository import Repository
from  web_service.model.billionaire import Billionaire

class BillionaireService:

    def __init__(self):
        self.repository= Repository()


    # elenco miliardari
    def elenco_miliardari(self):
        sql= "SELECT * FROM elenco_miliardari"
        ottenuto_db = self.repository.recupero_multiplo(sql)
        if isinstance(ottenuto_db, str):
            return {"codice": 500, "messaggio": ottenuto_db}, 500
        miliardari =[]
        for record in ottenuto_db:
            miliardario = Billionaire(nome_persona=record[0],fascia_eta=record[1],patrimonio_finale=record[2],
                                      paese_cittadinanza=record[3],industrie=record[4],genere=record[5])
            miliardari.append(miliardario.serializzazione_elenco_miliardari())
        return miliardari


    # elenco miliardari
    def elenco_miliardari_per_paese(self):
        sql = "SELECT * FROM miliardari_paesi"
        ottenuto_db = self.repository.recupero_multiplo(sql)
        if isinstance(ottenuto_db, str):
            return {"codice": 500, "messaggio": ottenuto_db}, 500
        miliardari = []
        for record in ottenuto_db:
            miliardario = Billionaire(nome_persona=record[0],
                                      paese_cittadinanza=record[1],paese=record[2],stato=record[3],citta=record[4])
            miliardari.append(miliardario.serializzazione_paese())
        return miliardari

        # elenco miliardari

    def elenco_miliardari_u40_self_made(self, self_made):
        if self_made == 'False':
            sql = "SELECT * FROM miliardari_u40self_made_false"
            ottenuto_db = self.repository.recupero_multiplo(sql)
            if isinstance(ottenuto_db, str):
                return {"codice": 500, "messaggio": ottenuto_db}, 500
            miliardari = []
            for record in ottenuto_db:
                miliardario = Billionaire(nome_persona=record[0],
                                          industrie=record[1], fonte_reddito=record[2], self_made=record[3], fascia_eta=record[4])
                miliardari.append(miliardario.serializzazione_self_made())
            return miliardari

        else:
            sql = "SELECT * FROM miliardari_u40self_made_true"
            ottenuto_db = self.repository.recupero_multiplo(sql)
            if isinstance(ottenuto_db, str):
                return {"codice": 500, "messaggio": ottenuto_db}, 500
            miliardari = []
            for record in ottenuto_db:
                miliardario = Billionaire(nome_persona=record[0],
                                          industrie=record[1], fonte_reddito=record[2], self_made=record[3], fascia_eta=record[4])
                miliardari.append(miliardario.serializzazione_self_made())
            return miliardari



    def elenco_miliardari_fascia_eta(self, codice_fascia_eta):
        if codice_fascia_eta == 0:
            sql = "SELECT * FROM eta_under_40"
            ottenuto_db = self.repository.recupero_multiplo(sql)
            if isinstance(ottenuto_db, str):
                return {"codice": 500, "messaggio": ottenuto_db}, 500
            miliardari = []
            for record in ottenuto_db:
                miliardario = Billionaire(nome_persona=record[0],
                                          fascia_eta=record[1], patrimonio_finale=record[2], fonte_reddito=record[3], citta=record[4])
                miliardari.append(miliardario.serializzazione_fascia_eta())
            return miliardari
        elif codice_fascia_eta == 1:
            sql = "SELECT * FROM eta_40_60"
            ottenuto_db = self.repository.recupero_multiplo(sql)
            if isinstance(ottenuto_db, str):
                return {"codice": 500, "messaggio": ottenuto_db}, 500
            miliardari = []
            for record in ottenuto_db:
                miliardario = Billionaire(nome_persona=record[0],
                                          fascia_eta=record[1], patrimonio_finale=record[2], fonte_reddito=record[3],
                                          citta=record[4])
                miliardari.append(miliardario.serializzazione_fascia_eta())
            return miliardari
        else :
            sql = "SELECT * FROM eta_over_60"
            ottenuto_db = self.repository.recupero_multiplo(sql)
            if isinstance(ottenuto_db, str):
                return {"codice": 500, "messaggio": ottenuto_db}, 500
            miliardari = []
            for record in ottenuto_db:
                miliardario = Billionaire(nome_persona=record[0],
                                          fascia_eta=record[1], patrimonio_finale=record[2], fonte_reddito=record[3],
                                          citta=record[4])
                miliardari.append(miliardario.serializzazione_fascia_eta())
            return miliardari



    def aggiungere_miliardario(self, corpo_richiesta):
        # 1. Validazione dati in entrata
        esito_validazione = Billionaire.validazione_registrazione(corpo_richiesta)
        if not esito_validazione[0]:
            return {"codice": 400, "messaggio": esito_validazione[1]}, 400

        # 2. Estrazione nome industria dal corpo richiesta
        nome_industria = corpo_richiesta['industrie']['industries']

        # 3. Cerca se l'industria esiste già
        record_industria = self.repository.recupero_singolo(
            "SELECT id FROM industria WHERE industries = %s", (nome_industria,)
        )

        # 4. la inserisce nuova industria
        if record_industria:
            id_industria = record_industria[0]
        else:
            inserimento = self.repository.manipolazione(
                "INSERT INTO industria (industries) VALUES (%s)", (nome_industria,)
            )
            if isinstance(inserimento, str):  # errore durante l'inserimento
                return {"codice": 500, "messaggio": inserimento}, 500
            record_industria = self.repository.recupero_singolo(
                "SELECT id FROM industria WHERE industries = %s", (nome_industria,)
            )
            id_industria = record_industria[0]

        # 5. Deserializzazione corpo richiesta in oggetto
        miliardario = Billionaire.deserializzazione(corpo_richiesta)
        miliardario.industrie = id_industria  # assegna id industria

        # 6. Controllo unicità nome_persona
        if self.repository.recupero_singolo(
                "SELECT id FROM billionaires_sistemato WHERE nome_persona = %s", (miliardario.nome_persona,)
        ):
            return {"codice": 409, "messaggio": "Nome già presente"}, 409

        # 7. Inserimento nel database
        sql = """
            INSERT INTO billionaires_sistemato (
                patrimonio_finale, nome_persona, eta, paese, citta, fonte_reddito,
                industrie, paese_cittadinanza, organizzazione, self_made, genere,
                stato, fascia_eta, codice_fascia_eta
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        valori = (
            miliardario.patrimonio_finale,
            miliardario.nome_persona,
            miliardario.eta,
            miliardario.paese,
            miliardario.citta,
            miliardario.fonte_reddito,
            miliardario.industrie,
            miliardario.paese_cittadinanza,
            miliardario.organizzazione,
            miliardario.self_made,
            miliardario.genere,
            miliardario.stato,
            miliardario.fascia_eta,
            miliardario.codice_fascia_eta
        )

        ottenuto_db = self.repository.manipolazione(sql, valori)

        if isinstance(ottenuto_db, str):
            return {"codice": 500, "messaggio": ottenuto_db}, 500

        # Recupero dell'id del miliardario appena inserito
        record_id = self.repository.recupero_singolo(
            "SELECT id FROM billionaires_sistemato WHERE nome_persona = %s ORDER BY id DESC LIMIT 1",
            (miliardario.nome_persona,)
        )
        id_inserito = record_id[0] if record_id else None

        # Aggiunta dell'id alla risposta
        corpo_richiesta["id"] = id_inserito

        return {
            "codice": 201,
            "messaggio": "Miliardario Registrato",
            "dati_inseriti": corpo_richiesta
        }, 201




    def eliminare_miliardario(self, id):
        # Recupero del miliardario
        record = self.repository.recupero_singolo(
            "SELECT * FROM billionaires_sistemato WHERE id = %s", (id,)
        )

        if not record:
            return {"codice": 404, "messaggio": "Miliardario non trovato"}, 404

        id_industria = record[7]  # posizione del campo 'industrie' se è l'id dell'industria

        valori_ritorno = Billionaire(
            id=record[0],
            patrimonio_finale=record[1],
            nome_persona=record[2],
            eta=record[3],
            paese=record[4],
            citta=record[5],
            fonte_reddito=record[6],
            industrie=record[7],
            paese_cittadinanza=record[8],
            organizzazione=record[9],
            self_made=record[10],
            genere=record[11],
            stato=record[12],
            fascia_eta=record[13],
            codice_fascia_eta=record[14]
        )

        # Eliminazione del miliardario
        risultato = self.repository.manipolazione(
            "DELETE FROM billionaires_sistemato WHERE id = %s", (id,)
        )

        if isinstance(risultato, str):
            return {"codice": 500, "messaggio": risultato}, 500

        # Verifico se l'industria è ancora utilizzata da altri
        altri = self.repository.recupero_singolo(
            "SELECT id FROM billionaires_sistemato WHERE industrie = %s", (id_industria,)
        )

        if not altri:
            # Se nessuno usa più questa industria, la elimino
            self.repository.manipolazione(
                "DELETE FROM industria WHERE id = %s", (id_industria,)
            )

        return {
            "codice": 200,
            "messaggio": f"Miliardario con ID {id} eliminato",
            "contenuto": valori_ritorno.__dict__
        }, 200
