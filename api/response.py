from rest_framework.response import Response

def response(status: int, message: str, data: list = []) -> dict:
  return Response({
    "status": status,
    "message": message,
    "data": data
  }, status)