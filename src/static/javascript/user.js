var view = document.querySelector("#view")
var usermod = document.querySelector("#usermod")
var licenzamod = document.querySelector("#licenzamod")
var metodomod = document.querySelector("#metodomod")


function ModUser() {
    view.style.display = "none"
    usermod.style.display = "flex"
    licenzamod.style.display = "none"
    metodomod.style.display = "none"
}

function ModLicenza() {
    view.style.display = "none"
    usermod.style.display = "none"
    licenzamod.style.display = "flex"
    metodomod.style.display = "none"
}

function ModMetodo() {
    view.style.display = "none"
    usermod.style.display = "none"
    licenzamod.style.display = "none"
    metodomod.style.display = "flex"
}

function Visualizza()
{
    window.location.href = "/AziendaAgricola"
}

function Annulla() {
    view.style.display = "flex"
    usermod.style.display = "none"
    licenzamod.style.display = "none"
    metodomod.style.display = "none"
}

function CheckUser() {
    var nome = document.getElementById("nome").value
    var cognome = document.getElementById("cognome").value
    var email = document.getElementById("email").value
    var password = document.getElementById("password").value
    var confermaPassword = document.getElementById("confermaPassword").value
    var indirizzo = document.getElementById("indirizzo").value
    var dataNascita = document.getElementById("dataNascita").value
    var partitaiva = document.getElementById("partitaiva").value
    var ruolo = document.getElementById("ruolo").value

    var nomeerr = document.getElementById("nomeerr")
    var cognomeerr = document.getElementById("cognomeerr")
    var emailerr = document.getElementById("emailerr")
    var passworderr = document.getElementById("passerr")
    var confermaerr = document.getElementById("conferr")
    var indirizzoerr = document.getElementById("indirizzoerr")
    var dataNascitaerr = document.getElementById("dataerr")
    var partitaivaerr = document.getElementById("partitaivaerr")

    const nomereg = /^[a-z ]{2,30}$/i
    const mailreg = /[A-Z0-9._%+-]+@[A-Z0-9-]+.+.[A-Z]{2,4}/i
    const passreg = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&_])[A-Za-z\d$@$!%*?&_]{8,20}$/
    const indireg = /^[A-Za-zÀ-ù0-9 ,‘-]+$/

    nomeerr.innerHTML = ""
    cognomeerr.innerHTML = ""
    emailerr.innerHTML = ""
    passworderr.innerHTML = ""
    confermaerr.innerHTML = ""
    indirizzoerr.innerHTML = ""
    dataNascitaerr.innerHTML = ""
    partitaivaerr.innerHTML = ""

    var mod = true

    if (!nomereg.test(nome)) {
        if (nome == "")
            nomeerr.innerHTML = "Campo Richiesto"
        else
            nomeerr.innerHTML = "Formato non valido"
        mod = false
    }

    if (!nomereg.test(cognome)) {
        if (cognome == "")
            cognomeerr.innerHTML = "Campo Richiesto"
        else
            cognomeerr.innerHTML = "Formato non valido"
        mod = false
    }

    if (!mailreg.test(email)) {
        if (email == "")
            emailerr.innerHTML = "Campo Richiesto"
        else
            emailerr.innerHTML = "Formato non valido"
        mod = false
    }


    if (password != "") {
        if (!passreg.test(password)) {
            passworderr.innerHTML = "Formato non valido"
            mod = false
        }

        if (password != confermaPassword) {
            confermaerr.innerHTML = "Le due password non corrispondono"
            mod = false
        }

    }

    if (!indireg.test(indirizzo)) {
        if (indirizzo == "")
            indirizzoerr.innerHTML = "Campo Richiesto"
        else
            indirizzoerr.innerHTML = "Formato non valido"
        mod = false
    }

    if (dataNascita == "") {
        dataNascitaerr.innerHTML = "Campo Richiesto"
        mod = false
    }

    if (ruolo == "farmer")
        if (partitaiva == "") {
            partitaivaerr.innerHTML = "Campo Richiesto"
            mod = false
        }

    if (mod) {
        var form = document.querySelector("#userform")
        form.submit();
    }
}

function CheckMetodo() {
    var numerocarta = document.getElementById("num_carta").value
    var titolare = document.getElementById("titolare").value
    var scadenza = document.getElementById("scadenza").value
    var cvv = document.getElementById("cvv").value

    var numerocartaerr = document.getElementById("numerocartaerr")
    var titolareerr = document.getElementById("titolareerr")
    var scadenzaerr = document.getElementById("scadenzaerr")
    var cvverr = document.getElementById("cvverr")

    const cartareg = /^(?:4[0-9]{12}(?:[0-9]{3})?|[25][1-7][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\d{3})\d{11})$/
    const titolarereg = /^[a-z ]{4,64}$/i
    const scadenzareg = /^(0[1-9]|1[0-2])\/?([0-9]{4}|[0-9]{2})$/
    const cvvreg = /^[0-9]{3,4}$/

    var mod = true

    numerocartaerr.innerHTML = ""
    titolareerr.innerHTML = ""
    scadenzaerr.innerHTML = ""
    cvverr.innerHTML = ""

    if (!cartareg.test(numerocarta)) {
        if (numerocarta == "")
            numerocartaerr.innerHTML = "Campo Richiesto"
        else
            numerocartaerr.innerHTML = "Formato non valido"
        mod = false
    }

    if (!titolarereg.test(titolare)) {
        if (titolare == "")
            titolareerr.innerHTML = "Campo Richiesto"
        else
            titolareerr.innerHTML = "Formato non valido"
        mod = false
    }

    if (!scadenzareg.test(scadenza)) {
        if (scadenza == "")
            scadenzaerr.innerHTML = "Campo Richiesto"
        else
            scadenzaerr.innerHTML = "Formato non valido"
        mod = false
    }

    if (!cvvreg.test(cvv)) {
        if (cvv == "")
            cvverr.innerHTML = "Campo Richiesto"
        else
            cvverr.innerHTML = "Formato non valido"
        mod = false
    }

    if (mod) {
        var form = document.querySelector("#metodoform")
        form.submit();
    }
}