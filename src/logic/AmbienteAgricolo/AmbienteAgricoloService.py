from src.logic.Adapters.NominatimAdapter import NominatimAdapter
from src.logic.Adapters.OpenMeteoAdapter import OpenMeteoAdapter
from src.logic.Adapters.SenseSquareAdapter import SenseSquareAdapter
from src.logic.DecisionIntelligence.DecisionIntelligenceService import DecisionIntelligenceService
from src.logic.GestioneEventi.GestioneEventiService import GestioneEventiService
from src.logic.Storage.ImpiantoDiIrrigazioneDAO import ImpiantoDiIrrigazioneDAO
from src.logic.Storage.EventoDAO import EventoDAO
from src.logic.model.Evento import Evento
from src.logic.model.ImpiantoDiIrrigazione import ImpiantoDiIrrigazione
from src.logic.model.Terreno import Terreno
from src.logic.Storage.TerrenoDAO import TerrenoDAO
import requests
import json
import re
from datetime import datetime

# TODO: ERROR HANDLING DAO TERRENO


class AmbienteAgricoloService():
    '''
    Classe Service di Ambiente Agricolo

    ...

    Attributi
    ----------
    ColturaEng : str[]
        Contiene i nomi di tutte le colture disponibili in inglese
    Colture : str[]
        Contine i nomi di tutte le colture
    StadiCrescita : str[]
        Contiene tutti gli stati di crescita delle colture

    Metodi
    -------
    isValidTerreno(terreno: Terreno) :
        Controlla se un terreno è valido
    validateTerreno(terreno: Terreno) :
        Controlla se tutti gli attributi di terreno sono validi
    visualizzaTerreni(farmer: str) :
        Restiruisce una lista dei terreni di cui un utente farmer è proprietario
    aggiungiTerreno(nome: str, coltura: str, stadio_crescita: str, posizione, preferito: bool, priorita: int, proprietario: str) :
        Aggiunge un terreno al database
    trovaTerreno(id: str) :
        Restiruisce un terreno in base all'id
    modificaTerreno(id: str, nome: str, coltura: str, stadio_crescita: str, posizione, preferito: bool, priorita: int, proprietario: str) :
            Modifica i dati di un terreno
    eliminaTerreno(id: str) :
        Elimina un terreno
    cercaPosizione(id: str) :
        Cerca la posizione di un terreno
    cercaInquinamento(provincia: str, regione: str, nazione: str, comune: str) :
        Cerca i dati relativi all'inquinamento di una specifica zone
    cercaStoricoInquinamento(dataInizio: str, dataFine: str, comune: str, regione: str, nazione: str, provincia: str, formato: str) :
        Cerca i dati relativi all'inquinamento di una specifica zone in uno specifico range temporale
    aggiungiIrrigatore(id_terreno: str, nome_irrigatore: str, posizione_irrigatore: str) :
        Aggiunge un irrigatore ad un terreno e crea un evento della sua creazione
    modificaIrrigatore(idIrrigatore: str, nomeIrrigatore: str, posizioneIrrigatore: str) :
        Modifica dei dati di un irrigatore
    getIrrigatore(idIrrigatore: str) :
        Restituisce un irrigatore in base all'id
    visualizzaListaIrrigatori(idTerreno: str) :
        Restituisce la lista degli irrigatori presenti su un terreno
    eliminaIrrigatore(idIrrigatore: str) :
        Elimina un irrigatore
    attivaDisattivaIrrigatore(idIrrigatore: str) :
        Attiva o disattiva un irrigatore
    visualizzaListaEventi(idTerreno: str) :
        Restituisce la lista degli eventi su un terreno
    cercalat(id: str) :
        Recupera la latitudine di un terreno
    cercalon(id: str) :
        Recupera la longitudine di un terreno
    cercaMeteo(lat: float, lon: float) :
        Recupera i dati meteo di una zona e crea un evento in caso la pioggia superi un certa soglia
    restituisciPredizioneLivelliIrrigazione(lon: float, lat: float, crop: str, stage: str) :
        Recupera la predizione dei livelli di irrigazione forniti dal modulo AI
    '''

    ColturaEng = ["Barley", "Bean", "Cabbage", "Carrot", "Cotton",
                  "Cucumber", "Eggplant", "Grain", "Lentil", "Lettuce"]
    Colture = ["Orzo", "Fagiolo", "Cavolo", "Carota", "Cotone",
               "Cetriolo", "Melanzana", "Grano", "Lenticchia", "Lattuga"]
    StadiCrescita = ["Iniziale", "Sviluppo", "Metà Stagione", "Fine Stagione"]

    def isValidTerreno(terreno: Terreno) -> bool:
        '''
        Controlla se un terreno è valido

        Parametri
        ----------
        terreno : Terreno
            Terreno da validare

        Returns
        -------
        risultato["esitoControllo"] : bool
            Esito del controllo
        '''
        risultato = AmbienteAgricoloService.validateTerreno(terreno)
        return risultato["esitoControllo"]

    def validateTerreno(terreno: Terreno):
        '''
        Controlla se tutti gli attributi di terreno sono validi

        Parametri
        ----------
        terreno : Terreno
            Terreno da validare

        Returns
        -------
        risultato : dict
            Esito del controllo
        '''

        risultato = {
            "nomeNonValido": False,
            "colturaNonValida": False,
            "posizioneNonValida": False,
            "preferitoNonValido": False,
            "prioritaNonValida": False,
            "proprietarioNonValido": False,
            "stadio_crescitaNonValido": False,
            "esitoControllo": False
        }
        regexNome = re.compile(r"[a-zA-z0-9_]+[\w\s\W]*$")
        regexPriorita = re.compile(r"^[0-9]")
        if (not re.match(regexNome, terreno.nome)):
            risultato["nomeNonValido"] = True
        if (terreno.coltura not in AmbienteAgricoloService.Colture):
            risultato["colturaNonValida"] = True
        posizione = terreno.posizione
        try:  # Se non esiste uno dei campi richiesti, la posizione è invalida.
            if (posizione["type"] != "Feature"):  # Una sola posizione
                risultato["posizioneNonValida"] = True
            if (posizione["properties"]):  # Non ha proprietà aggiuntive
                risultato["posizioneNonValida"] = True
            geometria = posizione["geometry"]
            if (geometria["type"] != "Polygon"):
                risultato["posizioneNonValida"] = True
            # Ha un array di coordinate
            if (len(geometria["coordinates"][0]) < 2 or len(
                    geometria["coordinates"][0][0]) != 2):
                risultato["posizioneNonValida"] = True
        except KeyError:
            risultato["posizioneNonValida"] = True
        if (terreno.preferito is not True and terreno.preferito is not False):
            risultato["preferitoNonValido"] = True
        if (not re.match(regexPriorita, str(terreno.priorita))):
            risultato["prioritaNonValida"] = True
        if (terreno.stadio_crescita not in AmbienteAgricoloService.StadiCrescita):
            risultato["stadio_crescitaNonValido"] = True
        if not (risultato["nomeNonValido"] or risultato["colturaNonValida"] or risultato["posizioneNonValida"] or risultato["preferitoNonValido"] or
                risultato["prioritaNonValida"] or risultato["proprietarioNonValido"] or risultato["stadio_crescitaNonValido"]):
            risultato["esitoControllo"] = True
        return risultato

    def visualizzaTerreni(farmer: str):
        '''
        Restiruisce una lista dei terreni di cui un utente farmer è proprietario

        Parametri
        ----------
        farmer : str
            ID di un utente farmer

        Returns
        -------
        Terreni : list
            lista dei terrenmi di cui l'utente farmer è proprietario
        '''
        Terreni = TerrenoDAO.restituisciTerreniByFarmer(farmer)
        return Terreni

    def aggiungiTerreno(nome: str, coltura: str, stadio_crescita: str,
                        posizione, preferito: bool, priorita: int, proprietario: str) -> bool:
        '''
        Aggiunge un terreno al database

        Parametri
        ----------
        nome : str
            nome del terreno
        coltura : str
            tipo di coltura che crescerà sul terreno
        stadio_crescita : str
            stato di crescita di una coltura
        posizione : str
            geojson contenente i confini del terreno
        preferito : bool
            se il terreno è preferito o meno
        priorita : int
            priorità del terreno
        proprietario : str
            id dell'utente farmer che è il proprietario

        Returns
        -------
        Terreno : bool
            Esito dell'operazione di aggiunta
        '''
        id = None
        terreno = Terreno(id, nome, coltura, stadio_crescita,
                          posizione, preferito, priorita, proprietario)
        risultato = AmbienteAgricoloService.validateTerreno(terreno)
        if (risultato["esitoControllo"]):
            resultDB = TerrenoDAO.InserisciTerreno(terreno)
            risultato["esitoOperazione"] = True
            risultato["restituito"] = resultDB
        else:
            risultato["esitoOperazione"] = False
            risultato["restituito"] = None
        return risultato

    def trovaTerreno(id: str) -> Terreno:
        '''
        Restiruisce un terreno in base all'id

        Parametri
        ----------
        id : str
            ID del terreno

        Returns
        -------
        Terreno : Terreno
            Terreno trovato sul DB
        '''
        Terreno = TerrenoDAO.TrovaTerreno(id)
        return Terreno

    def modificaTerreno(id: str, nome: str, coltura: str, stadio_crescita: str,
                        posizione, preferito: bool, priorita: int, proprietario: str) -> bool:
        '''
        Modifica i dati di un terreno

        Parametri
        ----------
        id : str
            ID del terreno
        nome : str
            nome del terreno
        coltura : str
            tipo di coltura che crescerà sul terreno
        stadio_crescita : str
            stato di crescita di una coltura
        posizione : str
            geojson contenente i confini del terreno
        preferito : bool
            se il terreno è preferito o meno
        priorita : int
            priorità del terreno
        proprietario : str
            id dell'utente farmer che è il proprietario

        Returns
        -------
        result.matched_count > 0 : bool
            Esito dell'operazione di modifica
        '''
        terreno = Terreno(id, nome, coltura, stadio_crescita,
                          posizione, preferito, priorita, proprietario)
        result = TerrenoDAO.modificaTerreno(terreno)
        # Restituisce True se andato bene, False altrimenti.
        return result.matched_count > 0

    def eliminaTerreno(id: str) -> bool:
        '''
        Elimina un terreno

        Parametri
        ----------
        id : str
            ID di un terreno

        Returns
        -------
        False : bool
            Non è stato possibile rimuovere il terreno dal DB
        True : bool
            Rimozione avvenuta con successo
        '''
        terreno = TerrenoDAO.TrovaTerreno(id)
        if (terreno is None):
            return False
        else:
            TerrenoDAO.RimuoviTerreno(terreno)
            return True

    def cercaPosizione(id: str):
        '''
        Cerca la posizione di un terreno

        Parametri
        ----------
        id : str
            ID di un terreno

        Returns
        -------
        None
            Posizione non trovata
        datiapi : str
            Json contenente la posizione del terreno
        '''
        terreno = TerrenoDAO.TrovaTerreno(id)
        if (terreno is None):
            return None
        else:
            # Estraggo latitudine e longitudine del primo punto del terreno, di
            # cui prendo la posizione
            lat = terreno.posizione["geometry"]["coordinates"][0][0][1]
            lon = terreno.posizione["geometry"]["coordinates"][0][0][0]
            print(lat)
            print(lon)
            nominatim = NominatimAdapter(lat, lon, "json", 10)
            datiapi = nominatim.get_data()
            print(datiapi)
            return datiapi  # JSON

    def cercaInquinamento(provincia: str, regione: str,
                          nazione: str, comune: str):
        '''
        Cerca i dati relativi all'inquinamento di una specifica zone

        Parametri
        ----------
        provincia : str
            Provincia
        regione : str
            Regione
        nazione : str
            Nazione
        comune : str
            Comune

        Returns
        -------
        datiapi : str
            Json contenente i dati relativi all'inquinamento
        '''
        adapter = SenseSquareAdapter(nazione, regione, provincia, comune)
        datiapi = adapter.get_data_for_today()
        return datiapi

    def cercaStoricoInquinamento(dataInizio: str, dataFine: str, comune: str,
                                 regione: str, nazione: str, provincia: str, formato: str):
        '''
        Cerca i dati relativi all'inquinamento di una specifica zone in uno specifico range temporale

        Parametri
        ----------
        dataInizio : str
            Data inizio della ricerca
        dataFine : str
            Data fine della ricerca
        provincia : str
            Provincia
        regione : str
            Regione
        nazione : str
            Nazione
        comune : str
            Comune

        Returns
        -------
        datiapi : str
            Json contenente i dati relativi all'inquinamento
        '''
        adapter = SenseSquareAdapter(
            nazione, regione, provincia, comune, start_date=dataInizio, end_date=dataFine, formato=formato)
        datiapi = adapter.get_data_time_interval()
        return datiapi

    def aggiungiIrrigatore(id_terreno: str, nome_irrigatore: str,
                           posizione_irrigatore: str) -> str:
        '''
        Aggiunge un irrigatore ad un terreno e crea un evento della sua creazione

        Parametri
        ----------
        id_terreno : str
            id del terreno
        nome_irrigatore : str
            nome da assegnare all'irrigatore
        posizione_irrigatore : str
            json contenente la posizione dell'irrigatore

        Returns
        -------
        id : str
            id dell'irriogatore inserito
        '''
        impianto = ImpiantoDiIrrigazione(
            "", nome_irrigatore, "irrigatore", "", posizione_irrigatore, False)
        id = ImpiantoDiIrrigazioneDAO.creaImpianto(impianto, id_terreno)
        evento = Evento("", "Creazione Irrigatore", "L'irrigatore :" + nome_irrigatore +
                        " è stato creato", datetime.now(), "INFO", False, False, id_terreno)
        GestioneEventiService.creaEvento(evento)
        return id

    def modificaIrrigatore(
            idIrrigatore: str, nomeIrrigatore: str, posizioneIrrigatore: str):
        '''
        Modifica dei dati di un irrigatore

        Parametri
        ----------
        idIrrigatore : str
            Id dell'irrigatore da modificare
        nomeIrrigatore : str
            nome dell'irrigatore
        posizioneIrrigatore : str
            Json contenente la posizione dell'irrigatore

        Returns
        -------
        datiapi : str
            Json contenente i dati relativi all'inquinamento
        '''
        impianto = ImpiantoDiIrrigazione(
            idIrrigatore, nomeIrrigatore, "irrigatore", "", posizioneIrrigatore, False)
        ImpiantoDiIrrigazioneDAO.modificaImpianto(impianto)
        return True

    def getIrrigatore(idIrrigatore: str):
        '''
        Restituisce un irrigatore in base all'id

        Parametri
        ----------
        idIrrigatore : str
            Id dell'irrigatore da recuperare

        Returns
        -------
        ImpiantoDiIrrigazioneDAO.findImpiantoById(idIrrigatore) : ImpiantoDiIrrigazione
            Irrigatore recuperato dal DB
        '''
        return ImpiantoDiIrrigazioneDAO.findImpiantoById(idIrrigatore)

    def visualizzaListaIrrigatori(idTerreno: str):
        '''
        Restituisce la lista degli irrigatori presenti su un terreno

        Parametri
        ----------
        idTerreno : str
            Id del terreno su cui sono presenti gli irrigatori

        Returns
        -------
        ImpiantoDiIrrigazioneDAO.findImpiantiByTerreno(idTerreno) : list
           Lista degli irrigatori presenti su un terreno
        '''
        return ImpiantoDiIrrigazioneDAO.findImpiantiByTerreno(idTerreno)

    def eliminaIrrigatore(idIrrigatore: str):
        '''
        Elimina un irrigatore

        Parametri
        ----------
        idIrrigatore : str
            Id dell'irrigatore da eliminare

        Returns
        -------
        None
        '''
        ImpiantoDiIrrigazioneDAO.eliminaImpianto(idIrrigatore)

    def attivaDisattivaIrrigatore(idIrrigatore: str):
        '''
        Attiva o disattiva un irrigatore

        Parametri
        ----------
        idIrrigatore : str
            Id dell'irrigatore

        Returns
        -------
        False : bool
            Impianto disattivato
        True : bool
            Impianto attivato
        '''
        if (ImpiantoDiIrrigazioneDAO.findImpiantoById(
                idIrrigatore).attivo is True):
            ImpiantoDiIrrigazioneDAO.disattivaImpianto(idIrrigatore)
            return False
        else:
            ImpiantoDiIrrigazioneDAO.attivaImpianto(idIrrigatore)
            return True

    def visualizzaListaEventi(idTerreno: str):
        '''
        Restituisce la lista degli eventi su un terreno

        Parametri
        ----------
        idTerreno : str
            Id del terreno

        Returns
        -------
        EventoDAO.findEventiByTerreno(idTerreno) : list
            Lista degli eventi di un terreno
        '''
        return EventoDAO.findEventiByTerreno(idTerreno)

    def cercalat(id: str):
        '''
        Recupera la latitudine di un terreno

        Parametri
        ----------
        id : str
            Id del terreno

        Returns
        -------
        None
            Latitudine non trovata
        lat : float
            Latitudine del terreno
        '''
        terreno = TerrenoDAO.TrovaTerreno(id)
        if (terreno is None):
            return None
        else:
            # Estraggo latitudine e longitudine del primo punto del terreno, di
            # cui prendo la posizione
            lat = terreno.posizione["geometry"]["coordinates"][0][0][1]
            return lat

    def cercalon(id: str):
        '''
        Recupera la longitudine di un terreno

        Parametri
        ----------
        id : str
            Id del terreno

        Returns
        -------
        None
            Longitudine non trovata
        lon : float
            Longitudine del terreno
        '''
        terreno = TerrenoDAO.TrovaTerreno(id)
        if (terreno is None):
            return None
        else:
            # Estraggo latitudine e longitudine del primo punto del terreno, di
            # cui prendo la posizione
            lon = terreno.posizione["geometry"]["coordinates"][0][0][0]
            return lon

    def cercaMeteo(lat: float, lon: float):
        '''
        Recupera i dati meteo di una zona e crea un evento in caso la pioggia superi un certa soglia

        Parametri
        ----------
        lat : float
            Latitudine
        lon : float
            Longitudine

        Returns
        -------
        data
            Dati meteo della zona
        '''
        # creo l'oggetto meteo
        meteo = OpenMeteoAdapter(lat, lon)
        data = meteo.get_data()

        # fai la somma delle precipitazioni per le prossime 24 ore
        somma = 0
        for i in range(0, 24):
            somma += data["hourly"]["precipitation"][i]

        if somma > 10:
            u = Evento("", "Pioggia", "Ci saranno ingenti quantità di pioggia nelle prossime 24 ore",
                       datetime.now(), "Pioggia", False, False, "")
            GestioneEventiService.creaEvento(u)

        return data

    def restituisciPredizioneLivelliIrrigazione(
            lon: float, lat: float, crop: str, stage: str):
        '''
        Recupera la predizione dei livelli di irrigazione forniti dal modulo AI

        Parametri
        ----------
        lon : float
            Longitudine
        lat : float
            Latitudine
        crop : str
            Coltura
        stage: str
            Stato di crescita

        Returns
        -------
        DecisionIntelligenceService.getPredizioneLivelliIrrigazione(lon, lat, crop, stage) : dict
            Predizione dei livelli di irrigazione forniti dal modulo AI
        '''
        return DecisionIntelligenceService.getPredizioneLivelliIrrigazione(
            lon, lat, crop, stage)
