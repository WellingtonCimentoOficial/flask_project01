const sub_menu_account = document.querySelector('.sub-account')
const account_icon = document.querySelector('ul.menu-bar li img.account-icon')
var menu_status = false
var icon_theme = document.querySelector('.theme-icon')
var icon_theme_status = false
const body_body = document.querySelector('body')
const sections = document.querySelectorAll('.dark')
const theme_dark = document.querySelectorAll('.theme-theme')

account_icon.addEventListener('click', () => {
    if (menu_status == false) {
        account_icon.style.color = "#0073ba"
        menu_status = true
    } else {
        if (icon_theme_status == true) {
            //icone do thema ativado
            account_icon.style.color = "white"
            menu_status = false
        } else {
            //icone do thema desativado
            account_icon.style.color = "black"
            menu_status = false
        }
    }
    sub_menu_account.classList.toggle("on")
})

icon_theme.addEventListener('click', () => {
    if (icon_theme_status == false) {
        //primeiro clique
        icon_theme.classList.toggle("far")
        icon_theme.classList.toggle("fas")
        body_body.style.backgroundColor = "#171717"
        icon_theme.style.color = "black"
        icon_theme.style.backgroundColor = "white"
        account_icon.style.color = "white"
        for (var c = 0; c < theme_dark.length; c++) {
            theme_dark[c].style.color = "white"
        }
        for (var c = 0; c < sections.length; c++) {
            sections[c].style.backgroundColor = "#171717"
        }
        icon_theme_status = true
    } else {
        //segundo clique
        icon_theme.classList.toggle("fas")
        icon_theme.classList.toggle("far")
        body_body.style.backgroundColor = "white"
        icon_theme.style.backgroundColor = "black"
        icon_theme.style.color = "white"
        account_icon.style.color = "black"
        for (var c = 0; c < theme_dark.length; c++) {
            theme_dark[c].style.color = "black"
        }
        for (var c = 0; c < sections.length; c++) {
            sections[c].style.backgroundColor = "white"
        }
        icon_theme_status = false
    }
    
})