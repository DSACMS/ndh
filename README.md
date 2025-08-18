# NDH

National Provider Directory at CMS

## About the Project

The soon to be renamed NDH project at CMS will implement a new Provider and Payer Directory service that will eventually grow to encompass (and probably replace) the functionality of NPPES.

### Project Vision
Enable patient data to work for patients, by supporting interoperability by providing clean enumeration of U.S. healthcare entities, and a reliable map of how those entities connect. 

<!--
### Project Mission
**{project mission}** -->


### Agency Mission
The Centers for Medicare and Medicaid Services (CMS) provides health coverage to more than 100 million people through Medicare, Medicaid, the Children’s Health Insurance Program, and the Health Insurance Marketplace. The CMS seeks to strengthen and modernize the Nation’s health care system, to provide access to high quality care and improved health at lower costs.

<!--
### Team Mission
TODO: Good to include since this is an agency-led project -->

## Core Team

A list of core team members responsible for the code and documentation in this repository can be found in [COMMUNITY.md](COMMUNITY.md).

## Repository Structure

This is a mega-repository that will contain sub-directories for each component of National Provider Directory. You will find more information about each component in a README.md file within its respective directory. 

### db/
The `db/` directory contains sql code for the National Provider Directory database. The `db/sql/schemas/` sub-directory contains the code necessary to create each schema in the db. The `db/tinman_SQL_schema_standard` directory contains the project's sql naming conventions and guidelines.

### etls/
The `etls/` directory contains the pipelines that extract, transform, and load (ETL) data into the database. Each sub-directory in the `etls/` directory represents a different input data source.

### src/
The `src/` directory contains the backend python code for the National Provider Directory APIs (built on Django). The `src/ndhfhir/` subdirectory contains the code for the FHIR API. 


# Development and Software Delivery Lifecycle

The following guide is for members of the project team who have access to the repository as well as code contributors. The main difference between internal and external contributions is that external contributors will need to fork the project and will not be able to merge their own pull requests. For more information on contributing, see: [CONTRIBUTING.md](./CONTRIBUTING.md).

## Local Development

### Database Setup
1. Create a local postgres server
2. Create a database called ndh
3. Execute the sql in `db/sql/schemas/ndh.sql` to create the ndh schema and associated tables
4. Create a `.env` file in the `src/` directory, following the template provided in `src/.env_template`, ensuring that the connection details reflect your database connection
5. Navigate to the `src/` directory. Run `python manage.py loaddata ndh.json` to load a sample of data into the database

### Django App Setup
1. Ensure that either colima (if using macOS) or the docker service is running
2. Run `docker-compose up --build` initially and following any changes
3. Navigate to `http://localhost:8000` to view your changes.
4. Happy coding!

## Coding Style and Linters

<!-- TODO - Add the repo's linting and code style guidelines -->

Each sub-directory has its own linting and testing guidelines. Lint and code tests are run on each commit, so linters and tests should be run locally before committing.

## Branching Model

This project follows [trunk-based development](https://trunkbaseddevelopment.com/), which means:

* Make small changes in [short-lived feature branches](https://trunkbaseddevelopment.com/short-lived-feature-branches/) and merge to `main` frequently.
* Be open to submitting multiple small pull requests for a single ticket (i.e. reference the same ticket across multiple pull requests).
* Treat each change you merge to `main` as immediately deployable to production. Do not merge changes that depend on subsequent changes you plan to make, even if you plan to make those changes shortly.
* Ticket any unfinished or partially finished work.
* Tests should be written for changes introduced, and adhere to the text percentage threshold determined by the project.

This project uses **continuous deployment** using [Github Actions](https://github.com/features/actions) which is configured in the [./github/workflows](.github/workflows) directory.

Pull-requests are merged to `main` and the changes are immediately deployed to the development environment. Releases are created to push changes to production.

## Contributing

Thank you for considering contributing to an Open Source project of the US Government! For more information about our contribution guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md).

## Community

The NDH team is taking a community-first and open source approach to the product development of this tool. We believe government software should be made in the open and be built and licensed such that anyone can download the code, run it themselves without paying money to third parties or using proprietary software, and use it as they will.

We know that we can learn from a wide variety of communities, including those who will use or will be impacted by the tool, who are experts in technology, or who have experience with similar technologies deployed in other spaces. We are dedicated to creating forums for continuous conversation and feedback to help shape the design and development of the tool.

We also recognize capacity building as a key part of involving a diverse open source community. We are doing our best to use accessible language, provide technical and process documents, and offer support to community members with a wide variety of backgrounds and skillsets.

### Community Guidelines

Principles and guidelines for participating in our open source community are can be found in [COMMUNITY.md](COMMUNITY.md). Please read them before joining or starting a conversation in this repo or one of the channels listed below. All community members and participants are expected to adhere to the community guidelines and code of conduct when participating in community spaces including: code repositories, communication channels and venues, and events.


## Governance
Information about how the NDH community is governed may be found in [GOVERNANCE.md](GOVERNANCE.md).


## Feedback

If you have ideas for how we can improve or add to our capacity building efforts and methods for welcoming people into our community, please let us know at **opensource@cms.hhs.gov**. If you would like to comment on the tool itself, please let us know by filing an **issue on our GitHub repository.**

<!--
## Glossary
Information about terminology and acronyms used in this documentation may be found in [GLOSSARY.md](GLOSSARY.md).
-->

## Policies

### Open Source Policy

We adhere to the [CMS Open Source
Policy](https://github.com/CMSGov/cms-open-source-policy). If you have any
questions, just [shoot us an email](mailto:opensource@cms.hhs.gov).

### Security and Responsible Disclosure Policy

_Submit a vulnerability:_ Vulnerability reports can be submitted through [Bugcrowd](https://bugcrowd.com/cms-vdp). Reports may be submitted anonymously. If you share contact information, we will acknowledge receipt of your report within 3 business days.

For more information about our Security, Vulnerability, and Responsible Disclosure Policies, see [SECURITY.md](SECURITY.md).

### Software Bill of Materials (SBOM)

A Software Bill of Materials (SBOM) is a formal record containing the details and supply chain relationships of various components used in building software.

In the spirit of [Executive Order 14028 - Improving the Nation’s Cyber Security](https://www.gsa.gov/technology/it-contract-vehicles-and-purchasing-programs/information-technology-category/it-security/executive-order-14028), a SBOM for this repository is provided here: https://github.com/DSACMS/ndh/network/dependencies.

For more information and resources about SBOMs, visit: https://www.cisa.gov/sbom.

## Public domain

This project is in the public domain within the United States, and copyright and related rights in the work worldwide are waived through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/) as indicated in [LICENSE](LICENSE).

All contributions to this project will be released under the CC0 dedication. By submitting a pull request or issue, you are agreeing to comply with this waiver of copyright interest.
