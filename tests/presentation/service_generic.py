from asyncio import Future

import pytest


async def generic_test_get(mocker, fake, service_class):
    expected = fake(1)
    repository = mocker.Mock()
    f = Future()
    f.set_result(expected)
    repository.get = mocker.MagicMock(return_value=f)
    service = service_class(repository)
    result = await service.get(1)
    assert result == expected
    repository.get.assert_called_once_with(1)


async def generic_test_all(mocker, fake, service_class):
    expected = [fake(1), fake(2)]
    repository = mocker.Mock()
    f = Future()
    f.set_result(expected)
    repository.all = mocker.MagicMock(return_value=f)
    service = service_class(repository)
    result = await service.all(1, 100)
    assert result == expected
    repository.all.assert_called_once_with(1, 100)
    repository.all.reset_data()
    result = await service.all(None, None)
    assert result == expected
    repository.all.assert_called_with(0, 100)


async def generic_test_create(mocker, fake, service_class):
    model = fake(-1)
    repository = mocker.Mock()
    f = Future()
    f.set_result(None)
    repository.create = mocker.MagicMock(return_value=f)
    service = service_class(repository)
    await service.create(model)
    repository.create.assert_called_once_with(model)


async def generic_test_update(mocker, fake, service_class):
    model = fake(1)
    repository = mocker.Mock()
    f = Future()
    f.set_result(None)
    repository.update = mocker.MagicMock(return_value=f)
    service = service_class(repository)
    await service.update(model)
    repository.update.assert_called_once_with(model)

    model = fake(None)
    with pytest.raises(AssertionError):
        await service.update(model)
    repository.update.assert_called_once()

    model = fake(-1)
    with pytest.raises(AssertionError):
        await service.update(model)
    repository.update.assert_called_once()


async def generic_test_delete(mocker, service_class):
    repository = mocker.Mock()
    identifier = 1
    f = Future()
    f.set_result(None)
    repository.delete = mocker.MagicMock(return_value=f)
    service = service_class(repository)
    await service.delete(identifier)
    repository.delete.assert_called_once_with(identifier)
