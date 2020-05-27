from django.http import JsonResponse

BAD_REQUEST = JsonResponse(data={'message': 'Bad request'}, status=400)

METHOD_NOT_ALLoW = JsonResponse(data={"message": "Method not allow"}, status=405)

MUST_HAVE_URL = JsonResponse(data={'message': 'must have url'}, status=400)

VALIDATE_ERROR = JsonResponse(data={'message': 'Request data error'}, status=400)

NOT_FOUND = JsonResponse(data={'message': 'Data request not found'}, status=404)
