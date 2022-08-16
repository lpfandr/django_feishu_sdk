django_feishu_sdk
=================

Required
========

1.Install or add django-feishu-sdk to your python path.

.. code:: python

   pip install django-feishu-sdk

2.Add feishu to your setting.

.. code:: python

   # 飞书配置
   FEISHU_V2_SDK_CONFIGS = {
       'FEISHU_APP_ID': "xxx",  # 企业应用的id
       'FEISHU_APP_SECRET': "xxx",  # 企业应用的SECRET
       'FEISHU_VERIFY_TOKEN': "xxx",  # 企业应用的事件加密token
       'FEISHU_ENCRYPT_KEY': "xxx",  # 企业应用的事件加密key
   }

3.If you use events, you’d better make the following settings

.. code:: python

   ALLOWED_HOSTS = ['*']
   MIDDLEWARE = [
       'django.middleware.security.SecurityMiddleware',
       'django.contrib.sessions.middleware.SessionMiddleware',
       'django.middleware.common.CommonMiddleware',
       # 'django.middleware.csrf.CsrfViewMiddleware',
       'django.contrib.auth.middleware.AuthenticationMiddleware',
       'django.contrib.messages.middleware.MessageMiddleware',
       'django.middleware.clickjacking.XFrameOptionsMiddleware',
   ]

Usage
=====

   ⚠ 您应该优先创建一个app,完善相关url路径，startapp xxx

   .. rubric:: 除事件外的数据获取
      :name: 除事件外的数据获取

   1.在view.py中调用飞书数据

.. code:: python

   from django.http import JsonResponse
   from django_feishu_sdk import *


   def send_text_messages(request):
       """
       发送文本消息
       """
       fs_client = FeishuClient()
       fs_client.send_card()
       res = fs_client.send_text(text='测试消息', receive_id_type='open_id', receive_id='ou_63f6845d304e7a1a3df99d6fce291d58')
       print(res)
       return JsonResponse(res)


   def get_user_info(request):
       """
       按照用户个人信息
       """
       fs_client = FeishuClient()
       res = fs_client.get_user_info(user_id='77g56381', user_id_type='user_id')
       print(res)
       return JsonResponse()

2.url.py

.. code:: python

   from django.urls import path
   from .views import *

   urlpatterns = [
       path('get_user_info/', get_user_info),  # 获取用户的信息
       path('event_process/', event_process),  # 接收事件订阅的消息
   ]

3.当前页面json显示 # 事件的数据获取
1.在app中的统计目录新建feishu.py文件,内容如下

.. code:: python

   from django.http import JsonResponse
   from django_feishu_sdk import UrlVerificationEvent, MessageReceiveEvent, FeishuClient, MessageReadEvent
   from django_feishu_sdk.apis.event import EventManager

   event_manager = EventManager()

   # 处理首次事件配置
   @event_manager.register("url_verification")
   def request_url_verify_handler(req_data: UrlVerificationEvent):
       # url verification, just need return challenge
       return JsonResponse({"challenge": req_data.event.challenge})

   # 消息已读事件
   @event_manager.register("im.message.message_read_v1")
   def message_read_event_handler(req_data: MessageReadEvent):
       print('sender', req_data.event.get('reader'))
       print('req_data', req_data.header.event_id)
       receive_id = req_data.event.get('reader').get('reader_id').get('open_id')
       fs_client = FeishuClient()
       res = fs_client.send_text(text='监测到消息已读', receive_id_type='open_id',
                                 receive_id=receive_id)
       print(res)
       return JsonResponse(res)

2.view.py文件如下

.. code:: python

   from django_feishu_sdk import *
   from .feishu import event_manager


   def event_process(request):
       """
       与飞书事件挂载
       """
       event_handler, event = event_manager.get_handler_with_event(request)
       return event_handler(event)

事件扩展
========

1.在app中的统计目录新建feishu.py文件,内容如下

.. code:: python


   from django.http import JsonResponse
   from django_feishu_sdk import UrlVerificationEvent, MessageReceiveEvent, FeishuClient, MessageReadEvent, EventContent
   from django_feishu_sdk.apis.event import EventManager


   class MessageReadEvent(EventContent):
       """
       事件类型：已读消息
       飞书文档地址：https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/events/message_read
       """

       @staticmethod
       def event_type():
           return "im.message.message_read_v1"


   class MyEventManager(EventManager):
       _event_list = [MessageReceiveEvent, UrlVerificationEvent, MessageReadEvent]


   event_manager = MyEventManager()


   @event_manager.register("im.message.receive_v1")
   def message_receive_event_handler(req_data: MessageReceiveEvent):
       # sender_id = req_data.event.sender.sender_id
       # message = req_data.event.message
       fs_client = FeishuClient()
       res = fs_client.send_text(text='测试消息', receive_id_type='open_id', receive_id='ou_63f6845d304e7a1a3df99d6fce291d58')
       print(res)
       return JsonResponse(res)

2.注意事项
feishu.py文件中类继承时，_event_list已经给出了默认的三个，应该保留

.. code:: python

   # 原始
   _event_list = [MessageReceiveEvent, UrlVerificationEvent, MessageReadEvent]
   # 重写后
   _event_list = [MessageReceiveEvent, UrlVerificationEvent, MessageReadEvent,yournewEvent]
