from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import MsgInfo, UserInfo, UserMsgIndex
from django.http import JsonResponse


def del_msg(request):
    pass


