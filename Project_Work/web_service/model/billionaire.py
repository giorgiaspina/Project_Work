from cerberus import  Validator

class Billionaire:

    schema_registrazione = {
        "patrimonio_finale":
                        {
                        "required": True,
                        "type": "integer"

                        },
        "nome_persona": {
                        "required": True,
                        "type": "string",
                        "regex": "^[a-zA-Zàéèìòù&\\s']{1,40}$"
                        },
        "eta":{
                        "required": True,
                        "type": "integer",
                        },

        "paese":{
                        "required": True,
                        "type": "string",
                        "regex": "^[a-zA-Zàéèìòù\\s']{1,24}$"
                        },
        "citta": {
                        "required": True,
                        "type": "string",
                        "regex": "^[a-zA-Zàéèìòù\\s']{1,24}$"
                        },
        "fonte_reddito":{
                        "required": True,
                        "type": "string",
                        "regex": "^[a-zA-Zàéèìòù\\s']{1,35}$"
                        },
        "industrie":{
                        "required": True,
                        "type": "dict",
                        "schema":{
                    "industries":{
                        "required": True,
                        "type": "string",
                        "regex": "^[a-zA-Zàéèìòù\\s']{1,26}$"
                                 }
                               }
                        },
        "paese_cittadinanza":{
                        "required": True,
                        "type": "string",
                        "regex": "^[a-zA-Zàéèìòù\\s']{1,20}$"
        },
        "organizzazione": {
                        "required": True,
                        "type": "string",
                        "regex": "^[a-zA-Zàéèìòù&\\s']{1,46}$"
        },
        "self_made": {
                        "required": True,
                        "type": "string",
                        "allowed": ["True","False"]
        },
        "genere": {
                        "required": True,
                        "type": "integer",
                        "allowed": [1,2]

        },
        "stato": {
                        "required": True,
                        "type": "string",
                        "regex": "^[a-zA-Zàéèìòù\\s']{1,19}$"
        },
        "fascia_eta": {
                        "required": True,
                        "type": "string",
                        "allowed": ["Over 60", "40-60","Under 40"]
        },
        "codice_fascia_eta":{
            "required": True,
            "type": "integer",
            "allowed": [0,1,2]
        }
    }



    def __init__(self,id=None,patrimonio_finale=None,nome_persona=None,eta=None,paese=None,
                 citta=None,fonte_reddito=None,industrie=None, paese_cittadinanza = None,
                 organizzazione=None,self_made=None,genere=None,stato=None,
                 fascia_eta=None,codice_fascia_eta=None):
        self.id = id
        self.patrimonio_finale = patrimonio_finale
        self.nome_persona = nome_persona
        self.eta = eta
        self.paese = paese
        self.citta = citta
        self.fonte_reddito = fonte_reddito
        self.industrie = industrie
        self.paese_cittadinanza = paese_cittadinanza
        self.organizzazione = organizzazione
        self.self_made = self_made
        self.genere = genere
        self.stato = stato
        self.fascia_eta = fascia_eta
        self.codice_fascia_eta = codice_fascia_eta



    # metodo per deserializzazione  json -> oggetto
    @classmethod
    def deserializzazione(cls,json):
        return cls(**json)


    # metodo per serializzazione  oggetto -> json
    def serializzazione(self):
        return self.__dict__


    def serializzazione_elenco_miliardari(self):
        return {
            "nome_persona": self.nome_persona,
            "fascia_eta": self.fascia_eta,
            "patrimonio_finale":self.patrimonio_finale,
            "paese_cittadinanza":self.paese_cittadinanza,
            "genere":self.genere,
            "industrie" : self.industrie
        }

    def serializzazione_paese(self):
        return {
            "nome_persona":self.nome_persona,
            "paese_cittadinanza":self.paese_cittadinanza,
            "paese" : self.paese,
            "stato" : self.stato,
            "citta" : self.citta
        }

    def serializzazione_self_made(self):
        return {
            "nome_persona":self.nome_persona,
            "industrie":self.industrie ,
            "fonte_reddito" : self.fonte_reddito,
            "self_made" :self.self_made,
            "fascia_eta" : self.fascia_eta
        }


    def serializzazione_fascia_eta(self):
        return{
            "nome_persona":self.nome_persona,
            "fascia_eta" :self.fascia_eta,
            "patrimonio_finale" :self.patrimonio_finale,
            "fonte_reddito" : self.fonte_reddito,
            "citta" : self.citta
        }

        # metodo per validazione dati di registrazione
    @classmethod
    def validazione_registrazione(cls, json):
        validatore = Validator(cls.schema_registrazione)
        if validatore.validate(json):
            return True,  # ritorna una tupla
        else:
            return False, validatore.errors