# -*- coding: utf-8 -*-
# author: itimor

from rest_framework import viewsets
from jobs.models import Jobs, Deployenv, DeployJobs
from jobs.serializers import JobsSerializer, DeployenvSerializer, DeployJobsSerializer
from rest_framework.response import Response
from rest_framework import status
from omsBackend.settings import sapi
from jobs.filters import JobFilterBackend


class JobsViewSet(viewsets.ModelViewSet):
    queryset = Jobs.objects.all()
    serializer_class = JobsSerializer
    filter_backends = (JobFilterBackend,)


class DeployenvViewSet(viewsets.ModelViewSet):
    queryset = Deployenv.objects.all()
    serializer_class = DeployenvSerializer
    filter_fields = ['job__name']


class DeployJobsViewSet(viewsets.ModelViewSet):
    queryset = DeployJobs.objects.all().order_by('-create_time')
    serializer_class = DeployJobsSerializer
    filter_fields = ['job__name']

    def list(self, request, *args, **kwargs):
        job_name = request.GET['job__name']
        works = DeployJobs.objects.all().filter(job__name=job_name).filter(deploy_status='deploy')
        deploy_serializer = DeployJobsSerializer(works, many=True, context={'request': request})
        for work in deploy_serializer.data:
            j_id = work['j_id']
            j = DeployJobs.objects.get(j_id=j_id)
            job_status = sapi.check_job(j_id)
            print(job_status)

            if list(set(job_status.values()))[0]:
                    j.result = sapi.get_result(j_id)
                    j.deploy_status = 'success'
                    import re
                    jdata = list(j.result.values())[0]
                    j.version = re.findall('At revision (\d+)', jdata)[0]
            else:
                j.deploy_status = 'deploy'

            j.save()
        queryset = DeployJobs.objects.all().filter(job__name=job_name).order_by('-create_time')
        serializer = DeployJobsSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
