import hashlib
import uuid

import redis
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from dailyfresh import settings
from user_center.models import UserInfo


def send_verify_mail(username, mail_addr):
    """
    发送账户激活验证邮件
    :param username:  用户名
    :param mail_addr:  用户的邮箱地址
    :return:  没有返回的信息
    """
    token = uuid.uuid1().hex
    '''
    subject 邮件主题
    message 邮件内的文本信息
    from_email 邮件的发件邮箱地址
    recipient_list 收件人地址（是一个列表）
    fail_silently=False
    auth_user=None
    auth_password=None,
    connection=None
    html_message=None 邮件内的html信息
    :return:
    '''
    sr = redis.StrictRedis()
    sr.set(username, token)
    html_message = "<a href='http://127.0.0.1/user/verify_mail/?user=" + username + "&token=" + token + ">激活链接</a>"
    send_mail('激活账号', '请点击下面的链接激活您的账号', settings.DEFAULT_FROM_EMAIL, [mail_addr, ], html_message=html_message)


def make_hash(password):
    """
    将用户注册时的密码sha-1加密后返回
    :param password:  用户输入的明文密码
    :return:  加密后的40位密文
    """
    sha1 = hashlib.sha1()
    sha1.update(password)
    return sha1.hexdigest()


def register(request):
    """
    渲染注册的模板
    :param request:
    :return: 模板信息
    """
    return render(request, 'user_center/register.html')


def register_handle(request):
    """
    处理注册的主函数
    :param request:
    :return: HttpResponse
    """
    post = request.POST
    username = post['user_name']
    password = post['pwd']
    mail = post['email']

    username_used = UserInfo.objects.filter(username=username)
    mail_used = UserInfo.objects.filter(mail=mail)

    if username_used and mail_used:
        return redirect('/user/register')
    else:
        user = UserInfo()
        user.username = username
        user.password = make_hash(password.encode('utf-8'))
        user.mail = mail
        user.save()
        send_verify_mail(username, mail)
    return HttpResponse('OK')


def register_username_check(request):
    """
    检查用户名是否已经被注册
    :param request:
    :return: 以JSON格式返回检查结果
    """
    get = request.GET
    result = False
    username = get['username']
    if UserInfo.objects.filter(username=username).count() == 0:
        result = True
    context = {'result': result}
    return JsonResponse(context)


def register_email_check(request):
    """
    检查邮箱是否已经被注册
    :param request:
    :return: 以JSON格式返回检查结果
    """
    get = request.GET
    result = False
    email = get['email']
    if UserInfo.objects.filter(mail=email).count() == 0:
        result = True
    context = {'result': result}
    return JsonResponse(context)


def verify_mail(request):
    """
    处理邮箱激活链接发过来的请求，
    验证GET请求的用户名与token是否与redis中存储的键值对一致
    :param request:
    :return: HttpResponse
    """
    get = request.GET
    username = get['user']
    token = get['token']
    sr = redis.StrictRedis()
    if sr.get(username).decode('utf-8') == token:
        user = UserInfo.objects.filter(username=username)[0]
        user.verifivation = True
        response = '激活成功'
        print(user.verifivation)
        sr.delete(username)
    else:
        response = '激活失败'
    return HttpResponse(response)