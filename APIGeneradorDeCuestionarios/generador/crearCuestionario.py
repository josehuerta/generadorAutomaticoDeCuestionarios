import spacy


class FiltrarContenido:
    textoOriginal = ""
    textoFiltrado = []

    def filtrarTexto(self):
        texto = self.getTextoOriginal()
        texto = texto.replace('-', '')
        texto = texto.replace(".", " ")
        texto = texto.replace('  ', ' ')
        texto = texto.replace(',', ' ')

        posExcluidos = ["INTJ", "PART", "PUNCT", "CCONJ", "CONJ", "NUM",
                        "SYM", "X", "SPACE"]

        nlp = spacy.load('es_core_news_lg')
        doc = nlp(texto)  # Crea un objeto de spacy tipo nlp

        # tokenizacion
        tokens = [token for token in doc]
        i = 0
        lnTokens = len(tokens)
        self.textoFiltrado = []
        while i < lnTokens:
            parrafo = []
            caso = 1
            respuesta = ""

            if (tokens[i].pos_ == "NOUN" or tokens[i].pos_ == "PROPN") and i+1 < lnTokens:
                # guardamos el sustantivo
                if tokens[i+1].pos_ == "CCONJ" and tokens[i+2].pos_ == "PROPN":
                    if i > 0 and tokens[i-1] and tokens[i-1].pos_ == "DET":
                        subject = str(tokens[i-1])+" "+str(tokens[i])+" " + \
                            str(tokens[i+1])+" "+str(tokens[i+2])
                    else:
                        subject = str(tokens[i])+" " + \
                            str(tokens[i+1])+" "+str(tokens[i+2])
                    parrafo.append(subject)
                    i = i+2
                else:

                    if tokens[i-1] and (tokens[i-1].pos_ == "ADP" or tokens[i-1].pos_ == "DET"):
                        # agregamos el adp o det
                        subject = str(tokens[i-1]).lower() + " "+str(tokens[i])
                    else:
                        subject = tokens[i]

                    parrafo.append(tokens[i])
                    i = i+1

                if (tokens[i].pos_ == "VERB" or tokens[i].pos_ == "AUX") and tokens[i].pos_ not in posExcluidos:
                    # agregamos el verbo que esta en seguida del sustantivo
                    parrafo.append(tokens[i])

                    if i+1 < lnTokens:

                        if tokens[i+1].pos_ != "VERB" and tokens[i+1].pos_ not in posExcluidos:
                            # caso 1
                            # noun+verb+idk
                            tipo = self.etiquetarContenido(tokens[i+1])

                            # obteniendo la respuesta
                            if tokens[i+1] and tokens[i+2]:

                                # en caso de que ka respuesta sea mayor a 2
                                if tokens[i+2].pos_ == "ADP" or tokens[i+2].pos_ == "DET" or tokens[i+2].pos_ == "ADV" and tokens[i+3]:
                                    respuesta = str(
                                        tokens[i+1])+" "+str(tokens[i+2] + " " + str(tokens[i+3]))
                                else:
                                    respuesta = str(
                                        tokens[i+1])+" "+str(tokens[i+2])

                            elif tokens[i+1]:
                                respuesta = str(tokens[i+1])

                            parrafo.append([caso, tipo])
                            parrafo.append(respuesta)

                        else:
                            # noun+verb+verb+idk
                            parrafo.append(tokens[i+1])
                            if i+2 < lnTokens:
                                if tokens[i+2].pos_ != "VERB" and tokens[i+2].pos_ not in posExcluidos:
                                    # caso2
                                    tipo = self.etiquetarContenido(tokens[i+2])

                                    # respuesta
                                    if tokens[i+2] and tokens[i+3]:
                                        respuesta = str(
                                            tokens[i+2])+" "+str(tokens[i+3])
                                    elif tokens[i+2]:
                                        respuesta = str(tokens[i+2])

                                    caso = 2
                                    parrafo.append([caso, tipo])
                                    parrafo.append(respuesta)

                                else:
                                    # noun+verb+verb+verb+idk
                                    # caso 3
                                    parrafo.append(tokens[i+2])
                                    if tokens[i+3].pos_ != "VERB" and tokens[i+3].pos_ not in posExcluidos:
                                        tipo = self.etiquetarContenido(
                                            tokens[i+3])

                                        if tokens[i+3] and tokens[i+4]:
                                            respuesta = str(
                                                tokens[i+3])+" "+str(tokens[i+4])
                                        elif tokens[i+3]:
                                            respuesta = str(tokens[i+3])

                                        caso = 3
                                        parrafo.append([caso, tipo])
                                        parrafo.append(respuesta)

                    if len(parrafo) > 1:
                        for p in parrafo:
                            # validamos si parrafo contiene una lista
                            # la lista nos da el caso y el tipo de interrogativo que tendra
                            # entonces si no la tiene , no es candidato a pregunta
                            if isinstance(p, list):
                                self.setTextoFiltrado(parrafo)

            i += 1

    def setTextoOriginal(self, textoOriginal):
        self.textoOriginal = textoOriginal

    def getTextoOriginal(self):
        return self.textoOriginal

    def setTextoFiltrado(self, textoFiltrado):
        self.textoFiltrado.append(textoFiltrado)

    def getTextoFiltrado(self):
        return self.textoFiltrado

    def etiquetarContenido(self, token):
        # pos: part of speech
        dicPOS = {
            "ADJ": "1",
            "DET": "2",
            "ADP": "3",
            "AUX": "4",
            "ADV": "5",
            "NOUN": "6",
            "NUM": "7",
            "advTiempo": "8",
            "advLugar": "9",
            "advModo": "10",
            "advCantidad": "11",
            "adpTiempo": "12",
            "adpLugar": "13",
            "adpModo": "14",
            "adpMotivo": "15",
            "PROPN": "16",
            "PRON": "17",
            "CCONJ": "18"

        }
        dicKeys = list(dicPOS.keys())

        adpLugar = ['a', 'bajo', 'en', 'entre', 'hasta', 'hacia', 'por',
                    'sobre', 'tras', 'dentro', 'delante', 'debajo', 'detras']
        adpModo = ['ante', 'con', 'contra', 'sin', 'según', 'mediante', 'vía']
        adpMotivo = "para"
        adpTiempo = "desde"

        advTiempo = ['ya', 'aún', 'hoy', 'tarde', 'pronto', 'todavía',
                     'ayer', 'recién', 'nunca', 'siempre', 'jamás', 'ahora']
        advLugar = ['ahí', 'allí', 'aquí', 'acá', 'delante', 'detrás',
                    'arriba', 'abajo', 'cerca', 'lejos', 'encima', 'fuera', 'dentro']
        advModo = ['mal', 'bien', 'regular', 'despacio',
                   'así', 'mejor', 'peor', 'similar', 'fácilmente']
        advCantidad = ['muy', 'más', 'poco', 'bastante',
                       'demasiado', 'menos', 'mucho', 'algo', 'casi']

        tipoDePalabra = ""
        if token.pos_ in dicKeys:
            if token.pos_ == "ADP":
                if str(token) in adpTiempo:
                    tipoDePalabra = dicPOS["adpTiempo"]
                elif str(token) in adpLugar:
                    tipoDePalabra = dicPOS["adpLugar"]
                elif str(token) in adpModo:
                    tipoDePalabra = dicPOS["adpModo"]
                elif str(token) in adpMotivo:
                    tipoDePalabra = dicPOS["adpMotivo"]
                else:
                    tipoDePalabra = dicPOS[token.pos_]
            elif token.pos_ == "ADV":
                if str(token) in advTiempo:
                    tipoDePalabra = dicPOS["advTiempo"]
                elif str(token) in advLugar:
                    tipoDePalabra = dicPOS["advLugar"]
                elif str(token) in advModo:
                    tipoDePalabra = dicPOS["advModo"]
                elif str(token) in advCantidad:
                    tipoDePalabra = dicPOS["advCantidad"]
                else:
                    tipoDePalabra = dicPOS[token.pos_]
            else:
                tipoDePalabra = dicPOS[token.pos_]

            return tipoDePalabra
        else:
            print("etiquetado:"+str(token)+str(token.pos_))


