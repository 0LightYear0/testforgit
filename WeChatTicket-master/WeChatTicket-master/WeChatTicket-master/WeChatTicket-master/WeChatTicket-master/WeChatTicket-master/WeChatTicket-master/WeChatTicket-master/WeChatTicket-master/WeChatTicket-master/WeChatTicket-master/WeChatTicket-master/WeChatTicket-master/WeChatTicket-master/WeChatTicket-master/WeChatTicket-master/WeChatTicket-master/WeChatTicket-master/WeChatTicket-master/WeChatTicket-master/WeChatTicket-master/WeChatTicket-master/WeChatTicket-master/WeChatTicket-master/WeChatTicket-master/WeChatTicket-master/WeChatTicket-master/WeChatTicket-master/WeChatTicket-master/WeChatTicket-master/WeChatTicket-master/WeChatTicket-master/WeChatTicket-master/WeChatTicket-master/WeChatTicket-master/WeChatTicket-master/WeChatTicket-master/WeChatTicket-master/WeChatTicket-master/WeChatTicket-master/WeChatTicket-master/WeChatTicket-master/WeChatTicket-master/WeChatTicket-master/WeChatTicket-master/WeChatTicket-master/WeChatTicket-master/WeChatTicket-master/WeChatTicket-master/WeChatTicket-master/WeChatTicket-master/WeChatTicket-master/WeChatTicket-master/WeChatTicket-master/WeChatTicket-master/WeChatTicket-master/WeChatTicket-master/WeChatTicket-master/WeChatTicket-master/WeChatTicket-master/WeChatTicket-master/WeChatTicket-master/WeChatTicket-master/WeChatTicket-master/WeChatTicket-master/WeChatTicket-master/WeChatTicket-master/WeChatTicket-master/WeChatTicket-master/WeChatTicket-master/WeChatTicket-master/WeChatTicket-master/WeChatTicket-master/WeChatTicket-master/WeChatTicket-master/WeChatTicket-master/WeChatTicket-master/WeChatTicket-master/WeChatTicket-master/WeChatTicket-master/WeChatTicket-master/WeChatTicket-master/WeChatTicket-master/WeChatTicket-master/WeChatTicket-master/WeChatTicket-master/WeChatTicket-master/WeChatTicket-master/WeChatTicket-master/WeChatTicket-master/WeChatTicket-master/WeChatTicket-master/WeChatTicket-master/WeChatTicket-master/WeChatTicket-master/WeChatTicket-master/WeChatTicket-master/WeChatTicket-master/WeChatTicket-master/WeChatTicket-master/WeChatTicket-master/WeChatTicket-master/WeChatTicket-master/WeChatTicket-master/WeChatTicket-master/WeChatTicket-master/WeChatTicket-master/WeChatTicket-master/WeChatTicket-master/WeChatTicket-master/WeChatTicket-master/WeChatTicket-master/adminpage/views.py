from django.shortcuts import render
import datetime
from codex.baseerror import *
from codex.baseview import APIView
from wechat.models import User, Activity, Ticket
from django.contrib.auth import authenticate,login,logout
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from WeChatTicket import settings
from wechat.views import CustomWeChatView
import urllib.request
import urllib.parse

class Login(APIView):

    def get(self):
        try:
            if self.request.user.is_authenticated():
                return 0
            else:
                raise BaseError(-1, "can not log in")
        except:
            raise BaseError(-1,"user get error")

    def post(self):
        self.check_input("username" ,"password")
        user = authenticate(username = self.input["username"], password = self.input["password"])
        if user is not None:
            if user.is_active:
                login(self.request, user)
                return 0
            else:
                BaseError(-1,"User is not active")
        else:
            raise BaseError(-1,"User does not exist")

class Logout(APIView):
    def post(self):
        try:
            logout(self.request)
        except:
            raise BaseError(-1, "Logout Error")
        else:
            return 0

class ActivityList(APIView):
    def get(self):
        if self.request.user.is_authenticated():
            currentTime = datetime.datetime.now().timestamp()
            result = []
            for activity in Activity.objects.all().exclude(status = -1):
                result.append({
                    'name':activity.name,
                    'id':activity.id,
                    'description':activity.description,
                    'startTime':activity.start_time.timestamp(),
                    'endTime':activity.end_time.timestamp(),
                    'place':activity.place,
                    'bookStart':activity.book_start.timestamp(),
                    'bookEnd':activity.book_end.timestamp(),
                    'currentTime':currentTime,
                    'status':activity.status
                })
            return result
        else:
            raise BaseError(-1 ,"Have not log in")

