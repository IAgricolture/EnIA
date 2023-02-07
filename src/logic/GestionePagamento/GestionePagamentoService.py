from src.logic.Storage.MetodoDiPagamentoDAO import MetodoDiPagamentoDAO
from src.logic.model.MetodoDiPagamento import MetodoDiPagamento

class GestionePagamentoService():
    def creaMetodoDiPagamento(numerocarta, titolare, scadenza, cvv, id)->MetodoDiPagamento:
        m = MetodoDiPagamento("", numerocarta, titolare, scadenza, cvv, id)
        return MetodoDiPagamentoDAO.creaMetodo(m)
    
    def modificaMetodo(mp: MetodoDiPagamento, num_carta:str, titolare:str, scadenza:str, cvv:str):
        mp.num_carta = num_carta
        mp.titolare = titolare
        mp.scadenza = scadenza
        mp.cvv = cvv
        return MetodoDiPagamentoDAO.modificaMetodo(mp)