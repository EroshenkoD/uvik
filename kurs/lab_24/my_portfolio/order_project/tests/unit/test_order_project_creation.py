import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from mixer.backend.django import mixer

from order_project.models import Order

pytestmark = pytest.mark.django_db


def test_order_project_creation():
    # given/when
    order_project = mixer.blend('order_project.Order')
    # then
    assert Order.objects.count() == 1, 'There should be only one order project created'
    assert Order.objects.first().id == order_project.id, f'Order project id expected to be {order_project.id}'


def test_order_project_creation_unique_email():
    # given
    email = 'test@ukr.net'
    mixer.blend('order_project.Order', email_customer=email)
    # when
    try:
        mixer.blend('order_project.Order', email_customer=email)
    except IntegrityError as e:
        # then
        assert str(e) == 'Mixer (order_project.Order): UNIQUE constraint failed: order_project_order.email_customer', \
            f"Unexpected message, {e}"
    else:
        raise Exception("Unexpected message, field 'email_customer' must be call IntegrityError")


def test_order_project_creation_unique_phone():
    # given
    phone = '123456789'
    mixer.blend('order_project.Order', phone_customer=phone)
    # when
    try:
        mixer.blend('order_project.Order', phone_customer=phone)
    except IntegrityError as e:
        # then
        assert str(e) == 'Mixer (order_project.Order): UNIQUE constraint failed: order_project_order.phone_customer', \
            f"Unexpected message, {e}"
    else:
        raise Exception("Unexpected message, field 'phone_customer' must be call IntegrityError")


def test_order_project_creation_validate_phone():
    # given/when
    try:
        order_project = mixer.blend('order_project.Order', phone_customer='phone')
        order_project.clean_fields()
    except ValidationError as e:
        # then
        assert type(dict(e)) is dict, f"ValidationError must have convert to dict{e}"
        assert dict(e)['phone_customer'][0] == "Phone number must be entered in the format: '+XXXXXXXXXXXX'", \
            f"Unexpected message, {e}"
    else:
        raise Exception("Unexpected message, field 'phone_customer' must be call ValidationError")


def test_order_project_creation_title_is_not_none():
    # given/when
    try:
        mixer.blend('order_project.Order', title=None)
    except IntegrityError as e:
        # then
        assert str(e) == 'Mixer (order_project.Order): NOT NULL constraint failed: order_project_order.title', \
            f"Unexpected message, {e}"
    else:
        raise Exception("Unexpected message, field 'title' must be call IntegrityError")
