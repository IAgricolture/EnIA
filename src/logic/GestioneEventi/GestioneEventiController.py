from src import login_manager

from src.logic.Autenticazione.AutenticazioneService import AutenticazioneService

from flask import jsonify, request, render_template, redirect, url_for
from src import app
from src.logic.GestioneEventi.GestioneEventiService import GestioneEventiService

class GestioneEventiController():
    '''
    Classe Controller di Eventi

    ...

    Attributi
    ----------
    None

    Metodi
    -------
    visualizzaEventi():
        Carica dal DataBase tutti gli eventi associati ad quel terreno 
    cancellaEvento():
        Cancella un singolo evento associati ad quel terreno
    cancellaTuttiEventi():
        Cancella tutti gli eventi associati ad quel terreno

    '''
    
    @app.route('/eventi', methods=['GET', 'POST'])
    def visualizzaEventi():
        '''Carica dal DataBase tutti gli eventi associati ad quel terreno'''
        #get idTerreno
        #get json request
        idTerreno = request.json['id_terreno']
        
        #get lista eventi
        eventiTrovati = GestioneEventiService.visualizzaEventiByTerreno(idTerreno)
        
        return jsonify(eventiTrovati)
    
    @app.route('/cancellaTuttiEventi', methods=['GET', 'POST'])
    def cancellaTuttiEventi():
        '''Cancella un singolo evento associati ad quel terreno'''
        #get idTerreno
        #get json request
        idTerreno = request.json['id_terreno']
        
        #cancella tutti gli eventi
        GestioneEventiService.cancellaTuttiEventiByTerreno(idTerreno)
        
        return jsonify("ok")
    
    @app.route("/eliminaEvento", methods=['GET', 'POST'])
    def eliminaEvento():
        ''' Cancella tutti gli eventi associati ad quel terreno'''
        #get json request
        idEvento = request.json['id_evento']
        #cancella evento
        GestioneEventiService.cancellaEvento(idEvento)
        return jsonify("ok")