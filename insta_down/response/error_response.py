from django.http import JsonResponse

BAD_REQUEST = JsonResponse(data={'message': 'Bad request'})

METHOD_NOT_ALLoW = JsonResponse(data={"message": "Method not allow"}, status=405)

MUST_HAVE_URL = JsonResponse(data={'message': 'must have url'},
                             content_type='application/json', status=400)

VALIDATE_ERROR = JsonResponse(data={'message': 'Request data error'})
