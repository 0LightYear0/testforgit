from codex.baseerror import *
from codex.baseview import APIView
import datetime

from wechat.models import User, Ticket, Activity

import urllib.request
import urllib.parse

class UserBind(APIView):

    def validate_user(self):
        """
        input: self.input['student_id'] and self.input['password']
        raise: ValidateError when validating failed
        """
        # 定义一个要提交的数据数组
        data = {}
        data['i_user'] = self.input['student_id']
        data['i_pass'] = self.input['password']

        # 定义post的地址
        url = 'https://id.tsinghua.edu.cn/do/off/ui/auth/login/post/fa8077873a7a80b1cd6b185d5a796617/0?/j_spring_security_thauth_roaming_entry'
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
        post_data = urllib.parse.urlencode(data).encode(encoding='UTF8')
        headers = {'User-Agent': user_agent}
        # 提交，发送数据
        req = urllib.request.Request(url, post_data, headers)
        # 获取提交后返回的信息
        response = urllib.request.urlopen(req)
        content = response.geturl()
        con = content[0:42]
        if(con != 'http://learn.cic.tsinghua.edu.cn/f/student'):
            raise  ValidateError('验证失败，用户名或密码不正确')

    def get(self):
        self.check_input('openid')
        return User.get_by_openid(self.input['openid']).student_id

    def post(self):
        self.check_input('openid', 'student_id', 'password')
        user = User.get_by_openid(self.input['openid'])
        self.validate_user()
        user.student_id = self.input['student_id']
        user.save()

class UserActivityDetail(APIView):
    def get(self):
        self.check_input('id')
        activity = Activity.objects.get(id = self.input['id'])
        if activity.status == 1:
            currentTime = datetime.datetime.now().timestamp()
            result = {
                'name': activity.name,
                'key': activity.key,
                'picUrl': activity.pic_url,
                'description': activity.description,
                'startTime': activity.start_time.timestamp(),
                'endTime': activity.end_time.timestamp(),
                'place': activity.place,
                'bookStart': activity.book_start.timestamp(),
                'bookEnd': activity.book_end.timestamp(),
                'totalTickets': activity.total_tickets,
                'currentTime': currentTime,
                'remain_tickets':activity.remain_tickets,
            }
            return result
        else:
            raise BaseError(-1, "No Such Activity")

class UserTicketDetail(APIView):
    def get(self):
        self.check_input('openid', 'ticket')
        currentTime = datetime.datetime.now().timestamp()
        tic = Ticket.objects.get(unique_id= self.input['ticket'])
        result = {
            'activityName':tic.activity.name,
            'place':tic.activity.place,
            'activityKey':tic.activity.key,
            'uniqueId':tic.unique_id,
            'startTime':tic.activity.start_time.timestamp(),
            'endTime':tic.activity.end_time.timestamp(),
            'currentTime':currentTime,
            'status':tic.status,
        }
        return result

