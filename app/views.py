import io
from django.db import connection
from django.db.models import Max, Min, Avg
from django.http import JsonResponse
import sqlite3
from django.conf import settings
import pandas as pd
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer,DataSeializer
from django.forms.models import model_to_dict

import re

from .models import CustomUser,CSVFile

@api_view(['POST'])
@permission_classes([])
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
@permission_classes([])
def user_login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        user = None
        if '@' in username:
            try:
                user = CustomUser.objects.get(email=username)
            except ObjectDoesNotExist:
                pass

        if not user:
            user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_csv(request):
    if request.method == 'POST':
        csv_url = request.data.get('csv_url')  # Use request.data to get POST data in DRF

        try:
            # Extract Google Sheets key and generate the new URL for downloading as Excel
            pattern = r"^https://docs\.google\.com/spreadsheets/d/([^/?#]+)"
            match = re.match(pattern, csv_url)
            if not match:
                return Response({'error': 'Invalid Google Sheets URL'}, status=400)
            gsheet_key = match.group(1)
            new_url = f'https://docs.google.com/spreadsheet/ccc?key={gsheet_key}&output=xlsx'

            # Read the Excel file into a Pandas DataFrame
            header_names = ['id','AppID','Name','Release_date','Required_age','Price','DLC_count','About_the_game','Supported_languages', 'Windows', 'Mac', 'Linux', 'Positive', 'Negative', 'Score_rank', 'Developers', 'Publishers', 'Categories', 'Genres', 'Tags']
            df = pd.read_excel(new_url,header=0,names = header_names)

            #df.columns = ['id'] + list(df.columns[1:]) 
            
            # Clean column names (remove leading and trailing whitespace)
            df.columns = df.columns.str.strip()


            db_path = settings.DATABASES['default']['NAME']
            conn = sqlite3.connect(db_path)


            # Save DataFrame to SQLite using df.to_sql()
            df.to_sql(CSVFile._meta.db_table, con=conn, if_exists='replace', index=False)

            conn.close()

            return Response({'message': 'CSV data saved successfully to SQLite'})
        except Exception as e:
            return Response({'error': str(e)}, status=400)

    return Response({'error': 'POST method required'}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_data(request):
    try:
        # Extract query parameters from the request
        filters = {}
        aggregates = {}

        # Extract query type from request
        query_type = request.query_params.get('query_type')

        # Iterate through all query parameters
        for key, value in request.query_params.items():
            if key == 'query_type':
                continue  # Skip the query_type parameter

            # Handle numerical and date columns for exact match
            if query_type == 'exact' and key in ['AppID', 'Release_date', 'Required_age', 'Price', 'DLC_count', 'Windows', 'Mac', 'Linux', 'Positive', 'Negative', 'Score_rank']:
                filters[key] = value

            # Handle string fields for substring match
            elif query_type == 'string' and key in ['Name', 'About_the_game', 'Supported_languages', 'Developers', 'Publishers', 'Categories', 'Genres', 'Tags']:
                filters[key + '__contains'] = value

            # Handle date columns for greater than or less than
            elif query_type in ['greaterthan', 'lessthan'] and key == 'Release_date':
                if query_type == 'greaterthan':
                    filters[key + '__gt'] = value
                elif query_type == 'lessthan':
                    filters[key + '__lt'] = value

            # Handle aggregate queries for numerical columns
            elif query_type == 'aggregate' and key in ['max', 'min', 'mean', 'avg']:
                column = value
                if key == 'max':
                    aggregates = {'max_' + column: Max(column)}
                elif key == 'min':
                    aggregates = {'min_' + column: Min(column)}
                elif key == 'mean' or 'avg':
                    aggregates = {'avg_' + column: Avg(column)}

        # Perform the query with filters
        csv_data = CSVFile.objects.filter(**filters)

        # Handle aggregate queries if requested
        if aggregates:
            aggregate_results = csv_data.aggregate(**aggregates)
            if isinstance(aggregate_results, dict):
                aggregate_results = [aggregate_results]
            return Response(aggregate_results, status=200)

        # Serialize and return data
        serializer = DataSeializer(csv_data, many=True)
        return Response(serializer.data, status=200)

    except Exception as e:
        return Response({'error': str(e)}, status=400)