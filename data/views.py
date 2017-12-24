# from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated

from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

# from data.permissions import IsOwnerOrReadOnly
from data.models import User, Blog
from data.serializers import UserRegisterSerializer, UserSerializer, BlogSerializer
from django.http import HttpResponseRedirect
from handler.ap_kpi import ApKpi


class UserRegisterAPIView(APIView):
    """
    用于测试自己实现的用户注册
    """
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny, )

    def post(self, request, format=None):
        data = request.data
        username = data.get('username')
        if User.objects.filter(username__exact=username):
            return Response("用户名已存在", HTTP_400_BAD_REQUEST)
        serializer = UserRegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            print(serializer.validated_data)
            serializer.save()
            return Response(serializer.validated_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    """
    用于测试自己实现的用户登入
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )

    def post(self, request, format=None):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        user = User.objects.get(username__exact=username)
        if user.password == password:
            serializer = UserSerializer(user)
            new_data = serializer.data
            # 记忆已登录用户
            self.request.session['user_id'] = user.id
            return Response(new_data, status=HTTP_200_OK)
        return Response('password error', HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        return HttpResponseRedirect('http://127.0.0.1:8083/')  # 跳转到index界面


class ApKpiAPIView(APIView):
    """
    处理apkpi数据
    """
    permission_classes = (AllowAny, )

    def get(self, request, format=None):
        path = request.GET.get('path')
        out_contents = list()
        ap = ApKpi()
        ap.pre_process(path, out_contents)
        contents = "<html><body>"
        for content in out_contents:
            contents = contents + content
        contents = contents + "</body></html>"
        return HttpResponse(contents)

    def post(self, request, format=None):
        data = request.data
        path = data.get('path')
        header = {'Access-Control-Allow-Origin': '*'}
        if path == "undefined":
            return Response("error", status=HTTP_200_OK, headers=header)
        out_contents = list()
        ap = ApKpi()
        file_path = ap.pre_process(path, out_contents)
        contents = str()
        for content in out_contents:
            contents = contents + content
        print(file_path)
        return Response(file_path, status=HTTP_200_OK, headers=header)


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    # permission_classes = (IsOwnerOrReadOnly, )
    permission_classes = (AllowAny, )

    def perform_create(self, serializer):
        serializer.save(
            owner=User.objects.get(id=self.request.session.get('user_id')))


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
