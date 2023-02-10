from src.dbConnection import terreni
from src.logic.model.Terreno import Terreno
from flask import jsonify
import datetime
from bson.objectid import ObjectId


class TerrenoDAO():
    
    '''
    Classe DAO di Terreno

    ...

    Attributi
    ----------
    None

    Metodi
    -------
    InserisciTerreno(terreno: Terreno):
        Questo metodo ci permette di istanziare un nuovo terreno su DataBase
    TrovaTerreno(id: str):
        Questo metodo ci permette di recuperare dal DataBase un terreno con id 
        corrispondenete a quello passarto in input
    RimuoviTerreno(terreno: Terreno):        
        Questo metodo ci permette di elimare dal DataBase il terreno passato in input
    modificaTerreno(terrenoMod: Terreno):
        Il metodo ci permette di modificare un'istanza del terreno presente nel database
    restituisciTerreniByFarmer(farmer: str):
        Questo metodo ci restiuisce una lista di terreni associati ad un faremer passato come input

    '''

    def InserisciTerreno(terreno: Terreno) -> str:
        '''
        Questo metodo ci permette di istanziare un nuovo terreno su DataBase

        Parametri
        ----------
        terreno: Terreno
            Terreno da inserire nel DataBase

        Returns
        -------
        result : str
            Restituisce l'id del terreno appena inserito
        '''
        
        result = terreni.insert_one({
            "Nome": terreno.nome,
            "Coltura": terreno.coltura,
            "Posizione": terreno.posizione,
            "Preferito": terreno.preferito,
            "Priorita": terreno.priorita,
            "proprietario": terreno.proprietario,
            "stadio_crescita": terreno.stadio_crescita
        })

        return str(result.inserted_id)

    def TrovaTerreno(id: str) -> Terreno:
        '''
        Questo metodo ci permette di recuperare dal DataBase un terreno con id 
        corrispondenete a quello passarto in input

        Parametri
        ----------
        id : str
            id del terrebi da Trovare

        Returns
        -------
        NewTerreno : Terreno
            Restituisce il terreno trovato
        None : Nonetype
            Restituisce None in caso non e stato trovato nessun terreno con id passato
        '''
        
        trovato = terreni.find_one({"_id": ObjectId(id)})
        if (trovato is None):
            return None
        id2 = str(trovato.get("_id"))
        nome = str(trovato.get("Nome"))
        coltura = str(trovato.get("Coltura"))
        posizione = trovato.get("Posizione")
        preferito = (trovato.get("Preferito"))
        priorita = int(trovato.get("Priorita"))
        proprietario = str(trovato.get("proprietario"))
        stadio_crescita = str(trovato.get("stadio_crescita"))
        NewTerreno = Terreno(
            id2,
            nome,
            coltura,
            stadio_crescita,
            posizione,
            preferito,
            priorita,
            proprietario)
        return NewTerreno

    def RimuoviTerreno(terreno: Terreno) -> bool:
        '''
        Questo metodo ci permette di elimare dal DataBase il terreno passato in input

        Parametri
        ----------
        terreno: Terreno
            Terreno da eliminare

        Returns
        -------
        True : bool
            Valore restituito in caso di corretta eliminazione
        False : bool
            Valore restituito in caso di NON eliminazione
        '''
        
        trovato = terreni.delete_one({"_id": ObjectId(terreno.id)})
        if trovato.deleted_count == 1:
            return True
        else:
            return False

    def modificaTerreno(terrenoMod: Terreno):
        '''
        Il metodo ci permette di modificare un'istanza del terreno presente nel database

        Parametri
        ----------
        terrenoMod: Terreno
            Terreno da modificare 

        Returns
        -------
        None : Nonetype
            Valore restituito nel caso in cui non e stato trovato il Terreno su cui 
            effettuare le modifiche
        terrenoMod : Terreno
            Restituisce il terreno modificatof
        '''
        
        trovato = TerrenoDAO.TrovaTerreno(str(terrenoMod.id))
        if (trovato is None):
            return None
        return terreni.update_one({"_id": ObjectId(trovato.id)},
                                  {"$set": {
                                      "Nome": terrenoMod.nome,
                                      "Coltura": terrenoMod.coltura,
                                      "Posizione": terrenoMod.posizione,
                                      "Preferito": terrenoMod.preferito,
                                      "Priorita": terrenoMod.priorita,
                                      "proprietario": terrenoMod.proprietario,
                                      "stadio_crescita": terrenoMod.stadio_crescita
                                  }})

    def restituisciTerreniByFarmer(farmer: str) -> list:
        '''
        Questo metodo ci restiuisce una lista di terreni associati ad un faremer passato come input

        Parametri
        ----------
        farmer: str
            faremr di cui si desidera avere la lista dei Terreno

        Returns
        -------
        ListaTerreni : Terreno
            Lista dei Terreni associato ad un farmer
        '''
        
        trovati = terreni.find({"proprietario": farmer})
        listaTerreni = []
        for trovato in trovati:
            id2 = str(trovato.get("_id"))
            nome = str(trovato.get("Nome"))
            coltura = str(trovato.get("Coltura"))
            posizione = trovato.get("Posizione")
            preferito = (trovato.get("Preferito"))
            priorita = int(trovato.get("Priorita"))
            proprietario = str(trovato.get("proprietario"))
            stadio_crescita = str(trovato.get("stadio_crescita"))
            NewTerreno = Terreno(
                id2,
                nome,
                coltura,
                stadio_crescita,
                posizione,
                preferito,
                priorita,
                proprietario)
            listaTerreni.append(NewTerreno)

        return listaTerreni
