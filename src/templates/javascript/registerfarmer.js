var divs = document.querySelectorAll(".form-group")
var div_counter = 1

function Avanti(){
    div_counter = (div_counter *1) + 1
    console.log("bo" + div_counter)
    divs.forEach(div => {
        div.style.display = "none"
        d = div.attributes 
        console.log(d['id'])
        if (d["id"].value == div_counter.toString()){
            div.style.display = "block"
        }
    });
}

function Dietro(){
    div_counter = (div_counter *1) - 1
    console.log("bo" + div_counter)
    divs.forEach(div => {
        div.style.display = "none"
        d = div.attributes 
        console.log(d['id'])
        if (d["id"].value == div_counter.toString()){
            div.style.display = "block"
        }
    });
}

function register(){    
    var nome = document.getElementById("nome").value
    var cognome = document.getElementById("cognome").value
    var email = document.getElementById("email").value
    var password = document.getElementById("password").value
    var confermaPassword = document.getElementById("confermaPassword").value
    var indirizzo = document.getElementById("indirizzo").value
    var dataNascita = document.getElementById("dataNascita").value
    var partitaiva = document.getElementById("partitaiva").value
    var licenza = document.getElementById("licenza").value
    var numerocarta = document.getElementById("numerocarta").value
    var titolare = document.getElementById("titolare").value
    var scadenza = document.getElementById("scadenza").value
    var cvv = document.getElementById("cvv").value

    var labelEmail = document.getElementById("labelEmail")
    var formPassword = document.getElementById("password")
    var labelPassword = document.getElementById("labelPassword")
    
    if( password != confermaPassword){
      
      labelPassword.innerHTML = "Le due password non corrispondono"
      formPassword.classList.add("has-error")
      formPassword.classList.add("has-feedback")
    }
    else{
      var url = new URL("http://localhost:5000/registerf")
      url.searchParams.append("email", email)
      url.searchParams.append("nome", nome)
      url.searchParams.append("cognome", cognome)
      url.searchParams.append("password", password)
      url.searchParams.append("indirizzo", indirizzo)
      url.searchParams.append("dataNascita", dataNascita)
      url.searchParams.append("partitaiva", partitaiva)
      url.searchParams.append("licenza", licenza)
      url.searchParams.append("numerocarta", numerocarta)
      url.searchParams.append("titolare", titolare)
      url.searchParams.append("scadenza", scadenza)
      url.searchParams.append("cvv", cvv)

      let response = fetch(url,
      {
        "method": "GET",
        "headers": {},
      }).then(res=>res.json())
      .then(data=>{
          console.log(data)
          if(data["emailUsata"]){
            labelEmail.innerHTML += ":email già usata"
          } else if (data["utenteRegistrato"]){
            labelCodice.innerHTML += ":utenteNonRegistrato"
          } else{
            labelCodice.innerHTML += "utenteRegistrato"
          }
      })
    }
    
}



