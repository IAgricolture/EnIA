AmbienteAgricoloController
============================

.. autoflask:: app:app
    :undoc-static:
    :include-empty-docstring:
    :endpoints: aggiungiTerreno, cercaModificata, elimina, dettagli, getStoricoInquinamento, downloadStoricoInquinamento, aggiungiIrrigatore, getIrrigatore, modificaIrrigatore, visualizzaIrrigatori, eliminaIrrigatore, attivaDisattivaIrrigatore, visualizzaTerreni, visualizzaPredizioneIrrigazione

AutenticazioneController
============================

.. autoflask:: app:app
    :undoc-static:
    :include-empty-docstring:
    :endpoints: login, logout

GestioneEventiController
============================

.. autoflask:: app:app
    :undoc-static:
    :include-empty-docstring:
    :endpoints: visualizzaEventi, cancellaTuttiEventi, eliminaEvento

GestioneScheduleController
============================

.. autoflask:: app:app
    :undoc-static:
    :include-empty-docstring:
    :endpoints: restituisciSchedule, modificaLivelloSchedule, usaScheduleConsigliato

RegistrazioneScheduleController
============================

.. autoflask:: app:app
    :undoc-static:
    :include-empty-docstring:
    :endpoints: registrazioneConCodiceDiAccesso, registrazioneFarmer

GestioneUtenteController
============================

.. autoflask:: app:app
    :undoc-static:
    :include-empty-docstring:
    :endpoints: user, aziendaagricola, removeFromAzienda, GenCode