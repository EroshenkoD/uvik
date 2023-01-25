import pytest
from django.db.models import QuerySet
from mixer.backend.django import mixer
from django.test import Client
from projects.models import Project


pytestmark = pytest.mark.django_db


@pytest.fixture
def projects():
    return mixer.cycle(2).blend('projects.Project', path="projects/static/test.png",
                                technology=mixer.sequence(*[choice[0] for choice in Project.LIST_TECHNOLOGY]))


class TestProjectView:
    endpoint = '/projects/'
    client = Client()

    @staticmethod
    def _common_check(response, expected_status=200, expected_content_type="text/html; charset=utf-8") -> None:
        assert response.get("content-type") == expected_content_type,\
            f"Unexpected content-type {response.get('content-type')}"
        assert response.status_code == expected_status, f"Unexpected status code: {response.status_code}"

    @staticmethod
    def check_fields(project_data: dict) -> None:
        assert project_data._meta.get_field("title"), "Instance Project must have field 'title'"
        assert project_data._meta.get_field("description"), "Instance Project must have field 'description'"
        assert project_data._meta.get_field("technology"), "Instance Project must have field 'technology'"
        assert project_data._meta.get_field("image"), "Instance Project must have field 'image'"

    def test_admins_gets_snippets(self, projects: QuerySet[Project]) -> None:
        # given/when
        response = self.client.get(self.endpoint)
        # then
        self._common_check(response)
        assert isinstance(response.context, list), 'Response is expected to be list'
        assert len(response.context) != 0, 'Response should not be empty'
        assert isinstance(response.context[1]['projects'][0], Project), f'Response have to have instance Project'
        self.check_fields(response.context[1]['projects'][0])



