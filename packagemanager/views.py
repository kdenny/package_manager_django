# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.forms.models import model_to_dict
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.http import HttpResponse

from packagemanager.models import Apartment, Resident, Package
from packagemanager.serializers import PackageReadSerializer, PackageCreateSerializer, ResidentSerializer, ApartmentSerializer
import os
from urlparse import urlparse
from twilio.rest.resources import Connection
from twilio.rest.resources.connection import PROXY_TYPE_HTTP

host, port = urlparse(os.environ["http_proxy"]).netloc.split(":")
Connection.set_proxy_info(
    host,
    int(port),
    proxy_type=PROXY_TYPE_HTTP,
)

from twilio.rest import TwilioRestClient

account = "AC03baeadb37d7438a8d8b57e819b98b83"
token = "b56cce2fd0222dfea54d36e627a4798b"
client = TwilioRestClient(account, token)

class PackagesListView(APIView):

    def get(self, request, apartment_key='0'):
        if (apartment_key == '0'):
            packages = Package.objects.all().order_by('date_received')
        else:
            packages = Package.objects.filter(apartment_no=apartment_key).order_by('date_received')
            print(packages)

        serializer = PackageReadSerializer(packages, many=True)
        return Response(serializer.data)

    def post(self, request):
        print(request.data)

        serializer = PackageCreateSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            print("serialized!")
            for package in request.data:

                resident_obj = Resident.objects.get(id=package['recipient'])
                resident_phone = '+1' + str(resident_obj.phone_number).strip()
                text_string = "Hi {0}! You have a package waiting for you at the front desk.".format(resident_obj.name)

                message = client.messages.create(to=resident_phone, from_="+12157098547",
                                                 body=text_string)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            #################### END POST RELATED METHODS ####################

class ApartmentsListView(APIView):

    def get(self, request):
        apartments = Apartment.objects.all()

        serializer = ApartmentSerializer(apartments, many=True)
        return Response(serializer.data)

class ApartmentResidentsView(APIView):

    def get(self, request, apartment_key='0'):
        if (apartment_key != '0'):
            apartment = Apartment.objects.get(number=apartment_key)
            residents = apartment.residents
        else:
            return None

        serializer = ResidentSerializer(residents, many=True)
        return Response(serializer.data)