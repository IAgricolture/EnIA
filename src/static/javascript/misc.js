function creaNotifica(messaggio, tipo, parent, name) 
  /* 
  DOCUMENTAZIONE: Funzione riutilizzabile per la creazione di una notifica in stile CelestialUI.
  Argomenti sono:
  Messaggio, che è una string contenente il testo della notifica
  Tipo, che in caso di notifica per un evento positivo sarà "successo", altri tipi sono aggiungibili nell'if
  Parent, che è l'elemento html ottenuto da document.getElement sotto cui verrà inserita la notifica. 
  Name, è il name che verrà impostato per gli elementi di notifica.
  */
  {
    var div = document.createElement('div')
    div.setAttribute("name", name)
    var testo = document.createElement('strong')
    testo.innerHTML = messaggio
    if(tipo == "successo")
    {
      div.className = "alert alert-success"
    } 
    else 
    {
      div.className = "alert alert-danger"
    }
    //Controlla che non esista già la notifica
    var notifiche = document.getElementsByName(name)
    if(notifiche.length > 0)
    {
      while(notifiche.length > 0){
        notifiche[0].parentNode.removeChild(notifiche[0])
        }
    }
    div.appendChild(testo) 
    parent.appendChild(div)
  }