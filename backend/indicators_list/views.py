from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
import os
import pandas as pd
import numpy as np


@api_view(["GET"])
def indicators_check_list(request):

    df = pd.read_excel("Indicators_InCITIES.xlsx", header=0, sheet_name='Indicators')
    
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df = df.where(pd.notnull(df), None)

    data = df.to_dict(orient='records')

    return Response(data)
