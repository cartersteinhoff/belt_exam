# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[A-Za-z\s]\w+')


class UserManager(models.Manager):
    def validate_login(self, post_data):
        errors = []

        # check DB for email
        if len(self.filter(username=post_data['username'])) > 0:
            # check this user's password
            user = self.filter(username=post_data['username'])[0]
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors.append('Password Incorrect!')

        else:
            errors.append('Username not found!')

        if errors:
            return errors

        return user

    def validate_registration(self, post_data):
        errors = []

        # error handling for name fields
        if len(post_data['name']) < 2:
            errors.append("Names must be at least 3 characters!")

        if len(post_data['username']) < 2:
            errors.append("Username must be at least 3 characters!")

        # error handling for passwords
        if len(post_data['password']) < 8:
            errors.append("Passwords must be at least 8 characters!")

        # error handling for passwords
        if not re.match(EMAIL_REGEX, post_data['email']):
            errors.append("Email must be valid")

        # error handling for  letter characters            
        if not re.match(NAME_REGEX, post_data['name']):
            errors.append('Names must contain letter characters only!')

        # error handling for uniqueness of username
        if len(User.objects.filter(username=post_data['username'])) > 0:
            errors.append("This username is already in use!")

        # error handling for password matches
        if post_data['password'] != post_data['password_confirm']:
            errors.append("Passwords do not match")

        if (len(post_data['hire-date'])) <= 0:
            errors.append("Please enter a valid birthdate!")

        if int(post_data['hire-date'][0:4]) > 2017:
            errors.append("Please enter a birthdate before this year!")

        if not errors:
            # make our new user
            # hash password
            hashed = bcrypt.hashpw((post_data['password'].encode()), bcrypt.gensalt(5))

            new_user = self.create(
                name=post_data['name'],
                username=post_data['username'],
                email=post_data['email'],
                password=hashed,
                hireDate=post_data['hire-date']
            )
            return new_user
        return errors


class User(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    hireDate = models.DateField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return self.name
