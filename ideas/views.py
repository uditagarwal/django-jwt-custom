from .models import Ideas
from .serializers import IdeasSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


class IdeasList(generics.ListCreateAPIView):
    '''
    List and Create View for Ideas
    '''
    serializer_class = IdeasSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self, *args, **kwargs):
        return Ideas.objects.all().filter(user=self.request.user)


    def list(self, request, *args, **kwargs):
        response = super(IdeasList, self).list(request, args, kwargs)
        # doing this because the test expects it as a list of results 
        # without the extra information
        response.data = response.data['results']
        return response


class IdeasDetail(generics.RetrieveUpdateDestroyAPIView):
    '''
    GET, PUT and DELETE view for Ideas
    '''
    serializer_class = IdeasSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self, *args, **kwargs):
        return Ideas.objects.all().filter(user=self.request.user)
