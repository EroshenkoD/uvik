import pytest
from django.db.models import QuerySet
from mixer.backend.django import mixer
from django.test import Client
from order_project.models import Order


pytestmark = pytest.mark.django_db


@pytest.fixture
def order_project():
    return mixer.blend('order_project.Order', phone_customer='99999999', email_customer='test_order@ukr.net',
                       type_website=mixer.sequence(*[choice[0] for choice in Order.LIST_WEBSITE]))


class TestOrderView:
    endpoint = '/order_project/'
    client = Client()

    @staticmethod
    def _common_check(response, expected_status=200, expected_content_type="text/html; charset=utf-8") -> None:
        assert response.get("content-type") == expected_content_type,\
            f"Unexpected content-type {response.get('content-type')}"
        assert response.status_code == expected_status, f"Unexpected status code: {response.status_code}"

    def test_creates_order_project(self, order_project: QuerySet[Order]) -> None:
        # given
        data = {
            'name_customer': order_project.name_customer,
            'phone_customer': order_project.phone_customer,
            'email_customer': order_project.email_customer,
            'title': order_project.title,
            'body': order_project.body,
            'type_website': order_project.type_website,
        }
        # when
        response = self.client.post(self.endpoint, data=data)
        # then
        self._common_check(response)
        assert Order.objects.count() == 1, 'There should be only one order project created'



