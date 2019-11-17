from presentation.services import AreaService

# Area
from tests.presentation.service_generic import *
from tests.util.fake import fake_area


@pytest.mark.asyncio
async def test_area_service_get(mocker):
    await generic_test_get(mocker, fake_area, AreaService)


@pytest.mark.asyncio
async def test_area_service_all(mocker):
    await generic_test_all(mocker, fake_area, AreaService)


@pytest.mark.asyncio
async def test_area_service_create(mocker):
    await generic_test_create(mocker, fake_area, AreaService)


@pytest.mark.asyncio
async def test_area_service_update(mocker):
    await generic_test_update(mocker, fake_area, AreaService)


@pytest.mark.asyncio
async def test_area_service_delete(mocker):
    await generic_test_delete(mocker, AreaService)
