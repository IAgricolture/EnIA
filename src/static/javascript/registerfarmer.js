var avanti = document.querySelector("#avanti")
var dietro = document.querySelector("#dietro")
var divs = document.querySelectorAll(".form-group")
var div_counter = 1

function Avanti() {
  div_counter = (div_counter * 1) + 1
  
  if(div_counter == 3)
    avanti.style.display = "none"
  
  if(div_counter > 1)
    dietro.style.display = "block"

  divs.forEach(div => {
    div.style.display = "none"
    d = div.attributes
    if (d["id"].value == div_counter.toString()) {
      div.style.display = "block"
    }
  });
}

function Dietro() {
  div_counter = (div_counter * 1) - 1
  
  if(div_counter < 3)
    avanti.style.display = "block"
  
  if(div_counter == 1)
    dietro.style.display = "none"

  divs.forEach(div => {
    div.style.display = "none"
    d = div.attributes
    if (d["id"].value == div_counter.toString()) {
      div.style.display = "block"
    }
  });
}

function Check() {
  var nome = document.getElementById("nome").value
  var cognome = document.getElementById("cognome").value
  var email = document.getElementById("email").value
  var password = document.getElementById("password").value
  var confermaPassword = document.getElementById("confermaPassword").value
  var indirizzo = document.getElementById("indirizzo").value
  var dataNascita = document.getElementById("dataNascita").value
  var partitaiva = document.getElementById("partitaiva").value
  var standard = document.getElementById("standard")
  var premium = document.getElementById("premium")
  var numerocarta = document.getElementById("numerocarta").value
  var titolare = document.getElementById("titolare").value
  var scadenza = document.getElementById("scadenza").value
  var cvv = document.getElementById("cvv").value
  
  var nomeerr = document.getElementById("nomeerr")
  var cognomeerr = document.getElementById("cognomeerr")
  var emailerr = document.getElementById("emailerr")
  var passworderr = document.getElementById("passerr")
  var confermaerr = document.getElementById("conferr")
  var indirizzoerr = document.getElementById("indirizzoerr")
  var dataNascitaerr = document.getElementById("dataerr")
  var partitaivaerr = document.getElementById("partitaivaerr")
  var licenzaerr = document.getElementById("licenzaerr")
  var numerocartaerr = document.getElementById("numerocartaerr")
  var titolareerr = document.getElementById("titolareerr")
  var scadenzaerr = document.getElementById("scadenzaerr")
  var cvverr = document.getElementById("cvverr")

  const nomereg = /^[a-z]{2,30}$/i
  const mailreg = /[A-Z0-9._%+-]+@[A-Z0-9-]+.+.[A-Z]{2,4}/i
  const passreg = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&_])[A-Za-z\d$@$!%*?&_]{8,20}$/
  const indireg = /^[A-Za-zÀ-ù0-9 ,‘-]+$/
  const cartareg = /^(?:4[0-9]{12}(?:[0-9]{3})?|[25][1-7][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\d{3})\d{11})$/
  const titolarereg = /^[a-z ]{4,64}$/i
  const scadenzareg = /^(0[1-9]|1[0-2])\/?([0-9]{4}|[0-9]{2})$/
  const cvvreg = /^[0-9]{3,4}$/

  var register = true

  nomeerr.innerHTML = ""
  cognomeerr.innerHTML = ""
  emailerr.innerHTML = ""
  passworderr.innerHTML = ""
  confermaerr.innerHTML = ""
  indirizzoerr.innerHTML = ""
  dataNascitaerr.innerHTML = ""
  partitaivaerr.innerHTML = ""
  licenzaerr.innerHTML = ""
  numerocartaerr.innerHTML = ""
  titolareerr.innerHTML = ""
  scadenzaerr.innerHTML = ""
  cvverr.innerHTML = ""

  if(!nomereg.test(nome))
  {
    if(nome == "")
      nomeerr.innerHTML = "Campo Richiesto"
    else
      nomeerr.innerHTML = "Formato non valido"
    register = false
  }

  if(!nomereg.test(cognome))
  {
    if(cognome == "")
      cognomeerr.innerHTML = "Campo Richiesto"
    else
      cognomeerr.innerHTML = "Formato non valido"
    register = false
  }

  if(!mailreg.test(email))
  {
    if(email == "")
      emailerr.innerHTML = "Campo Richiesto"
    else
      email.innerHTML = "Formato non valido"
    register = false
  }

  if(!passreg.test(password))
  {
    if(password == "")
      passworderr.innerHTML = "Campo Richiesto"
    else
      passworderr.innerHTML = "Formato non valido"
    register = false
  }

  if(password != confermaPassword)
  {
    confermaerr.innerHTML = "Le due password non corrispondono"
    register = false
  }

  if(!indireg.test(indirizzo))
  {
    if(indirizzo == "")
      indirizzoerr.innerHTML = "Campo Richiesto"
    else
      indirizzoerr.innerHTML = "Formato non valido"
    register = false
  }

  if(dataNascita == "")
  {
    dataNascitaerr.innerHTML = "Campo Richiesto"
  }

  if(partitaiva == "")
  {
    partitaivaerr.innerHTML = "Campo Richiesto"
  }

  if(!cartareg.test(numerocarta))
  {
    if(numerocarta == "")
      numerocartaerr.innerHTML = "Campo Richiesto"
    else
      numerocartaerr.innerHTML = "Formato non valido"
    register = false
  }

  if(!titolarereg.test(titolare))
  {
    if(titolare == "")
      titolareerr.innerHTML = "Campo Richiesto"
    else
      titolareerr.innerHTML = "Formato non valido"
    register = false
  }

  if(!scadenzareg.test(scadenza))
  {
    if(scadenza == "")
      scadenzaerr.innerHTML = "Campo Richiesto"
    else
      scadenzaerr.innerHTML = "Formato non valido"
    register = false
  }

  if(!cvvreg.test(cvv))
  {
    if(cvv == "")
      cvverr.innerHTML = "Campo Richiesto"
    else
      cvverr.innerHTML = "Formato non valido"
    register = false
  }
  
  if(!standard.checked && !premium.checked)
  {
    licenzaerr.innerHTML = "Campo Richiesto"
  }
  else
  {
    var licenza
    if(standard.checked)
    {
      licenza = standard.value
    }
    else
    {
      licenza = premium.value
    }
  }

  if(register)
  {
    var form = document.querySelector("#form")
    form.submit();
  }
}