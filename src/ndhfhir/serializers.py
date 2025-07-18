from rest_framework import serializers
from fhir.resources.practitioner import Practitioner
from fhir.resources.bundle import Bundle

class FHIRSerializer(serializers.Serializer):
    """
    Base serializer for FHIR resources
    """
    def to_representation(self, instance):
        """
        Convert FHIR resource to JSON
        """
        # Use the resource's as_json() method to convert to JSON
        if hasattr(instance, 'dict'):
            return instance.dict()
        return super().to_representation(instance)

class PractitionerFHIRSerializer(FHIRSerializer):
    """
    Serializer for FHIR Practitioner resource
    """
    class Meta:
        model = Practitioner

class BundleSerializer(FHIRSerializer):
    """
    Serializer for FHIR Bundle resource
    """
    class Meta:
        model = Bundle


def create_bundle(resources, bundle_type="searchset"):
    """
    Create a FHIR Bundle containing multiple resources
    
    Args:
        resources: List of FHIR resources to include in the bundle
        bundle_type: Type of bundle (e.g. 'searchset', 'collection')
    
    Returns:
        A FHIR Bundle resource
    """
    entries = []
    
    for resource in resources:
        # Get the resource type (Patient, Practitioner, etc.)
        resource_type = resource.get_resource_type()
        
        # Create an entry for this resource
        entry = {
            "fullUrl": f"{resource_type}/{resource.id}",
            "resource": resource,
        }
        
        entries.append(entry)
    
    # Create the bundle
    bundle = Bundle(
        type=bundle_type,
        entry=entries,
        total=len(entries)
    )
    
    return bundle