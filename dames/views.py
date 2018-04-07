from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.authtoken.models import Token
from dames.models import Partie
from dames.serializers import PartieSerializer


class PartieViewset(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        partie = Partie.objects.get(user=request.user)
        return HttpResponse(partie.data) #si j'utilise Response, DRF mettra des guillements supplémentaire

    def post(self, request):
        try:
            partie = Partie.objects.get(user=request.user)
        except Partie.DoesNotExist:
            partie = Partie.objects.create(user=request.user, data=request.data)
        partie.data = self.request.data
        partie.save()
        return Response(request.data, status=201)
    def delete(self, request):
        Partie.objects.get(user=request.user).delete()
        return Response("Partie finie !")

@api_view(http_method_names=['GET'])
def liste(request):
    reponse = []
    for partie in Partie.objects.exclude(player2__gt=''):
            reponse.append({"id":partie.id,
                        "player1": partie.player1})
    return Response(reponse)

@api_view(['GET'])
def rejoindre(request, pk):
    partie = Partie.objects.get(id=pk)
    token = Token.objects.get(user=partie.user)
    return HttpResponse(token.key)

@api_view(['DELETE'])
def delete(request):
    partie = Partie.objects.get(user=request.user)
    Token.objects.get(user=request.user).delete()
    partie.delete()
    request.user.delete()
    return Response("DELETED")

class Lobby(ModelViewSet):
    queryset = Partie.objects.exclude(player2__gt='')
    serializer_class = PartieSerializer

    def create(self, request, *args, **kwargs):
        serializer = PartieSerializer(data=request.data)
        if serializer.is_valid():
            return HttpResponse(serializer.create(serializer.validated_data))


