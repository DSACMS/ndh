from fhir.resources.practitioner import Practitioner as FHIRPractitioner
from fhir.resources.humanname import HumanName
from fhir.resources.identifier import Identifier
from fhir.resources.contactpoint import ContactPoint
from .utils import SmartyStreetstoFHIR
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.period import Period
from fhir.resources.meta import Meta

def create_fhir_practitioner(provider):
    """Convert an Individual model to a FHIR Practitioner resource"""

    individual=provider.individual
    # Create FHIR Practitioner
    fhir_practitioner = FHIRPractitioner()
    
    # Set ID
    fhir_practitioner.id = str(provider.npi.npi)
    
    # Set meta
    fhir_practitioner.meta = Meta(
        profile=["http://hl7.org/fhir/us/core/StructureDefinition/us-core-practitioner"]
    )
    
    # Set identifiers
    identifiers = []
    
    # Doctor ID identifier
    doctor_identifier = Identifier(
        system="http://terminology.hl7.org/NamingSystem/npi",
        value=str(provider.npi.npi),
        type=CodeableConcept(
                coding=[Coding(
                    system="http://terminology.hl7.org/CodeSystem/v2-0203",
                    code="PRN",
                    display="Provider number"
                )]
            ),
        use='official',
        period=Period(
            start=provider.npi.enumeration_date,
            end=provider.npi.deactivation_date
    )
    )
    identifiers.append(doctor_identifier)

    for id in individual.individualtootheridentifier_set.all():
        license_identifier = Identifier(
            #system="", TODO: Figure out how to associate a system with each identifier
            value=id.value,
            type=CodeableConcept(
                coding=[Coding(
                    system="http://terminology.hl7.org/CodeSystem/v2-0203",
                    code=id.otherIdentifierType.id,
                    display=id.otherIdentifierType.value
                )]
            ),
            #use="" TODO: Add use for other identifier
            period=Period(
                start=id.issue_date,
                end=id.expiry_date
        )
        )
        identifiers.append(license_identifier)
    
    fhir_practitioner.identifier = identifiers

    names=[]
    
    for name in individual.individualtoname_set.all():
        human_name = HumanName(
            family=name.last_name,
            given=[name.first_name, name.middle_name],
            use=name.fhir_name_type.value,
            period=Period(
                start=name.effective_date,
                end=name.end_date
            )
        )
        if name.prefix!='':
            human_name.prefix = [name.prefix]
        if name.suffix!='':
            human_name.suffix = [name.suffix]
        names.append(human_name)
    fhir_practitioner.name = names
    fhir_practitioner.gender=individual.gender_code
    
    # Set contact (email and phone)
    contacts = []
    for email in individual.individualtoemailaddress_set.all():
        email_contact = ContactPoint(
            system="email",
            value=email.email_address,
            #use="work" TODO: add email use
        )
        contacts.append(email_contact)
    
    for phone in individual.individualtophonenumber_set.all():
        phone_contact = ContactPoint(
            system=phone.phone_type.value,
            value=f"{phone.phone_number.value} ext. {phone.extension}",
            #use="work" TODO: add phone use
        )
        contacts.append(phone_contact)
    
    if contacts:
        fhir_practitioner.telecom = contacts
    
    # Set address
    for address in individual.individualtoaddress_set.all():
        practitioner_address=SmartyStreetstoFHIR(address)
        fhir_practitioner.address = [practitioner_address]
    
    # Set qualification (specialty, education)
    qualifications = []
    
    # Add specialty as qualification
    for taxonomy in individual.individualtonucctaxonomycode_set.all():
        specialty_qualification = dict(
            code=CodeableConcept(
                coding=[Coding(
                    system="http://nucc.org/provider-taxonomy",
                    code=taxonomy.nucc_taxonomy_code_id,
                    display=taxonomy.nucc_taxonomy_code.display_name
                )]
            )
        )
        qualifications.append(specialty_qualification)
    
    if qualifications:
        fhir_practitioner.qualification = qualifications
    
    
    
    return fhir_practitioner