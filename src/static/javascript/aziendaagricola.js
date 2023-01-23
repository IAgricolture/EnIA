var add = document.getElementById("add")
var wrapper = document.getElementById("wrapper")
var scelta = document.getElementById("scelta")
var codice = document.getElementById("codice")

function Aggiungi()
{
    wrapper.style.display = "none"
    codice.style.display = "none"
    add.style.display = "block"
    scelta.style.display = "block"
}

function Add(id)
{
    var ruolo = document.getElementById("ruolo").value
    
    var data = new FormData()
    data.append("ruolo", ruolo)
    data.append("datore", id)

    let response = fetch("GenCode",
          {
            "method": "POST",
            "headers": {},
            "body":data
          }).then(res=>res.json())
          .then(data=>{
            console.log("dentro")
              scelta.style.display = "none"
              codice.style.display = "block"
              var gen = document.getElementById("gencode")
              gen.innerHTML = data
          })
}

function Chiudi()
{
    window.location.href = "/AziendaAgricola"
}

  function rimandaelimina(dipendenteid)
  {
    console.log(dipendenteid)
    var data = {
      "id": dipendenteid
    }
    fetch("/removeFromAzienda", 
    {
      "method": "POST",
      headers: {
        'Content-Type': 'application/json'
      },
      "body": JSON.stringify(data)
    }).then(res=>res.json())
    .then(data=>{
        console.log(data)
        if(data["result"] == "True")
        {
          creaNotifica("Utente rimosso correttamente!", "successo", document.getElementById("spazioNotifica"), "notificamodifica")
          document.getElementById(dipendenteid).style.display = "none"
        }
        else
        {
          creaNotifica("Si è verificato un errore durante la rimozione dell'utente.", "fallimento", document.getElementById("spazioNotifica"), "notificamodifica")
        }
    })
  }