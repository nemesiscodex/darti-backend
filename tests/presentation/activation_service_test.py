from presentation.services import ActivationService

# Area
from tests.presentation.service_generic import *
from tests.util.fake import fake_activation


@pytest.mark.asyncio
async def test_activation_service_get(mocker):
    await generic_test_get(mocker, fake_activation, ActivationService)


@pytest.mark.asyncio
async def test_activation_service_all(mocker):
    await generic_test_all(mocker, fake_activation, ActivationService)


@pytest.mark.asyncio
async def test_activation_service_create(mocker):
    await generic_test_create(mocker, fake_activation, ActivationService)


@pytest.mark.asyncio
async def test_activation_service_update(mocker):
    await generic_test_update(mocker, fake_activation, ActivationService)


@pytest.mark.asyncio
async def test_activation_service_delete(mocker):
    await generic_test_delete(mocker, ActivationService)
