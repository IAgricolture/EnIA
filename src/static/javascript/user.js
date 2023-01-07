var view = document.querySelector("#view")
var nome = document.querySelector("#nome")
var cognome = document.querySelector("#cognome")
var email = document.querySelector("#email")
var ruolo = document.querySelector("#ruolo")
var nascita = document.querySelector("#nascita")
var indirizzo = document.querySelector("#indirizzo")
var userview = document.querySelector("#userview")
var codice = document.querySelector("#codice")
var farmerview = document.querySelector("#farmerview")
var partitaiva = document.querySelector("#partitaiva")
var licenza = document.querySelector("#licenza")
var metodo = document.querySelector("#metodo")

function load(user)
{
    let s = user
    s = s.replaceAll("&#34;", "\"")
    var u = JSON.parse(s)
    nome.append(u["nome"])
    cognome.append(u["cognome"])
    email.append(u["email"])
    ruolo.append(u["ruolo"])
    nascita.append(u["dataNascita"])   
    indirizzo.append(u["indirizzo"])
   
    if (u["ruolo"] == "farmer")
    {
        farmerview.style.display = "flex"
        partitaiva.append(u["partitaIVA"])
    }
    else
    {
        userview.style.display = "flex"
        codice.append(u["codice"])
    }
}