class CreateActivity(APIView):
    def post(self):
        self.check_input('name', 'place', 'key', 'description', 'picUrl', 'startTime', 'endTime', 'bookStart','bookEnd',
                         'totalTickets','status')
        if self.request.user.is_authenticated():
            activity = Activity.objects.create(name = self.input['name'], key = self.input['key'], place = self.input['place'],
                                               description = self.input['description'], pic_url = self.input['picUrl'], end_time = self.input['endTime'], start_time = self.input['startTime'], book_start = self.input['bookStart'],
                                          book_end = self.input['bookEnd'],total_tickets = self.input['totalTickets'],status = self.input['status'], remain_tickets = self.input['totalTickets'])
            activity.save()
            return activity.id
        else:
            raise BaseError(-1, "Have not log in")

class DeleteActivity(APIView):
    def post(self):
        self.check_input('id')
        flag = 0
        if self.request.user.is_authenticated():
            for activity in Activity.objects.all().exclude(status=-1):
                if activity.id == self.input['id']:
                    flag = 1
                    activity.status = -1
                    activity.save()
            if flag == 1:
                return 0
            else:
                raise BaseError(-1, "No such activity")
        else:
            raise BaseError(-1, "Have not log in")

'''class ImageUpload(APIView):
    def post(self):
        self.check_input('image')
        if self.request.user.is_authenticated(): '''

class ActivityDetail(APIView):
    def get(self):
        self.check_input('id')
        result = {}
        if self.request.user.is_authenticated():
            currentTime = datetime.datetime.now().timestamp()
            activity = Activity.objects.get(id = self.input['id'])
            result={
                'name':activity.name,
                'key':activity.key,
                'picUrl':activity.pic_url,
                'description':activity.description,
                'startTime':activity.start_time.timestamp(),
                'endTime':activity.end_time.timestamp(),
                'place':activity.place,
                'bookStart':activity.book_start.timestamp(),
                'bookEnd':activity.book_end.timestamp(),
                'totalTickets':activity.total_tickets,
                'currentTime':currentTime,
                'status':activity.status,
                'bookedTickets':activity.total_tickets-activity.remain_tickets,
                'usedTickets':0
            }
            return result

    def post(self):
        self.check_input('id','place','description','picUrl','startTime','endTime','bookEnd'
                         ,'totalTickets','status')
        if self.request.user.is_authenticated():
            activity = Activity.objects.get(id=self.input['id'])
            activity.place = self.input['place']
            activity.description = self.input['description']
            activity.pic_url = self.input['picUrl']
            activity.start_time = self.input['startTime']
            activity.end_time = self.input['endTime']
            activity.book_end = self.input['bookEnd']
            activity.total_tickets = self.input['totalTickets']
            activity.status = self.input['status']
            activity.save()
            return 0
        else:
            raise BaseError(-1,"Can not modify the activity")

class UploadImage(APIView):
    def post(self):
        if self.request.user.is_authenticated():
            filename = self.request.FILES['image']
            path = default_storage.save(filename.name, ContentFile(filename.read()))
            return settings.get_url('media/')+ str(path)
        else:
            raise BaseError(-1,"You have not log in")
class ActivityMenu(APIView):
    def get(self):
        if self.request.user.is_authenticated():
            currentTime = datetime.datetime.now().timestamp()
            result = []
            for activity in Activity.objects.all().exclude(status = -1):
                result.append({
                    'name':activity.name,
                    'id':activity.id,
                    'menuIndex':activity.menuIndex
                })
            return result
        else:
            raise BaseError(-1 ,"Have not log in")
    def post(self):
        if self.request.user.is_authenticated() == False:
            raise "Have not log in"

        list = self.input

        for index in range(0,len(list)):
            temp = Activity.objects.get(id = list[index])
            temp.menuIndex = index+1
            temp.save()

        all_list = Activity.objects.all()
        for index in range(0, len(all_list)):
            if all_list[index].id not in list:
                all_list[index].menuIndex = 0
                all_list[index].save()


class CheckIn(APIView):
    def post(self):
        self.check_input('actId')
        flag = 0
        if self.request.user.is_authenticated():
            if 'ticket' in self.input:
                for tic in Ticket.objects.all():
                    if tic.activity.id == int(self.input['actId']) and tic.unique_id == self.input['ticket']:
                        result = {
                            'ticket': tic.unique_id,
                            'studentId': tic.student_id
                        }
                        #tic.activity.remain_tickets -= 1
                        tic.activity.save()
                        return result
            elif 'studentId' in self.input:
                for tic in Ticket.objects.all():
                    #print(type(tic.student_id))
                    #print(type(self.input['studentId']))
                    #print(type(tic.activity.id))
                    #print(type(self.input['actId']))
                    #print('\n')
                    if tic.activity.id == int(self.input['actId']) and tic.student_id == self.input['studentId']:
                        result = {
                            'ticket': tic.unique_id,
                            'studentId': tic.student_id
                        }
                        #tic.activity.remain_tickets -= 1
                        tic.activity.save()
                        return result
            else:
                raise BaseError(-1, "Wrong StudentID or TicketID")
            raise BaseError(-1, "Wrong StudentID or TicketID")
        else:
            raise BaseError(-1 ,"Have not log in")






