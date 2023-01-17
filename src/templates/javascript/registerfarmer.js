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



