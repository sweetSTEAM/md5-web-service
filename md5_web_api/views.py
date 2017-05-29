from rest_framework.response import Response
from rest_framework.decorators import api_view
from celery.result import AsyncResult
from celery.states import EXCEPTION_STATES
from .md5core import url_is_valid
from .tasks import get_md5_task
from django.core.cache import cache

@api_view(['POST'])
def post_link(request):
    """
    Start processing a link
    """
    data = request.data
    # Simple validation of the url without connection
    if 'url' not in data or not url_is_valid(data['url']):
        return Response({'message': 'Invalid link'}, status=400)

    # Running the background task and returning id
    res = get_md5_task.delay(url=data['url'])
    # need to save id in cache in case task is valid and just PENDING
    # there is probably better solution in celery, but haven't found one yet
    cache.set(res.id, '1', 24*60*60)
    return Response({'guid': res.id}, status=202)


@api_view(['GET'])
def get_status(request, guid):
    """
    Check the status of the request
    """
    task = AsyncResult(guid)
    if not cache.get(guid):
        status = 'FAILURE'
        info = 'UNKNOWN TASK ID'
        code = 404
    elif task.status == 'PENDING':
        status = 'PROGRESS'
        info = 'PENDING'
        code = 409
    elif task.status == 'PROGRESS':
        status = 'PROGRESS'
        info = task.info['PROGRESS']
        code = 409
    elif task.status == 'STARTED':
        status = 'STARTED'
        info = 'STARTED'
        code = 409
    elif task.status == 'SUCCESS':
        status = 'SUCCESS'
        info = task.result
        code = 200
    elif task.status in EXCEPTION_STATES:
        status = 'FAILURE'
        info = repr(task.info)
        code = 400
    else:
        status = 'FAILURE'
        info = task.status
        code = 400

    return Response({
        'guid': guid, 'state': status, 'info': info
    }, status=code)
