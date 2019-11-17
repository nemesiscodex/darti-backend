from dependency_injector import containers, providers

from aep.data.datasources import AreaDatasource, SensorDatasource, ReadingDatasource, ActivationDatasource
from aep.data.repositories import AreaRepository, SensorRepository, ReadingRepository, ActivationRepository
from aep.presentation.services import AreaService, SensorService, ReadingService, ActivationService


class Datasources(containers.DeclarativeContainer):
    area = providers.Factory(AreaDatasource)
    sensor = providers.Factory(SensorDatasource)
    reading = providers.Factory(ReadingDatasource)
    activation = providers.Factory(ActivationDatasource)


class Repositories(containers.DeclarativeContainer):
    area = providers.Factory(AreaRepository, Datasources.area)
    sensor = providers.Factory(SensorRepository, Datasources.sensor)
    reading = providers.Factory(ReadingRepository, Datasources.reading)
    activation = providers.Factory(ActivationRepository, Datasources.activation)


class Services(containers.DeclarativeContainer):
    area = providers.Factory(AreaService, Repositories.area)
    sensor = providers.Factory(SensorService, Repositories.sensor)
    reading = providers.Factory(ReadingService, Repositories.reading)
    activation = providers.Factory(ActivationService, Repositories.activation)
