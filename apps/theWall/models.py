from __future__ import unicode_literals
from django.db import models
import re, bcrypt

class UserManager(models.Manager):
    def checkRegistration(self, data):
        errors = {}
        emailRegex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        users = User.objects.all()
        if len(data['first_name']) < 2:
            errors['first_name'] = "Error: Name fields must contain at least 2 Characters"
        elif len(data['last_name']) < 2:
            errors['last_name'] = "Error: Name fields must contain at least 2 Characters"
        elif bool(re.search(r'\d', data['first_name'])) == True:
            errors['first_name'] = "Error: Name fields cannot contain a number. who are u R2D2?"
        elif bool(re.search(r'\d', data['last_name'])) == True:
            errors['last_name'] = "Error: Name fields cannot contain a number. Who are u R2D2?"
        elif not emailRegex.match(data['email']):
            errors['email'] = "Error: Email is not valid"
        for user in users:
            if data['email'] == user.email:
                errors['email'] = "Sorry! email already taken"
        if len(data['password']) < 8:
            errors['password'] = "Error: password must contain at least 8 characters"
        elif data['password'] != data['pw_confirm']:
            errors['password'] = "Error: Password and confirmation do not match"
        elif bool(re.search(r'\d', data['password'])) == False:
            errors['password'] = "Error: Password must contain at least 1 number(s)"
        return errors

    def checkLogin(self, data):
        errors = {}
        # password = bcrypt.hashpw(request.form['password'].encode(), bcrypt.gensalt())
        if not User.objects.filter(email=data['email']):
            errors['login'] = "Were sorry. we couldn't find your email in our system!"
        else: 
            user = User.objects.get(email=data['email'])
            print(user.password)
            # print("*"*100)
            print("Test : " + str(bcrypt.checkpw(data['password'].encode(),user.password.encode())))
            print("*"*100)
            if not bcrypt.checkpw(data['password'].encode(), user.password.encode()):
                errors['login'] = "Error: password incorrect"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at =models.DateTimeField(auto_now_add = True)
    objects = UserManager()
    def __repr__(self):
        return "<object id: {}, first_name: {}, last_name: {}, created_at: {}".format(self.first_name, self.last_name, self.email, self.created_at)


class Message(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    user_id = models.ForeignKey(User, related_name = 'messages', on_delete = models.PROTECT)
    def __repr__(self):
        return "<comment id: {}, content: {}, created_at: {}>".format(self.id, self.content, self.created_at)

class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    user_id = models.ForeignKey(User, related_name = 'comments', on_delete = models.PROTECT)
    message_id = models.ForeignKey(Message, related_name = 'comments', on_delete = models.CASCADE)
    def __repr__(self):
        return "<message id: {}, content: {}, created_at: {}>".format(self.id, self.content, self.created_at)