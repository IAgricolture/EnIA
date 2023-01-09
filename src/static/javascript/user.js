var view = document.querySelector("#view")
var usermod = document.querySelector("#usermod")
var licenzamod = document.querySelector("#licenzamod")
var metodomod = document.querySelector("#metodomod")


function ModUser()
{
    view.style.display = "none"
    usermod.style.display = "flex"
    licenzamod.style.display = "none"
    metodomod.style.display = "none"
}

function ModLicenza()
{
    view.style.display = "none"
    usermod.style.display = "none"
    licenzamod.style.display = "flex"
    metodomod.style.display = "none"
}

function ModMetodo()
{
    view.style.display = "none"
    usermod.style.display = "none"
    licenzamod.style.display = "none"
    metodomod.style.display = "flex"
}