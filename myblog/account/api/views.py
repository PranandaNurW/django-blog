from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import authenticate

from rest_framework.authtoken.models import Token
from account.api.serializers import RegistrationSerializer, AccountPropertiesSerializer
from account.models import Account

#CREATE USER & TOKEN
@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def registration_view(request):
	if request.method == 'POST':
		data = {}
		serializer = RegistrationSerializer(data=request.data)
		
		if serializer.is_valid():
			account = serializer.save()
			data['response'] = 'successfully registered new user.'
			data['email'] = account.email
			data['username'] = account.username
			data['pk'] = account.pk
		else:
			data = serializer.errors
		return Response(data)

#GET PROFILE ACCOUNT
@api_view(['GET',])
@permission_classes([IsAuthenticated,])
def account_properties_view(request):
    try:
        account = request.user
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = AccountPropertiesSerializer(account)
        return Response(serializer.data)

#UPDATE EMAIL & USERNAME
@api_view(['PUT',])
@permission_classes([IsAuthenticated,])
def update_account_view(request):
    try:
        account = request.user
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        serializer = AccountPropertiesSerializer(account, data=request.data)
        data = {}

        if serializer.is_valid():
            serializer.save()
            data['response'] = "Successfully update an account"
            return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#LOGIN & CREATE TOKEN IF DOESNT EXIST
class ObtainAuthTokenView(APIView):

	authentication_classes = []
	permission_classes = []

	def post(self, request):
		context = {}

		email = request.POST.get('email')
		password = request.POST.get('password')
		account = authenticate(email=email, password=password)
		if account:
			try:
				token = Token.objects.get(user=account)
			except Token.DoesNotExist:
				token = Token.objects.create(user=account)
			context['response'] = 'Successfully authenticated.'
			context['pk'] = account.pk
			context['email'] = email
			context['token'] = token.key
		else:
			context['response'] = 'Error'
			context['error_message'] = 'Invalid credentials'

		return Response(context)