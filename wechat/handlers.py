# -*- coding: utf-8 -*-
#
from wechat.wrapper import WeChatHandler
from wechat.models import Activity, Ticket, User
import datetime
import json

__author__ = "Epsirom"


class ErrorHandler(WeChatHandler):

    def check(self):
        return True

    def handle(self):
        return self.reply_text('对不起，您输入的信息不规范，请重试')


class DefaultHandler(WeChatHandler):

    def check(self):
        return True

    def handle(self):
        return self.reply_text('对不起，没有找到您需要的信息:(')


class HelpOrSubscribeHandler(WeChatHandler):

    def check(self):
        return self.is_text('帮助', 'help') or self.is_event('scan', 'subscribe') or \
               self.is_event_click(self.view.event_keys['help'])

    def handle(self):
        return self.reply_single_news({
            'Title': self.get_message('help_title'),
            'Description': self.get_message('help_description'),
            'Url': self.url_help(),
        })


class UnbindOrUnsubscribeHandler(WeChatHandler):

    def check(self):
        return self.is_text('解绑') or self.is_event('unsubscribe')

    def handle(self):
        self.user.student_id = ''
        self.user.save()
        return self.reply_text(self.get_message('unbind_account'))


class BindAccountHandler(WeChatHandler):

    def check(self):
        return self.is_text('绑定') or self.is_event_click(self.view.event_keys['account_bind'])

    def handle(self):
        return self.reply_text(self.get_message('bind_account'))


class BookEmptyHandler(WeChatHandler):

    def check(self):
        return self.is_event_click(self.view.event_keys['book_empty'])

    def handle(self):
        return self.reply_text(self.get_message('book_empty'))


class BookWhatHandler(WeChatHandler):

    def check(self):
        return self.is_event_click(self.view.event_keys['book_what'])

    def handle(self):
        acts = Activity.objects.filter(book_end__gte=datetime.datetime.now()).order_by('start_time')
        answer = []
        for index in range(0, len(acts)):
            if index >= 5:
                break
            answer.append({
                'Title': acts[index].name,
                'Description': acts[index].description,
                'Url': self.url_act(acts[index].id),
            })
        return self.reply_news(answer)

class GetTicketHandler(WeChatHandler):

    def check(self):
        return self.is_event_click(self.view.event_keys['get_ticket'])

    def handle(self):
        tic_flag  = False

        tic = []
        
        for i in Ticket.objects.all():
            if i.student_id == self.user.student_id and i.status == 1:
                    tic_flag = True
                    tic.append(i)
        answer = []
        if len(tic) == 0:
            return self.reply_text("Sorry, you have no tickets now!")
        for index in range(0, len(tic)):
            if index >= 5:
                break
            answer.append({
                'Title': tic[index].activity.name,
                'Description': tic[index].activity.description,
                'Url': self.url_tic(self.user.open_id, tic[index].unique_id),
            })
        return self.reply_news(answer)

class ClickHeaderHandler(WeChatHandler):
    actid = 0
    def check(self):
        for act in Activity.objects.all():
            if self.is_event_click(self.view.event_keys['book_header'] + str(act.id)):
                ClickHeaderHandler.actid = act.id
                return self.is_event_click(self.view.event_keys['book_header']+str(act.id))
    def handle(self):
        act = Activity.objects.get(id = ClickHeaderHandler.actid)
        currentTime = datetime.datetime.now().timestamp()
        if self.user.student_id:
            if act:
                if act.book_start.timestamp() <= currentTime:
                    if act.book_end.timestamp() > currentTime:
                        if act.remain_tickets > 0:
                            tic = Ticket.objects.filter(student_id= User.objects.get(open_id=self.user.open_id).student_id).filter(activity = act).filter(status = 1)
                            if tic:
                                return self.reply_text("您已经拥有该活动的票了。")
                            tic_id = self.get_ticket_id(act, act.total_tickets - act.remain_tickets)
                            temp = Ticket.objects.create(student_id = User.objects.get(open_id=self.user.open_id).student_id, unique_id = tic_id, activity = act, status = 1)
                            temp.save()
                            act.remain_tickets -= 1
                            act.save()
                            return self.reply_single_news({
                                    'Title':act.name,
                                    'Description':act.description,
                                    'Url':self.url_activity(tic_id),
                            })
                        else:
                            return self.reply_text("抱歉，该活动的票已被抢光。")
                    else:
                        return self.reply_text("抱歉，该活动抢票已结束。")
                else:
                    return self.reply_text("抱歉，该活动尚未开始抢票。")
            else:
                return self.reply_text("对不起，您选择的活动不存在。")
        else:
            return self.reply_text("对不起，您还未绑定学号。")


class BookHeaderHandler(WeChatHandler):

    def check(self):
        return self.is_text_command('抢票')

    def handle(self):
        str = self.input['Content'][3:]
        activity = Activity.objects.filter(key = str)
        currentTime = datetime.datetime.now().timestamp()
        if self.user.student_id:
            if activity:
                for act in activity:
                    if act.book_start.timestamp() <= currentTime:
                        if act.book_end.timestamp() > currentTime:
                            if act.remain_tickets > 0:
                                tic = Ticket.objects.filter(student_id= User.objects.get(open_id=self.user.open_id).student_id).filter(activity = act).filter(status = 1)
                                if tic:
                                    return self.reply_text("您已经拥有该活动的票了。")
                                tic_id = self.get_ticket_id(act, act.total_tickets - act.remain_tickets)
                                temp = Ticket.objects.create(student_id = User.objects.get(open_id=self.user.open_id).student_id, unique_id = tic_id, activity = act, status = 1)
                                temp.save()
                                act.remain_tickets -= 1
                                act.save()
                                return self.reply_single_news({
                                    'Title':act.name,
                                    'Description':act.description,
                                    'Url':self.url_activity(tic_id),
                            })
                            else:
                                return self.reply_text("抱歉，该活动的票已被抢光。")
                        else:
                            return self.reply_text("抱歉，该活动抢票已结束。")
                    else:
                        return self.reply_text("抱歉，该活动尚未开始抢票。")
            else:
                return self.reply_text("对不起，您输入的活动不存在。")
        else:
            return self.reply_text("对不起，您还未绑定学号。")

class CancellHeaderHandler(WeChatHandler):

    def check(self):
        return self.is_text_command('退票')

    def handle(self):
        str = self.input['Content'][3:]
        activity = Activity.objects.filter(key = str)
        currentTime = datetime.datetime.now().timestamp()
        if activity:
            for act in activity:
                if act.book_start.timestamp() <= currentTime:
                    tic = Ticket.objects.get(student_id= User.objects.get(open_id=self.user.open_id).student_id, activity = act, status = 1)
                    if tic:
                        tic.delete()
                        act.remain_tickets += 1
                        act.save()
                        return self.reply_text("退票成功。")
                    else:
                        return self.reply_text("您还尚未拥有该活动的票。")
                else:
                    return self.reply_text("抱歉，该活动尚未开始抢票。")
        else:
            return self.reply_text("对不起，您输入的活动不存在。")


class CalHandler(WeChatHandler):

    def check(self):
        return True

    def handle(self):
        return self.reply_text(eval(self.input['Content']))
