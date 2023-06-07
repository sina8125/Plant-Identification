import os
import shutil

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404

from auth_api.authentication import CustomJWTAuthentication
from .models import Plant, Leaf, Stem, Flower, Medicine
from .serializers import PlantSerializer, LeafSerializer, StemSerializer, FlowerSerializer, MedicinalSerializer


class PlantList(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        plants = Plant.objects.all()
        serializer = PlantSerializer(plants, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PlantSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlantDetail(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Plant.objects.get(pk=pk)
        except Plant.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        plant = self.get_object(pk)
        serializer = PlantSerializer(plant)
        return Response(serializer.data)

    def put(self, request, pk):
        plant = self.get_object(pk)
        serializer = PlantSerializer(plant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        plant = self.get_object(pk)
        image_path = plant.image.path
        plant.delete()
        image_path = image_path[0: image_path.rindex('\\') + 1]
        shutil.rmtree(image_path)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PlantLeafImageList(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        leafs = Leaf.objects.all()
        serializer = LeafSerializer(leafs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LeafSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlantLeafImageDetail(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Leaf.objects.get(pk=pk)
        except Plant.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        leaf = self.get_object(pk)
        serializer = LeafSerializer(leaf)
        return Response(serializer.data)

    def put(self, request, pk):
        leaf = self.get_object(pk)
        old_image_path = leaf.image.path
        if os.path.isfile(old_image_path):
            os.remove(old_image_path)

        serializer = LeafSerializer(leaf, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        leaf = self.get_object(pk)
        image_path = leaf.image.path
        leaf.delete()
        if os.path.isfile(image_path):
            os.remove(image_path)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PlantStemImageList(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        stems = Stem.objects.all()
        serializer = StemSerializer(stems, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlantStemImageDetail(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Stem.objects.get(pk=pk)
        except Stem.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        stem = Stem.objects.get(pk=pk)
        serializer = StemSerializer(stem)
        return Response(serializer.data)

    def put(self, request, pk):
        stem = self.get_object(pk)
        old_image_path = stem.image.path
        if os.path.isfile(old_image_path):
            os.remove(old_image_path)
        # based on how to call serializer by different parameter in each function,it can do what you want
        # for example below line,stem is old data , request.data is new data,then serializer update old data to new data
        # stem.image = request.FILES.get('image')
        # stem.save()
        serializer = StemSerializer(stem, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        stem = self.get_object(pk)
        image_path = stem.image.path
        stem.delete()
        if os.path.isfile(image_path):
            os.remove(image_path)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PlantFlowerImageList(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        flowers = Flower.objects.all()
        serializer = FlowerSerializer(flowers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FlowerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlantFlowerImageDetail(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Flower.objects.get(pk=pk)
        except Flower.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        flower = self.get_object(pk)
        serializer = FlowerSerializer(flower)
        return Response(serializer.data)

    def put(self, request, pk):
        flower = self.get_object(pk)
        old_image_path = flower.image.path
        if os.path.isfile(old_image_path):
            os.remove(old_image_path)
        serializer = FlowerSerializer(flower, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        flower = self.get_object(pk)
        image_path = flower.image.path
        flower.delete()
        if os.path.isfile(image_path):
            os.remove(image_path)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PlantMedicinalList(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self):
        medicines = Medicine.objects.all()
        serializer = MedicinalSerializer(medicines, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MedicinalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlantMedicinalDetail(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Medicine.objects.get(pk=pk)
        except Medicine.DoesNotExist:
            raise Http404

    def get(self, pk):
        medicine = self.get_object(pk)
        serializer = MedicinalSerializer(medicine)
        return Response(serializer.data)

    def put(self, request, pk):
        medicine = self.get_object(pk)
        serializer = Medicine(medicine, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        medicine = self.get_object(pk)
        medicine.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
