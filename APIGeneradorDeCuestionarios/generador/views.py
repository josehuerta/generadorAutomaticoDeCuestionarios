from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Contenido
from .serializer import ContenidoSerializer

from rest_framework import status

from .crearCuestionario import GenerarPreguntas
from .crearCuestionario import FiltrarContenido


class Cuestionario(APIView):
    serializer_class = ContenidoSerializer

    def post(self, request, format=None):
        serializer = ContenidoSerializer(Contenido, data=request.data)
        # objetos para el filtrado y generacion de cuestionarios
        filtro = FiltrarContenido()
        generador = GenerarPreguntas()
        # obtenemos el texto de interes del usuario
        texto = ""
        texto = request.data['texto']
        # print("texto recibido"+texto)
        filtro.setTextoOriginal(texto)

        print("filtrado y etiquetado del texto\n\n")
        filtro.filtrarTexto()

        print("1 pasamos el texto filtrado y etiquetado \n\n")
        print(filtro.getTextoFiltrado())
        generador.setContenidoFiltrado(filtro.getTextoFiltrado())

        print("2 se comienza la generacion del cuestionario\n\n")
        cuestionario = generador.crearPreguntas()
        print("3 culminacion de generacion del cuestionario\n\n")
        if serializer.is_valid():
            return Response({'cuestionario': cuestionario})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
