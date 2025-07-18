from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Provider
from .adapters import create_fhir_practitioner
from .serializers import PractitionerFHIRSerializer, BundleSerializer, create_bundle

def index(request):
    return HttpResponse("Connection to ndh database: successful")

def health(request):
    return HttpResponse("healthy")

class FHIRPractitionerViewSet(viewsets.ViewSet):
    """
    ViewSet for FHIR Practitioner resources
    """
    #permission_classes = [permissions.IsAuthenticated]
    def list(self, request):
        """
        Return a list of all providers as FHIR Practitioner resources
        """
        providers = Provider.objects.all()
        
        # Convert each provider to a FHIR Practitioner
        fhir_practitioners = [create_fhir_practitioner(provider) for provider in providers]
        
        # Create a Bundle containing all practitioners
        bundle = create_bundle(fhir_practitioners)
        
        # Serialize the bundle
        serializer = BundleSerializer(bundle)
        
        # Set appropriate content type for FHIR responses
        response = Response(serializer.data)
        response["Content-Type"] = "application/fhir+json"
        
        return response
    
    def retrieve(self, request, pk=None):
        """
        Return a single provider as a FHIR Practitioner resource
        """
        provider = get_object_or_404(Provider, pk=int(pk))
        
        # Convert provider to FHIR Practitioner
        fhir_practitioner = create_fhir_practitioner(provider)
        
        # Serialize the FHIR Practitioner
        serializer = PractitionerFHIRSerializer(fhir_practitioner)
        
        # Set appropriate content type for FHIR responses
        response = Response(serializer.data)
        response["Content-Type"] = "application/fhir+json"
        
        return response