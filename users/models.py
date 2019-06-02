from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password, is_password_usable

class CustomAccountManager(BaseUserManager):
    def create_user(self, email, sid, name, password):
        user = self.model(email=email, sid=sid, name=name, password=password)
        # user.shown_name = name + '#' + sid[-4:]
        user.set_password(password)
        user.is_staff = False
        user.is_superuser = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, sid, name, password):
        user = self.create_user(email=email, sid=sid, name=name, password=password)
        # user.shown_name = name + '#' + sid[-4:]
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, email_):
        print(email_)
        return self.get(email=email_)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name = "이메일")
    sid = models.CharField(unique=True, max_length=10, primary_key=True, verbose_name = "학번")
    name = models.CharField(max_length=20, verbose_name = "닉네임")
    # shown_name = models.CharField(max_length=24)
    rank = models.IntegerField(default=0, verbose_name = "레벨")
    point = models.IntegerField(default=0, verbose_name = "포인트")
    is_staff = models.BooleanField(default=False, verbose_name = "관리자 여부")
    review_count = models.IntegerField(default=0, verbose_name = "작성 리뷰 수")
    # review_today = models.IntegerField(default=0, verbose_name = "오늘 작성 리뷰 수")
    REQUIRED_FIELDS = ['sid', 'name']
    USERNAME_FIELD = 'email'

    objects = CustomAccountManager()

    def get_short_name(self):
        return self.email

    def natural_key(self):
        return self.email

    # def get_shown_name(self):
    #     return self.shown_name

    def __str__(self):
        return self.email
    
    def get_lvl(self):
        return 'lv.' + str(self.point//500)
    
    def get_show_profile(self):
        return 'lv.' + str(self.point//500) + ' ' + self.name

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
    
