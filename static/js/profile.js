const input_upload_photo_profile = document.querySelector("#input-upload-photo")
const photo_profile = document.querySelector("#photo-profile")
const text_image_upload = document.querySelector(".text-image-upload")
const profile_upload_options = document.querySelector(".profile-upload-options")
const profile_upload_icon = document.querySelector('.profile-upload-icon')
const input_upload_photo = document.getElementById('input-upload-photo')

//Efeitos quando o mouse fica e sai de cima da imagem de perfil
input_upload_photo_profile.addEventListener('mouseover', function(){
    photo_profile.style.opacity = "0.3"
    text_image_upload.style.display = "block"
    profile_upload_options.style.display = "flex"
})
input_upload_photo_profile.addEventListener('mouseout', function(){
    photo_profile.style.opacity = "1"
    text_image_upload.style.display = "none"
    profile_upload_options.style.display = "none"
})

text_image_upload.addEventListener('mouseover', function(){
    photo_profile.style.opacity = "0.3"
    text_image_upload.style.display = "block"
    profile_upload_options.style.display = "flex"
})
text_image_upload.addEventListener('mouseout', function(){
    photo_profile.style.opacity = "1"
    text_image_upload.style.display = "none"
    profile_upload_options.style.display = "none"
})


//Opções que aparecem quando o mouse fica e sai de cima da imagem de perfil
profile_upload_options.addEventListener('mouseover', () => {
    photo_profile.style.opacity = "0.3"
    text_image_upload.style.display = "block"
    profile_upload_options.style.display = "flex"
})
profile_upload_options.addEventListener('mouseout', () => {
    photo_profile.style.opacity = "1"
    text_image_upload.style.display = "none"
    profile_upload_options.style.display = "none"
})

profile_upload_icon.addEventListener('click', () => { //quando clicar no icone de upload, clicar também no arquivo de upload
    input_upload_photo.click()
})
text_image_upload.addEventListener('click', () => { //quando clicar no texto de upload, clicar também no arquivo de upload
    input_upload_photo.click()
})