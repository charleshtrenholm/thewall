from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
    def checkRegistration(self, data):
        errors = {}
        emailRegex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        checkusers = User.objects.all()
        if len(data['first_name']) < 1 or len(data['last_name']) < 1:
            errors['name'] = "Please complete all fields"
        elif len(data['first_name']) < 2 or len(data['last_name']) < 2:
            errors['name'] = "Error: name fields must contain at least 2 characters"
        elif not emailRegex.match(data['email']):
            errors['email'] = "Error: Invalid email address"
        for user in checkusers:
            if data['email'] == user.email:
                errors['email'] = "Sorry! Email already taken"
        if len(data['password']) < 8:
            errors['password'] = "Error: Password must be at least 8 characters"
        elif bool(re.search(r'\d', data['password'])) == False:
            errors['password'] = "Error: Password must contain at least 1 number(s)"
        elif data['password'] != data['pw_confirm']:
            errors['password'] = "Error: Password and confirmation do not match"
        return errors

    def checkLogin(self, data):
        errors = {}
        users = User.objects
        if not data:
            errors['login'] = "Error: please complete all fields"
        elif not User.objects.get(email=data['email']):
            errors['login'] = "Sorry! We couldn't find your email in our system"
        else: user = User.objects.get(email=data['email'])
        if not bcrypt.checkpw(data['password'].encode(), user.password.encode()):
            errors['login'] = "Error: password incorrect"
        return errors

    def checkUpdate(self, data):
        errors = {}
        emailRegex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        checkusers = User.objects.all()
        if len(data['first_name']) < 1 or len(data['last_name']) < 1:
            errors['name'] = "Please complete all fields"
        elif len(data['first_name']) < 2 or len(data['last_name']) < 2:
            errors['name'] = "Error: name fields must contain at least 2 characters"
        elif not emailRegex.match(data['email']):
            errors['email'] = "Error: Invalid email address"
        for user in checkusers:
            if data['email'] == user.email:
                errors['email'] = "Sorry! Email already taken"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    objects = UserManager()
    def __repr__(self):
        return "<user first_name: {}, last_name: {}, email{}, id: {}>".format(self.first_name, self.last_name, self.email, self.id)

class QuoteManager(models.Manager):
    def checkQuote(self, data):
        errors = {}
        if len(data['author']) == 0 or len(data['quote']) == 0:
            errors['quote'] = "Please fill out the form"
        elif len(data['author']) < 3:
            errors['quote'] = "Error: Author name must contain at least 3 characters"
        elif len(data['quote']) < 10:
            errors['quote'] = "Error: quote must contain at least 10 characters"
        return errors

class Quote(models.Model):
    author = models.CharField(max_length = 255)
    content = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    user = models.ForeignKey(User, related_name = "quotes", on_delete = models.CASCADE)
    objects = QuoteManager()
    def __repr__(self):
        return "<quote id: {}, quote content: {}".format(self.id, self.content)

class Like(models.Model):
    quote = models.ForeignKey(Quote, related_name = "likes", on_delete = models.CASCADE)
    user = models.ForeignKey(User, related_name = "likes", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