class GenerarPreguntas:
    contenidoFiltrado = []
    diccionarioInterrogativos = {}

    def __init__(self):
        self.diccionarioInterrogativos = {
            "1": "Cómo",
            "2": "Qué",
            "3": "Dónde",
            "4": "Qué",
            "5": "Cuándo",
            "6": "Qué",
            "7": "Cuántos",
            "8": "Cuándo",
            "9": "Dónde",
            "10": "Cómo",
            "11": "Cuántos",
            "12": "Cuándo",
            "13": "Dónde",
            "14": "Cómo",
            "15": "Para qué",
            "16": "Qué",
            "17": "Qué",
            "18": "Qué"}

    def obtenerTipoComplemento(self):
        contenido = self.getContenidoFiltrado()
        # el tipo de complemento esta en -2 ya que -2 es la respuesta
        listaTipoComplementos = [listaComplemento[-2]
                                 for listaComplemento in contenido]
        return listaTipoComplementos

    def setContenidoFiltrado(self, contenido):
        self.contenidoFiltrado = contenido

    def getContenidoFiltrado(self):
        return self.contenidoFiltrado

    def getDiccionarioInterrogativo(self, key):
        return self.diccionarioInterrogativos[key]

    def crearPreguntas(self):
        listaTipoComplemento = self.obtenerTipoComplemento()
        tipoComplemento = [valor[1] for valor in listaTipoComplemento]
        tipoFrase = [valor[0] for valor in listaTipoComplemento]
        # whith open('model_pickle', 'wb') as modelo:
        #     modeloPrediccion = pickle.load(modelo)
        sigInterrogacionInicial = "¿ "
        sigInterrogacionFin = "?"
        preguntas = []
        contenido = self.getContenidoFiltrado()

        lnContenido = len(contenido)
        for i in range(0, lnContenido):
            pregunta = []
            # interrogativo = modeloPrediccion.predict(tipo)
            # pregunta.append(interrogativo)
            # print(tipoComplemento[i])

            # agregamos el pronombre interrogativo
            # if self.getDiccionarioInterrogativo(tipoComplemento[i]):

            pregunta.append(
                self.getDiccionarioInterrogativo(tipoComplemento[i]))

            if tipoFrase[i] == 1:
                # agregamos el verbo
                pregunta.append(contenido[i][1])
            elif tipoFrase[i] == 2:
                # agregamos aux y verbo
                pregunta.append(contenido[i][1])
                pregunta.append(contenido[i][2])
            else:
                # agregamos aux aux verbo
                pregunta.append(contenido[i][1])
                pregunta.append(contenido[i][2])
                pregunta.append(contenido[i][3])

            # agregamos el sustantivo
            pregunta.append(str(contenido[i][0]))

            pregFinal = sigInterrogacionInicial
            for palabra in pregunta:
                aux = str(palabra)
                pregFinal = pregFinal+aux+" "

            pregFinal = pregFinal+sigInterrogacionFin

            # agregamos la respuesta, para quitarla solo hay que comentar las dos lineas de abajo
            respuesta = str(contenido[i][-1])
            pregFinal = pregFinal+" "+respuesta

            preguntas.append(pregFinal)

        return preguntas
