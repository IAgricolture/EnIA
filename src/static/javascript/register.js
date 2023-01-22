function register(){
        
    var nome = document.getElementById("nome").value
    var cognome = document.getElementById("cognome").value
    var email = document.getElementById("email").value
    var password = document.getElementById("password").value
    var confermaPassword = document.getElementById("confermaPassword").value
    var codiceDiAccesso = document.getElementById("codiceDiAccesso").value
    var indirizzo = document.getElementById("indirizzo").value
    var dataNascita = document.getElementById("dataNascita").value
    console.log(dataNascita)

    var labelEmail = document.getElementById("labelEmail")
    var formPassword = document.getElementById("password")
    var labelPassword = document.getElementById("labelPassword")
    var labelCodice = document.getElementById("labelCodice")
    var formRegistrazione = document.getElementById("formRegistrazione")
    
    if( password != confermaPassword){
      
      labelPassword.innerHTML = "Le due password non corrispondono"
      formPassword.classList.add("has-error")
      formPassword.classList.add("has-feedback")
    }
    else{
      
      var data = new FormData()
      data.append("nome", nome)
      data.append("cognome", cognome)
      data.append("email", email)
      data.append("password", password)
      data.append("codice", codiceDiAccesso)
      data.append("indirizzo", indirizzo)
      data.append("dataNascita", dataNascita)

      let response = fetch("register",
      {
        "method": "POST",
        "headers": {},
        "body":data
      }).then(res=>res.json())
      .then(data=>{
          console.log(data)
          if(data["emailUsata"]){
            labelEmail.innerHTML += ":email già usata"
          } else if (data["codiceNonValido"]){
            labelCodice.innerHTML += ":codice non valido o già usato"
          } else if (data["utenteRegistrato"]){
            labelCodice.innerHTML += ":utenteNonRegistrato"
          } else{
            labelCodice.innerHTML += "utenteRegistrato"
          }
      })
    }
    
}