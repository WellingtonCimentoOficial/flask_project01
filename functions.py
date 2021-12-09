def renameprofile(mimetype):
    '''
    identifica a extensão da imagem e
    renomea a mesma.
    '''
    if 'png' in mimetype:
        name = 'profile.png'
        return name
    elif 'jpg' in mimetype:
        name = 'profile.jpg'
        return name
    elif 'jpeg' in mimetype:
        name = 'profile.jpeg'
        return name
    else:
        return 'error'