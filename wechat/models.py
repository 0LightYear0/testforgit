from django.db import models
import json
from codex.baseerror import LogicError


class User(models.Model):
    open_id = models.CharField(max_length=64, unique=True, db_index=True)
    valid_tickets = models.CharField(max_length=200, default = '[]')
    invalid_tickets = models.CharField(max_length=200, default='[]')
    used_tickets = models.CharField(max_length=200, default='[]')
    student_id = models.CharField(max_length=32, db_index=True)

    @classmethod
    def get_by_openid(cls, openid):
        try:
            return cls.objects.get(open_id=openid)
        except cls.DoesNotExist:
            raise LogicError('User not found')

    def get_valid_tickets(self):
        if isinstance(self.valid_tickets, str):
            return json.loads(self.valid_tickets)
        return self.valid_tickets

    def append_valid_tickets(self, ticket):
        temp = self.get_valid_tickets()
        temp.append(ticket)
        self.valid_tickets = json.dumps(temp)
        self.save()

    def remove_valid_tickets(self, ticket):
        temp = self.get_valid_tickets()
        if ticket in temp:
            ticket.remove(ticket)
            self.valid_tickets = json.dumps(temp)
            self.save()
            return True
        self.valid_tickets = json.dumps(temp)
        self.save()
        return False

    def get_invalid_tickets(self):
        if isinstance(self.invalid_tickets, str):
            return json.loads(self.invalid_tickets)
        return self.invalid_tickets

    def append_invalid_tickets(self, ticket):
        temp = self.get_invalid_tickets()
        temp.append(ticket)
        self.invalid_tickets = json.dumps(temp)
        self.save()

    def remove_invalid_tickets(self, ticket):
        temp = self.get_invalid_tickets()
        if ticket in temp:
            ticket.remove(ticket)
            self.invalid_tickets = json.dumps(temp)
            self.save()
            return True
        self.invalid_tickets = json.dumps(temp)
        self.save()
        return False

    def get_used_tickets(self):
        if isinstance(self.used_tickets, str):
            return json.loads(self.used_tickets)
        return self.used_tickets

    def append_used_tickets(self, ticket):
        temp = self.get_used_tickets()
        temp.append(ticket)
        self.used_tickets = json.dumps(temp)
        self.save()

    def remove_used_tickets(self, ticket):
        temp = self.get_used_tickets()
        if ticket in temp:
            ticket.remove(ticket)
            self.used_tickets = json.dumps(temp)
            self.save()
            return True
        self.used_tickets = json.dumps(temp)
        self.save()
        return False





class Activity(models.Model):
    name = models.CharField(max_length=128)
    key = models.CharField(max_length=64, db_index=True)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    place = models.CharField(max_length=256)
    book_start = models.DateTimeField(db_index=True)
    book_end = models.DateTimeField(db_index=True)
    total_tickets = models.IntegerField()
    status = models.IntegerField()
    pic_url = models.CharField(max_length=256)
    remain_tickets = models.IntegerField()
    menuIndex = models.IntegerField(default=0)

    STATUS_DELETED = -1
    STATUS_SAVED = 0
    STATUS_PUBLISHED = 1


class Ticket(models.Model):
    student_id = models.CharField(max_length=32, db_index=True)
    unique_id = models.CharField(max_length=64, db_index=True, unique=True)
    activity = models.ForeignKey(Activity)
    status = models.IntegerField()

    STATUS_CANCELLED = 0
    STATUS_VALID = 1
    STATUS_USED = 2
