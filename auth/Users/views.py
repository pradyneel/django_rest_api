from django.http import response
from django.shortcuts import render, redirect
from Users.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.renderers import TemplateHTMLRenderer
from .models import User
import jwt, datetime



class SignUp(APIView):
    def post(self, request):
        if request.method == 'POST':
            serializer = UserSerializer(data = request.data)
            serializer.is_valid(raise_exception = True)
            serializer.save()
            return Response(serializer.data)
    def get(self, request):
        return render(request, 'Users/signup.html', {})

class Login(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        payload = {
            'id': user.id, #user id
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5), #expiration of token
            'iat': datetime.datetime.utcnow() #date the token created
        }

        token = jwt.encode(payload, 'secretkey', algorithm = 'HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return redirect('/api/user')
    
    def get(self, request):
        return render(request, 'Users/login.html', {})
    
    

class UserView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'Users/Users.html'
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('UnAuthenticated!')

        try:
            payload = jwt.decode(token, 'secretkey', algorithms = ['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('UnAuthenticated!')

        user = User.objects.all()
        serializer = UserSerializer(user, many= True)


        return Response({'serializer':serializer.data, 'users':user})

class LogoutView(APIView):
    def get(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return redirect('/api/login')


class DeleteView(APIView):
    def get(self, request, pk):
        response = User.objects.get(id = pk)
        response.delete()
        return redirect('/api/user')

class UpdateView(APIView):
    def post(self, request, pk):
        response = User.objects.get(id=pk)
        serializer = UserSerializer(instance = response, data=request.data, partial= True)

        if serializer.is_valid():
            serializer.save()
        else:
            return Response("Error")
        return redirect('/api/user')

    def get(self, request, pk):
        return render(request, 'Users/update.html', {'id':id})     