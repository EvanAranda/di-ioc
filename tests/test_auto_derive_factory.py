from typing import Optional

from di_ioc import ServiceContainer, scoped, auto


class Dep1:
    pass


class Dep2:
    pass


class Service:
    def __init__(self, dep1: Dep1, dep2: Optional[Dep2]):
        self.dep1 = dep1
        self.dep2 = dep2

    @staticmethod
    def create_optional(dep1: Dep1, dep2: Optional[Dep2]) -> 'Service':
        return Service(dep1, dep2)

    @staticmethod
    def create_default(dep1: Dep1, dep2: Dep2 = None) -> 'Service':
        return Service(dep1, dep2)


def test_derive():
    container = ServiceContainer()
    container[Dep1] = auto(Dep1)
    container[Dep2] = auto(Dep2)
    container[Service] = auto(Service)
    service = container.get_service(Service)
    assert service.dep1 is not None
    assert service.dep2 is not None


def test_derive_optional_deps():
    container = ServiceContainer()
    container[Dep1] = auto(Dep1)
    container[Service] = auto(Service.create_optional)
    container.get_service(Service)
    service = container.get_service(Service)
    assert service.dep1 is not None
    assert service.dep2 is None


def test_derive_default_deps():
    container = ServiceContainer()
    container[Dep1] = auto(Dep1)
    container[Service] = auto(Service.create_default, lifetime=scoped)
    service = container.get_service(Service)
    assert service.dep1 is not None
    assert service.dep2 is None
