import logging
from django.views import generic

from .models import Project


logger_file = logging.getLogger('file')
logger_console = logging.getLogger('console')


class IndexView(generic.ListView):
    logger_console.info('Test IndexView')
    template_name = 'projects/index.html'
    context_object_name = 'projects'

    def get_queryset(self):
        logger_file.warning('Test get_queryset')
        return Project.objects.all()


class DetailView(generic.DetailView):
    logger_console.info('Test DetailView')
    model = Project
    context_object_name = 'project'
    template_name = 'projects/detail.html'



