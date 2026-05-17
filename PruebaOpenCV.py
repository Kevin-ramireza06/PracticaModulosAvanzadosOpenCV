import cv2
# Aqui importamos libreria openCV
import time
# Esta librería propia de Python es para poder trabajar con el tiempo
import winsound
# Esta librería propia de Python es para reproducir los sonidos del sistema Windows

referencia_camara = cv2.VideoCapture(0)
# Con la función .VideoCapture() capturamos la cámara de nuestro dispositivo.
# De parámetros podemos poner un número, siendo el 0 la cámara por defecto de nuestro dispositivo, y si sumamos
# serán las demás cámaras del dispositivo.

# Para trabajar con un video, ponemos la ruta, junto con la extensión de este como parámetro entre ''

detector_ojos = cv2.CascadeClassifier('Hardcascades/haarcascade_eye.xml')
# Con la función .CascadeClassifier() integramos a nuestro proyecto un hardcascade, de parámetro le pasamos la ruta en
# donde está ubicada el hardcascade que vamos a usar, en nuestro caso, uno que detecte los ojos.

tiempo_inicio_distraccion = 0
LIMITE_SEGUNDOS = 3
foto_tomada = False

while (True):
    # También podemos usar la función .isOpened() que lo que hace es devolver true siempre que OpenCV haya sido capaz de leer
    # los datos de la cámara.

    estaGrabando, imagen = referencia_camara.read()
    # La función .read() nos devuelve 2 valores, el primero es un booleano que indica si se está o no grabando la imagen.
    # Y el segundo es la imagen como tal.

    if (estaGrabando):

        gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        # La función .cvtColor() nos permite pasar la imagen que le pasemos por parámetro, a la escala de colores que
        # queramos, en nuestro caso, una escala de grises (mediante la constante) para que al hardcascade le quede más
        # fácil identificar los elementos que éste busca.
        ojos = detector_ojos.detectMultiScale(gris, 1.33, 9)
        # Aquí estamos usando el hardcascade, la función .detectMultiScale() lo que hace es buscar y detectar en la
        # imagen (ahora en escala de grises) las coincidencias que encuentre en la imagen, de lo que el hardcascade busca
        # (en nuestro caso detecta todo aquello que el hardcascade entienda como un ojo).

        # Este recibe 3 parámetros. El primero es la escala de colores que estamos manejando, en nuestro caso el gris. El
        # segundo es cómo el hardcascade va a intentar identificar los elementos que busca, reduciendo el tamaño de la
        # imagen internamente varias veces el porcentaje que definamos en el parámetro, en nuestro caso sería un 30% (1.30),
        # esto define la precisión con la que va a querer buscar coincidencias. Entre más pequeño, más preciso va a ser, por
        # ende va a hacer más lento el programa.

        # El tercero es el filtro de calidad, éste define cuántas veces tiene que detectar algo parecido a lo que
        # estamos buscando en la misma zona para darlo por válido. Entre más bajo el número, menos estricto y preciso es,
        # por lo que en nuestro caso, puede confundir cualquier cosa con un ojo.

        for (x, y, w, h) in ojos:
            # La función .detectMultiScale() devuelve 4 valores, los cuales son las coordenadas x, y, el alto y el ancho.

            cv2.rectangle(imagen, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # La función .rectangle() pinta un rectángulo en la imagen que se le pase por parámetro. De segundo parámetro
            # se le pasan las coordenadas, de tercero el tamaño, de cuarto es el color que vamos a pintar el cuadrado y el
            # último el grosor de éste.

        if len(ojos) == 0 :
            # La función .len() nos sirve en nuestro caso para contar los ojos que se han encontrado.

            if tiempo_inicio_distraccion == 0:
                tiempo_inicio_distraccion = time.time()
                # La función .time() de la librería time, captura el momento exacto en el que se ejecuta
                # mediante un número, lo usamos para contabilizar el tiempo que la persona está distraída.
            else:
                tiempo_pasado = time.time() - tiempo_inicio_distraccion
                # Aquí definimos cuánto tiempo ha pasado desde que se detectó la distracción.
                if tiempo_pasado > LIMITE_SEGUNDOS:
                    # Si ha pasado más tiempo del que definimos, entonces informamos de la distracción.

                    cv2.putText(imagen, "TE HAS DISTRAIDO", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    # La función .putText() nos permite poner texto en la imagen que se ejecute. Recibe la imagen,
                    # el texto que vas a pintar, las coordenadas de la imagen en donde lo vas a pintar (siendo el 0,0 la
                    # esquina superior izquierda), la fuente de la letra (que usamos una constante de OpenCV), el tamaño,
                    # el color y por último el grosor.

                    if not foto_tomada:
                        nombre_archivo = f"Imagenes/Prueba_distraccion_{int(time.time())}.png"
                        cv2.imwrite(nombre_archivo, imagen)
                        # La función .imwrite() nos guarda la imagen en la ruta que le pasemos por parámetro. En este
                        # caso, guardamos la prueba de que la persona se ha distraído.
                        # Si la ruta o carpeta no existe no lo guardará.

                        print(f"Te has distraido. Prueba guardada en: {nombre_archivo}")

                        winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS | winsound.SND_ASYNC)
                        # Con esta línea reproducimos el sonido típico de Windows.

                        foto_tomada = True
        else:
            tiempo_inicio_distraccion = 0
            foto_tomada = False

        cv2.imshow("Captura de video", imagen)
        # La función .imshow() abre en una ventana lo que está capturando la cámara. El primer parámetro es el título de
        # la ventana, y el segundo, como vimos en la variable anterior, la imagen procesada. Pero al estar en un while, esto
        # se procesa y cambia constantemente, dando la sensación de un video.

        if (cv2.waitKey(1) & 0xFF == ord(' ')):
            # La función .waitKey() indica si se ha presionado una tecla en el lapso de tiempo que definamos como
            # parámetro, la segunda condición es para devolver si se presionó la tecla que definamos, en este caso el espacio.
            print("Acabas de cerrar la grabacion de video")
            break

        if (cv2.waitKey(24) & 0xFF == ord('f')):
            cv2.imwrite("Imagenes/Captura.png", imagen)
            # La función .imwrite() nos guarda la imagen en la ruta que le pasemos por parámetro, en nuestro caso el
            # frame que hay en la cámara al momento de presionar la "f".
            print("Acabas de tomar una captura")
            captura_imagen = cv2.imread("Imagenes/Captura.png")
            # La función .imread() captura y muestra la imagen que le pasemos por parámetro.
            cv2.imshow("Captura que acabamos de tomar", captura_imagen)

    else:
        print("No hay camara")
        break

referencia_camara.release()
# La función .release() lo que hace es borrar el contenido de nuestra referencia a OpenCV.
cv2.destroyAllWindows()
# La función .destroyAllWindows() como su nombre lo indica cierra todas las ventanas de la cámara que se hayan abierto.

# De esta forma cerramos correctamente cualquier programa de OpenCV.