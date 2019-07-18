from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from .models import Profile, Contact
from myweibo.models import MsgInfo, UserInfo, UserMsgIndex, Comment, HotMsg, Bulletin


@login_required
@csrf_exempt
def index(request):
    user_profile = Profile.objects.get(user=request.user)
    msg_index = UserMsgIndex.objects.filter(user=request.user).order_by("-time")
    hot_msg = HotMsg.objects.all()
    bulletins = Bulletin.objects.all()
    if request.method == 'POST':
        content = request.POST.get('msg_contents')
        # print(content)
        msg = MsgInfo.objects.create(content=content, user=request.user)  # 将消息写入数据库
        msg.save()
        msg_id = msg.id
        msgindex = UserMsgIndex.objects.create(user=request.user, author=request.user, message=msg, time=msg.time)
        msgindex.save()
        print('推送用户：', request.user)
        # 获取粉丝列表
        user_fans = Contact.objects.filter(user_to_id=user_profile.user_id)
        print(user_fans.count())
        # 分别向各个粉丝的msg_index中添加刚刚发布的消息
        for fans in user_fans:
            user = User.objects.get(id=fans.user_from_id)
            UserMsgIndex.objects.create(user=user, author=request.user, message=msg, time=msg.time)
            print('被推送用户：', user.username)
        user_profile.msg_count += 1
        user_profile.save()
    user_msg_count = user_profile.msg_count
    user_fans_count = user_profile.fans_count
    user_follow_count = user_profile.follow_count
    user_icon = user_profile.icon.url
    return render(request, 'account/index1.html', locals())


@require_POST
@login_required
@csrf_exempt
def share(request):
    if request.method == 'POST':
        user_profile = Profile.objects.get(user=request.user)
        content = request.POST.get('msg_contents')
        print(content)
        msg = MsgInfo.objects.create(content=content, user=request.user, type=1)  # 将消息写入数据库
        msg.save()
        msg_id = msg.id
        msgindex = UserMsgIndex.objects.create(user=request.user, author=request.user, message=msg, time=msg.time)
        msgindex.save()
        print('推送用户：', request.user)
        # 获取粉丝列表
        user_fans = Contact.objects.filter(user_from_id=user_profile.user_id)
        # 分别向各个粉丝的msg_index中添加刚刚发布的消息
        for fans in user_fans:
            user = User.objects.get(id=fans.user_to_id)
            UserMsgIndex.objects.create(user=user, author=request.user, message=msg, time=msg.time)
            print('被推送用户：', user.username)
    return JsonResponse({"msg_id": msg_id})


@require_POST
@login_required
@csrf_exempt
def comment(request):
    user = request.user
    m_id = request.POST.get('msg_id')
    comment = Comment.objects.filter(message_id=m_id).values().order_by('-time')
    if comment.count() == 0:
        print(comment)
        return JsonResponse({'status': 'None'})
    data = {}
    data["data"] = list(comment)
    return JsonResponse(data, safe=False)


@login_required
@csrf_exempt
def post_comment(request):
    content = request.POST.get('content')
    m_id = request.POST.get('msg_id')
    msg = MsgInfo.objects.get(id=m_id)
    c = Comment.objects.create(user=request.user, content=content, message=msg, username=request.user.username)
    msg.commented_count += 1
    msg.save()
    c.save()
    print(content, m_id)
    print('msg', msg.content)
    return JsonResponse({'status': 'ok'})


@login_required
@csrf_exempt
def like(request):
    m_id = request.POST.get('msg_id')
    msg = MsgInfo.objects.get(id=m_id)
    msg.like += 1
    msg.save()
    print(msg.like)
    return JsonResponse({'lick_count': msg.like})


@login_required
def user_detail(request, username):
    user_id = User.objects.get(username=username)
    request.session['username'] = username
    user = get_object_or_404(User, username=username, is_active=True)
    user_profile = Profile.objects.get(user_id=user_id)
    # user_icon = user_profile.icon.url
    print(user_profile.user)
    # 获取用户发布的微博
    user_msg = MsgInfo.objects.filter(user_id=user_id).order_by('-time')

    paginator = Paginator(user_msg, 10)  # 使用分页功能
    for item in paginator.page(1).object_list:
        print(item.content)
    if request.method == 'GET':
        # 获取url后面的page参数的值，首页不显示page参数，默认值是1
        page = request.GET.get('page')
        try:
            msgs = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数，返回第一页。
            msgs = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse("找不到页面内容")
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内， 返回结果的最后一页
            msgs = paginator.page(paginator.num_pages)
    return render(request, 'account/user/detail.html', locals())


@require_POST
@login_required
@csrf_exempt
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            f1 = Profile.objects.get(user=request.user)
            f2 = Profile.objects.get(user=user)
            if action == "follow":
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
                f1.follow_count += 1
                f2.fans_count += 1
                f1.save()
                f2.save()
                print(f1.user, f2.user)
            else:
                Contact.objects.filter(user_from=request.user, user_to=user).delete()
                f1.follow_count -= 1
                f2.fans_count -= 1
                f1.save()
                f2.save()

            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'ko'})

    return JsonResponse({'status': 'ko'})


@require_POST
@login_required
@csrf_exempt
def del_msg(request):
    user = request.user
    user_info = UserInfo.objects.get(user=user)
    index_id = request.POST.get('msg_index_id')
    msg_id = request.POST.get('msg_id')
    print(type(index_id))
    print("索引id：", index_id)
    print("消息id：", msg_id)
    # if request.method == 'POST':
    msg = MsgInfo.objects.filter(id=msg_id).delete()
    UserMsgIndex.objects.filter(message_id=msg_id).delete()
    user_info.msg_count -= 1
    user_info.save()

    return JsonResponse({'status': 'ok'})


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Authenticated successfully")
                else:
                    return HttpResponse("Disabled account")
            else:
                return HttpResponse("Invalid login")
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # 建立新数据对象但是不写入数据库
            new_user = user_form.save(commit=False)
            # 设置密码
            new_user.set_password(user_form.cleaned_data['password'])
            # 保存User对象
            new_user.save()
            Profile.objects.create(user=new_user)
            UserInfo.objects.create(user=new_user)
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def edit(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def my_fans(request):
    username = request.session.get('username', default=request.user)
    user_id = User.objects.get(username=username)
    user_info = Profile.objects.get(user_id=user_id)
    fans_count = user_info.fans_count
    # fans = User.follower.all()
    fans_info = Contact.objects.filter(user_to_id=user_id)
    for fan in fans_info:
        print(fan.user_from.profile.profile, fan.user_from.profile.user)

    return render(request, 'account/myfans.html', locals())


@login_required
def my_follow(request):
    username = request.session.get('username', default=request.user)
    user_id = User.objects.get(username=username)
    user_info = Profile.objects.get(user_id=user_id)
    follow_count = user_info.follow_count
    # fans = User.follower.all()
    follow_info = Contact.objects.filter(user_from_id=user_id)
    for follow in follow_info:
        print(follow.user_from.profile.user_id)
        print(follow.user_from.profile.profile)
    return render(request, 'account/myfollow.html', locals())


@login_required
@csrf_exempt
def bulletin(request, id):
    # bulletin_id = request.POST.get('bulletin_id')
    bulletin_item = Bulletin.objects.get(id=id)
    print(bulletin_item.title) 
    return render(request, 'account/bulletin.html', locals())