    var validMap = true
    function insert(){

      if(!(validate()))
      {
      return //FORSE ESISTE UN ALTRO MODO?
      }
        var nome = document.getElementById("nome").value
        var coltura = document.getElementById("coltura").value
        var preferito = document.getElementById("preferito").checked
        var priorita = document.getElementById("priorita").value
        var stadio_crescita = document.getElementById("stadio").value
        
          var url = "aggiuntaTerreno"
          data = new FormData()
          console.log(polygon.toGeoJSON())
          data.append("nome", nome)
          data.append("coltura", coltura)
          data.append("preferito", preferito)
          data.append("priorita", priorita)
          geoJson = polygon.toGeoJSON()
          
          var data = {
                nome : nome,
                coltura : coltura,
                preferito : preferito,
                priorita : priorita,
                posizione : geoJson,
                stadio_crescita : stadio_crescita
          }
          console.log(JSON.stringify(data))
          console.log(data)

          let response = fetch("/aggiuntaTerreno",
          {
            "method": "POST",
            headers: {
              'Content-Type': 'application/json'
            },
            "body": JSON.stringify(data)
          }).then(res=>res.json())
          .then(data=>{
              console.log(data)
              if(data["TerrenoAggiunto"]){
                creaNotifica("Terreno aggiunto correttamente!", "successo", document.getElementById("form1"), "notificamodifica")
                setTimeout(redirect, 1000);
                } else {
                  creaNotifica("Si è verificato un errore durante l'aggiunta del terreno.", "fallimento", document.getElementById("form1"), "notificamodifica")
                }
          })        
    }

    function redirect() {
      window.location.href = "/visualizzaTerreni";
    }
    
    function validateMap()
    {
       if(!validMap)
       {
        creaNotifica("Errore: inserire almeno un punto sulla mappa, che rappresenti il terreno. Per inserire, bisogna fare clic sinistro.", "fallimento", document.getElementById("spazioNotifica"), "notificamappa")
       }
       return validMap
    }
    
    function validate() 
    /*Controlla che i dati siano stati correttamente inseriti nei form.
      Funzionamento: creo una Regexp, che viene poi modificata a seconda del form type. validAll indica 
      che tutti i campi sono corretti, validThisForm che quello considerato lo sia. 
      Per ogni form, controlla che non sia vuoto o incorretto: altrimenti, crea una notifica di errore, se
      non esiste già. Se invece il form è corretto e la notifica esiste, la rimuove.*/
    {
      var regexp = /[a-zA-z0-9_]+[\w\s\W]*$/  //Regex per testo alfanumerico, con o senza spazi, e prima lettera non è un simbolo
      var validAll = true
      var forms = [ document.getElementById('nome'), document.getElementById('coltura'), document.getElementById('priorita')]     
      forms.forEach(function(form){   //Per ogni form, controlla se ha testo al suo interno e se ha formato corretto con REGEXP.
        console.log("Controllo form" + form.id)
        var validThisForm = true
        var div = document.createElement('div')
        div.className = "alert alert-danger"
        var testo = document.createElement('strong')
        var notifiche = form.parentElement.getElementsByClassName("alert alert-danger")
        if(form.type == "number")   //Cambio regex per i numeri
        {
         var regexp = /^[0-9]/
        }else
        {
         var regexp = /[\w\s]+$/
        }

        if(!(form.value))
        {
          validThisForm = false
          testo.innerHTML="Errore: necessario compilare il campo."
        }
        else
        {
          if(!(regexp.test(form.value)))
          {
            validThisForm = false
            if(regexp == /[\w\s]+$/)
            {
              testo.innerHTML="Errore: il valore inserito non è corretto. Riprovare, usando solo caratteri alfanumerici, e non speciali."
            }
            else
            {
              testo.innerHTML="Errore: il valore inserito non è corretto. Riprovare, usando un unico numero."
            }
          }
        }
        if(!(validThisForm))
        {
          validAll = false
          div.appendChild(testo)
          if(!(notifiche.length > 0))
          {
            form.parentElement.appendChild(div)
          }
        }
        else
        {
          if(notifiche.length > 0)
          {
            while(notifiche.length > 0){
            notifiche[0].parentNode.removeChild(notifiche[0])
            }
          }
        }
        console.log("Risultato controllo, form è corretto: " + validThisForm)
      })
      console.log("Risultato controllo, form sono corretti: " + validAll)
      var validMap = validateMap()
      console.log("Risultato controllo, mappa è corretta: " + validMap)
      console.log("Risultato: " + validAll && validMap)
      return validAll && validMap
    }

    function resetMap()
    {
      
      window.polygon.remove()
      window.points = [];
      validMap = false
    }
