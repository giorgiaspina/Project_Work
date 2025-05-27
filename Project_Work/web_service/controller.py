from flask import Flask, request
from web_service.service.billionaire_service import BillionaireService


# istanziazione applicazione web di tipo Flask
app= Flask(__name__)

# istanziazione componenti service
miliardari_service= BillionaireService()


# endpoint elenco miliardari
# localhost:5000/miliardari/get
@app.get("/miliardari/get")
def endpoint_elenco_miliardari():
    return miliardari_service.elenco_miliardari()

# endpoint elenco miliardari per Paese
# localhost:5000/miliardari/paesi
@app.get("/miliardari/paesi")
def endpoint_paesi():
    return miliardari_service.elenco_miliardari_per_paese()


# endpoint elenco miliardari self_made (True/False)
# localhost:5000/miliardari/<string:self_made>
@app.get("/miliardari/<string:self_made>")
def endpoint_under_40(self_made):
    return miliardari_service.elenco_miliardari_u40_self_made(self_made)


# endpoint elenco miliardari per codice_fascia_eta (0,1,2)
# localhost:5000/miliardari/<int:codice_fascia_eta>
@app.get("/miliardari/<int:codice_fascia_eta>")
def endpoint_fascia_eta(codice_fascia_eta):
    return miliardari_service.elenco_miliardari_fascia_eta(codice_fascia_eta)


# endpoint registrazione
# localhost:5000/miliardari/registrazione
@app.post("/miliardari/registrazione")
def endpoint_registrazione_miliardario():
    corpo_richiesta = request.json
    return miliardari_service.aggiungere_miliardario(corpo_richiesta)


# endpoint delete miliardario
# localhost:5000/miliardari/elimina/2641
@app.delete("/miliardari/elimina/<int:id>")
def endpoint_elimina_miliardario(id):
    return miliardari_service.eliminare_miliardario(id)



# blocco condizionale di eseguibilità
if __name__ == "__main__":
    app.run()