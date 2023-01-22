function register() {
    var nome = document.getElementById("nome").value
    var cognome = document.getElementById("cognome").value
    var email = document.getElementById("email").value
    var password = document.getElementById("password").value
    var confermaPassword = document.getElementById("confermaPassword").value
    var codiceDiAccesso = document.getElementById("codiceDiAccesso").value
    var indirizzo = document.getElementById("indirizzo").value
    var dataNascita = document.getElementById("dataNascita").value

    var nomeerr = document.getElementById("nomeerr")
    var cognomeerr = document.getElementById("cognomeerr")
    var emailerr = document.getElementById("emailerr")
    var passworderr = document.getElementById("passerr")
    var confermaerr = document.getElementById("conferr")
    var cod = document.getElementById("cod")
    var indirizzoerr = document.getElementById("indirizzoerr")
    var dataNascitaerr = document.getElementById("dataerr")

    const nomereg = /^[a-z ]{2,30}$/i
    const mailreg = /[A-Z0-9._%+-]+@[A-Z0-9-]+.+.[A-Z]{2,4}/i
    const passreg = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&_])[A-Za-z\d$@$!%*?&_]{8,20}$/
    const indireg = /^[A-Za-zÀ-ù0-9 ,‘-]+$/

    var register = true

    nomeerr.innerHTML = ""
    cognomeerr.innerHTML = ""
    emailerr.innerHTML = ""
    passworderr.innerHTML = ""
    confermaerr.innerHTML = ""
    cod.innerHTML = ""
    indirizzoerr.innerHTML = ""
    dataNascitaerr.innerHTML = ""

    if (!nomereg.test(nome)) {
      if (nome == "")
        nomeerr.innerHTML = "Campo Richiesto"
      else
        nomeerr.innerHTML = "Formato non valido"
      register = false
    }

    if (!nomereg.test(cognome)) {
      if (cognome == "")
        cognomeerr.innerHTML = "Campo Richiesto"
      else
        cognomeerr.innerHTML = "Formato non valido"
      register = false
    }

    if (!mailreg.test(email)) {
      if (email == "")
        emailerr.innerHTML = "Campo Richiesto"
      else
        emailerr.innerHTML = "Formato non valido"
      register = false
    }

    if (!passreg.test(password)) {
      if (password == "")
        passworderr.innerHTML = "Campo Richiesto"
      else
        passworderr.innerHTML = "Formato non valido"
      register = false
    }

    if (password != confermaPassword) {
      confermaerr.innerHTML = "Le due password non corrispondono"
      register = false
    }

    if (!indireg.test(indirizzo)) {
      if (indirizzo == "")
        indirizzoerr.innerHTML = "Campo Richiesto"
      else
        indirizzoerr.innerHTML = "Formato non valido"
      register = false
    }

    if (dataNascita == "") {
      dataNascitaerr.innerHTML = "Campo Richiesto"
      register = false
    }

    if (register) {
      var data = new FormData()
      data.append("nome", nome)
      data.append("cognome", cognome)
      data.append("email", email)
      data.append("password", password)
      data.append("codice", codiceDiAccesso)
      data.append("indirizzo", indirizzo)
      data.append("dataNascita", dataNascita)

      let response = fetch("register", {
          "method": "POST",
          "headers": {},
          "body": data
        }).then(res => res.json())
        .then(data => {
          console.log(data)
          if (data["emailUsata"]) {
            emailerr.innerHTML = "email già usata"
          } if (data["codiceNonValido"]) {
            cod.innerHTML = "codice non valido o già usato"
          }if(data["utenteRegistrato"]){
              window.location.href ="/login"
          }
        })
    }
  }