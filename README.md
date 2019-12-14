Darti Backend (WIP)
======
### Demos
- [Backend](https://backend-darti.apps.ca-central-1.starter.openshift-online.com/) ([repo](https://github.com/nemesiscodex/darti-backend))
    - Basic crud with test data + pagination
- [Frontend](https://frontend-darti.apps.ca-central-1.starter.openshift-online.com/) ([repo](https://github.com/nemesiscodex/darti-frontend))
    - Charts + Sensor List/Create
### Usage
Install postgres and redis or run them locally docker/docker-compose:
```bash
docker-compose -d postgres redis
```
- Postgres and Redis configurations are in `aep/settings.py`
- DB migration files are in `aep/migrations/`

Install dependencies (on Ubuntu):
```
sudo apt-get update && sudo apt-get install -y build-essential libpq-dev
```
Python dependencies:
```bash
virtualenv -p /usr/bin/python3.7 venv
source ./venv/bin/activate
pip install -r requirements.txt
```
Run app:
```
python -m aep.app
```
The backend will be available at http://localhost:8888/

To run tests:
```
pytest
```

### Architecture
<img src="https://user-images.githubusercontent.com/3976562/70764552-a6acbf80-1d36-11ea-907a-626d017cd5de.png" width="300" alt="architecture">

#### Backend stack
- Python 3.7
- PostgreSQL 11 + PostGIS
- Redis 5
- aiohttp
- asyncpg
- aioredis

#### Basic data model
<img src="https://user-images.githubusercontent.com/3976562/70762245-af00fc80-1d2e-11ea-8b59-6a18d3bffe6d.png" alt="Data model" width="300" />

- **Area**: A named area in a map. A polygon defined by a list of points with GPS coordinates.
- **Sensor**: Sensor with a type, an identifier and GPS coordinates.
- **Activation**: It represents the activation count of a Sensor in a specific reading instance.
- **Reading**: A reading represents the state of the sensor network in a specific moment in time. It also contains weather information, the system status and GPS coordinates.

#### Roadmap
- [ ] User Authentication + Roles and permissions.
- [ ] PostGIS integration for `Area` polygons in crud + query sensors by Area. 
- [ ] Better pagination.
- [ ] Improve filtering for reports.
    - [ ] Activations by Sensor per month/day and Area
    - [ ] Aggregate Activations per month/day and Area
    - [ ] Aggregate weather info per month/day and Area
- [ ] API Docs (swagger?).
- [ ] Improve caching mechanism.
- [ ] Database migration tool that doesn't use `psycopg2`

## About the project
### Chagas Disease
In Paraguay, as well as in other Latin American countries, [Chagas disease](https://en.wikipedia.org/wiki/Chagas_disease)
is one of the pressing issues in the area of public health.

This disease is caused by the parasite [Trypanosoma cruzi](https://en.wikipedia.org/wiki/Trypanosoma_cruzi), being [Triatoma infestans](https://en.wikipedia.org/wiki/Triatoma_infestans) insect or commonly called vinchuca (kissing bug), the main vector of South America.

Currently, there is a concern in European countries and on the United States, due to the growing eco-tourism to South American countries, where Chagas disease is referred to as an "exotic disease".
Prevention mostly involves eliminating kissing bugs and avoiding their bites. **A vaccine has not been developed as of 2019**.

Treatment options for infected patients are limited.
Early infections are treatable with the medication if given early, but becomes less effective the longer a person has had Chagas disease.

Most people with the disease live in poverty, and do not realize they are infected. 

#### Eradication of Chagas Disease with Technology
> A project in conjunction with the [Center for the Development of Scientific Research (CEDIC)](https://www.cedicpy.com/) and the [Polytechnic School of the National University of Asunción](http://www.fpuna.edu.py/).  

The monitoring of the vector transmitting Chagas disease will be possible through the implementation of a wireless infrared photoelectric sensor network for remote early detection of kissing bugs infestation in a surveillance zone.
Readings of the sensor network will be sent from a ground station to the research lab located in the Polytechnic School using a [satellite](https://birds4.birds-project.com/).
