from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class DRFStatusView(APIView):
    permission_classes = [] 
    def get(self, request):
        return Response({"status": "DRF is enabled"}, status=status.HTTP_200_OK)
