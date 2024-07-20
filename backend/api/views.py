from eurostatapiclient import EurostatAPIClient
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

VERSION = '1.0'
FORMAT = 'json'
LANGUAGE = 'en'

client = EurostatAPIClient(VERSION, FORMAT, LANGUAGE)

class EurostatDataView(APIView):
    def get(self, request, dataset_id):
        try:
            # Fetching data from Eurostat
            response = client.get_dataset(dataset_id)
            data = response.get('value', [])
            
            return Response(data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)