import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
# import matplotlib.pyplot as plt

st.sidebar.title('Aula dia 21-05')

st.title('Filtros')

uploaded_file = st.sidebar.file_uploader("Escolha a imagem", type=['png', 'jpg'])


if uploaded_file is not None:
    image_original = Image.open(uploaded_file)
    image = np.copy(image_original)
    img_shape = (image_original.size[1],image_original.size[0])
    color = st.sidebar.radio(
     "",
     ('colorida', 'tons de cinza'))

    if color == 'tons de cinza':
        gray_arr = np.mean(np.array(image), axis=2)
        image = Image.fromarray(gray_arr).convert('L')

    option = st.sidebar.selectbox(
        'Escolha uma transformação',
        (
            'Escolha...',
            'Negativo',
            'Transformação em (log)',
            'Transformação (Power-Law)',
            'Alongamento de contraste',
            'Corte no nível de intensidade',
            'Média',
            'Gaussiano', # TODO:
            'Realce'
        )
    )

    st.sidebar.text(option)


    if(option == 'Negativo'):
        if color == 'tons de cinza':
            image = Image.fromarray(255 - gray_arr).convert('L')
        else:
            image = Image.fromarray(255 - image)
    elif(option == 'Transformação em (log)'):

        c = st.sidebar.slider('c', 0, 130, 25)
        st.sidebar.latex(r'''
            s = c log(1 + r)
        ''')
        if color == 'tons de cinza':
            log_image_arr = c * (np.log(gray_arr + 1))
            image = Image.fromarray(log_image_arr).convert('L')
            # image = Image.fromarray(255 - gray_arr).convert('L')
        else:
            image[:,:,0] = c * (np.log(image[:,:,0] + 1))
            image[:,:,1] = c * (np.log(image[:,:,1] + 1))
            image[:,:,2] = c * (np.log(image[:,:,2] + 1))
            image = Image.fromarray(image)
            # image = Image.fromarray(255 - gray_arr).convert('L')
    elif(option == 'Transformação (Power-Law)'):

        c = st.sidebar.slider('c', 0, 130, 25)
        gamma = st.sidebar.slider('gamma', 0., 25., .1)
        st.sidebar.latex(r'''
                    s = c r^\gammaγ
        ''')
        if color == 'tons de cinza':
            image = Image.fromarray(c * (gray_arr/255) ** gamma).convert('L')
        else:
            for i in range(3):
                image[:,:,i] = (c * (image[:,:,i]/255) ** gamma)

            image = Image.fromarray(image)

    elif(option == 'Alongamento de contraste'):
        intervals = st.sidebar.slider( 'Intervalo', 0, 255, (25, 75))
        s = st.sidebar.slider( 'valor de s', 0, 255, 75)

        if color == 'tons de cinza':
            # by Igor
            cinza_copia = np.copy(gray_arr)

            cinza_copia[cinza_copia < intervals[0]] = 0
            cinza_copia[(intervals[0] >= cinza_copia) & (cinza_copia <= intervals[1])] = s
            cinza_copia[cinza_copia > intervals[1]] = 0

            image = Image.fromarray(cinza_copia).convert('L')
        else:
            # imagem colorida
            colorida = np.copy(image)

            for i in range(3):
                colorida[colorida[:,:,i] < intervals[0]] = 0
                colorida[(intervals[0]>= colorida[:,:,i]) & (colorida[:,:,i] <= intervals[1])] = s
                colorida[colorida[:,:,i] > intervals[1]] = 0

            image = Image.fromarray(colorida)


    elif(option == 'Corte no nível de intensidade'):
        intervals = st.sidebar.slider( 'Intervalo', 0, 255, (25, 75))

        s = st.sidebar.slider( 'valor de s', 0, 255, 75)

        if color == 'tons de cinza':
            # by Thierris
            img = np.copy(gray_arr)
            img[(intervals[0] >= img) & (img <= intervals[1])] = s
            image = Image.fromarray(img).convert('L')
        else:
            #colorida
            colorida = np.copy(image)

            for i in range(3):
                colorida[(intervals[0]>= colorida[:,:,i]) & (colorida[:,:,i] <= intervals[1])] = s

            image = Image.fromarray(colorida)

    elif(option == 'Média'):

        tam = st.sidebar.slider( 'tamanho do filtro', 3, 9, 3)

        filtro = np.ones((tam,tam))/tam**2

        if color == 'tons de cinza':
            # by Kelvin
            img_filtered_arr = np.convolve(filtro.flatten(), gray_arr.flatten(), 'same')
            img_filtered_arr = img_filtered_arr.reshape(img_shape)
            image = Image.fromarray(img_filtered_arr).convert('L')

        else:
            # by Rafa/Manteiga!
            img = np.copy(image)
            r = image[:,:,0]
            g = image[:,:,1]
            b = image[:,:,2]

            img_filtered_arr_r = np.convolve(filtro.flatten(), r.flatten(), 'same').reshape(img_shape)
            img_filtered_arr_g = np.convolve(filtro.flatten(), g.flatten(), 'same').reshape(img_shape)
            img_filtered_arr_b = np.convolve(filtro.flatten(), b.flatten(), 'same').reshape(img_shape)

            img[:,:,0] = img_filtered_arr_r
            img[:,:,1] = img_filtered_arr_g
            img[:,:,2] = img_filtered_arr_b

            image = Image.fromarray(img)

    elif(option == 'Gaussiano'): # TODO: implementar o filtro gaussiano
        # TODO: colocar sidebars dos parâmetros da gaussiana

        if color == 'tons de cinza':
            image = Image.fromarray(gray_arr).convert('L')
        else:
            image = Image.fromarray(image)


    elif(option == 'Realce'):

        tam = st.sidebar.slider( 'tamanho do filtro', 3, 9, 3)
        filtro = np.ones((tam,tam))/tam**2

        # TODO: fazer um select com filtro da média ou gaussiano.

        if color == 'tons de cinza':
            img_gray_arr = np.copy(gray_arr)
            img_filtered_arr = np.convolve(filtro.flatten(), gray_arr.flatten(), 'same').reshape(img_shape)
            image = Image.fromarray(img_filtered_arr).convert('L')
            img_res_arr = img_gray_arr - img_filtered_arr

            image_res = Image.fromarray(img_res_arr).convert('L')

            img_realce_arr = img_gray_arr + img_res_arr
            img_realce = Image.fromarray(img_realce_arr).convert('L')
            img_gray = Image.fromarray(img_gray_arr).convert('L')

        else:
            image = Image.fromarray(image)


    if(option == 'Realce'):
        # st.image([image, image_res, img_realce, img_gray],width=[100,100,100,100])
        st.image(image,
            caption='Cage is a Sunrise 🌞 by the mountain 🌄',
            width=200,
            use_column_width=True)
        st.image(image_res,
            caption='Cage is a Sunrise 🌞 by the mountain 🌄',
            width=200,
            use_column_width=True)
        st.image(img_realce,
            caption='Cage is a Sunrise 🌞 by the mountain 🌄',
            width=200,
            use_column_width=True)
        st.image(img_gray,
            caption='Cage is a Sunrise 🌞 by the mountain 🌄',
            width=200,
            use_column_width=True)

    else:
        st.image(image, caption='Cage is a Sunrise 🌞 by the mountain 🌄', use_column_width=True)
