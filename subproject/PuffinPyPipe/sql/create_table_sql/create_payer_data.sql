-- SOURCED FROM Payer FHIR / JSON Data or from the PUFs/Google Searches etc.
-- I see no way to reduce these tables in a way that allows us make the change to a VTIN model,
-- while still ultimately being compatible with the data we are required to express as low-level (i.e. the strict parts)
-- of FHIR compliance. 

CREATE TABLE ndh.payer_interop_endpoint (
    id SERIAL PRIMARY KEY,
    payer_id int   NOT NULL,
    interop_endpoint_id int   NOT NULL
);

CREATE TABLE ndh.payer (
    -- marketplace/network-puf.IssuerID
    id SERIAL PRIMARY KEY,
    -- marketplace/plan-attributes-puf.IssuerMarketPlaceMarketingName
    payer_nme varchar   NOT NULL
);

-- There are a lot of atributes for plans, not sure how much we need to include
CREATE TABLE ndh.plan (
    -- marketplace/plan-attributes-puf.PlanId
    id SERIAL PRIMARY KEY,
    payer_id int   NOT NULL,
    marketcoverage_id int   NOT NULL,
    -- marketplace/plan-attributes-puf.ServiceAreaId
    service_area_id int   NOT NULL,
    -- marketplace/plan-attributes-puf.DentalOnlyPlan
    is_dental_only_lan boolean   NOT NULL,
    -- marketplace/plan-attributes-puf.PlanMarketingName
    plan_marketing_name varchar   NOT NULL,
    -- marketplace/plan-attributes-puf.HIOSProductId
    hios_product_id varchar   NOT NULL,
    plan_type_id int   NOT NULL,
    -- marketplace/plan-attributes-puf.IsNewPlan
    is_new_plan boolean   NOT NULL
);

CREATE TABLE ndh.plan_type (
    id SERIAL PRIMARY KEY,
    -- marketplace/plan-attributes-puf.PlanType
    plan_type_name varchar   NOT NULL
);

CREATE TABLE ndh.marketcoverage (
    id SERIAL PRIMARY KEY,
    -- marketplace/plan-attributes-puf.MarketCoverage
    marketcoverage_name varchar   NOT NULL
);

CREATE TABLE ndh.plan_network_plan (
    id SERIAL PRIMARY KEY,
    plan_id int   NOT NULL,
    plan_network_id int   NOT NULL
);

CREATE TABLE ndh.plan_network (
    -- marketplace/network-puf.NetworkID
    id SERIAL PRIMARY KEY,
    -- marketplace/network-puf.NetworkName
    plan_network_name varchar(100)   NOT NULL,
    -- marketplace/network-puf.NetworkURL
    plan_network_url varchar(500)   NOT NULL
);

-- TODO how does this relate to FIPS counties and the sub-counties concept from MA plans?
CREATE TABLE ndh.service_area (
    -- marketplace/plan-attributes-puf.ServiceAreaId
    id SERIAL PRIMARY KEY,
    -- marketplace/service-area-puf.ServiceAreaName
    service_area_name varchar   NOT NULL,
    -- marketplace/service-area-puf.StateCode
    state_code_id INT   NOT NULL
    -- wishlist
    -- , service_area_shape GEOMETRY(MULTIPOLYGON, 4326)   NOT NULL -- enable with PostGIS turned on! 
);

-- PECOS Sourced initially, then UX Maintained
CREATE TABLE ndh.plan_network_clinical_organization (
    id SERIAL PRIMARY KEY,
    plan_network_id int   NOT NULL,
    clinical_organization_id int   NOT NULL
);
