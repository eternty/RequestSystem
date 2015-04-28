# coding=utf-8
from django.utils import timezone
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _
# from django.contrib.auth.models import User


class MyUserManager(BaseUserManager):

    def _create_user(self, username, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(username=username, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password,
                                 True, True, **extra_fields)


class Company(models.Model):
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    manager = models.ForeignKey('System_User', related_name='manager_of', blank=True, null=True)
    focus = models.ForeignKey('System_User', related_name='focus_of', blank=True, null=True)


class User_type(models.Model):
    name = models.CharField(max_length=20)
    info = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class System_User(AbstractBaseUser, PermissionsMixin):
    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = u'Пользователь'
        verbose_name_plural = u'Пользователи'
        ordering = ('-date_joined', )

    email = models.EmailField(_('email address'), max_length=100, unique=True)
    username = models.CharField(_('username'), max_length=50, unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    patronymic = models.CharField(max_length=30)

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    phone = models.CharField(max_length=15)
    company = models.ForeignKey(Company, null=True)
    usertype = models.ForeignKey(User_type, null=True)
    place = models.CharField(max_length=30)

    def __unicode__(self):
        return self.username

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        full_name = '%s %s %s' % (self.first_name, self.middle_name, self.last_name)
        return full_name.strip()


class Contract(models.Model):
    number = models.CharField(max_length=15)
    company = models.ForeignKey(Company)
    begin_date = models.DateField(auto_now=False, auto_now_add=False)
    finish_date = models.DateField(auto_now=False, auto_now_add=False)
    resume = models.CharField(max_length=200)


class Request_status(models.Model):
    name = models.CharField(max_length=30)
    info = models.CharField(max_length=100)


class Request_type(models.Model):
    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=15)
    info = models.CharField(max_length=100)


class Request_priority(models.Model):
    name = models.CharField(max_length=15)
    info = models.CharField(max_length=100)


class Equipment(models.Model):
    name = models.CharField(max_length=30)
    serial = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    contract = models.ForeignKey(Contract)
    description = models.CharField(max_length=100)


class Normative_time(models.Model):
    reqtype = models.ForeignKey(Request_type)
    priority = models.ForeignKey(Request_priority)
    status = models.ForeignKey(Request_status)
    time_value = models.TimeField(auto_now=False, auto_now_add=False)


class Groups_engineer(models.Model):
    name = models.CharField(max_length=30)
    head = models.ForeignKey(System_User, blank=True, null=True)
    info = models.CharField(max_length=100)


class Specialization(models.Model):
    engineer = models.ForeignKey(System_User)
    group = models.ForeignKey(Groups_engineer)


class Request(models.Model):
    company = models.ForeignKey(Company)
    creator = models.ForeignKey(System_User, related_name='creator_of')
    reqtype = models.ForeignKey(Request_type)
    priority = models.ForeignKey(Request_priority)
    header = models.CharField(max_length=30)
    info = models.TextField(max_length=200)
    status = models.ForeignKey(Request_status)
    dispatcher = models.ForeignKey(System_User, blank=True, null=True, related_name='dispatcher_of')
    group = models.ForeignKey(Groups_engineer, blank=True, null=True)
    engineer = models.ForeignKey(System_User, blank=True, null=True, related_name='engineer_of')
    createtime = models.TimeField(auto_now=False, auto_now_add=True)
    REQUEST_MARKS = (
        ('EF', 'Engineer_fault'),
        ('DF', 'Disp_fault'),
        ('ED', 'Disp_engineer_faults'),
        ('OK', 'All in time')
    )
    mark = models.CharField(max_length=2, choices=REQUEST_MARKS, default='OK')
    equipment = models.ForeignKey(Equipment, blank=True, null=True)
    approvement = models.BooleanField(default=False)
    solution = models.CharField(max_length=250)


class Execution_time(models.Model):
    request = models.ForeignKey(Request)
    rstatus = models.ForeignKey(Request_status)
    start_exectime = models.TimeField(auto_now=False, auto_now_add=False)
    finish_exectime = models.TimeField(auto_now=False, auto_now_add=False)


class Comment(models.Model):
    author = models.ForeignKey(System_User)
    content = models.CharField(max_length=250)
    request = models.ForeignKey(Request)
    date_time = models.DateTimeField(auto_now=False, auto_now_add=True, blank=True, null=True)


class Replacement(models.Model):
    crashed = models.ForeignKey(Equipment, related_name='crash')
    replace = models.ForeignKey(Equipment, related_name='replace')


class Storage(models.Model):
    equipment = models.ForeignKey(Equipment, related_name='storaged')
    income_date = models.DateField(auto_now=False, auto_now_add=True)
    outcome_date = models.DateField(auto_now=False, auto_now_add=False)
    target_equipment = models.ForeignKey(Equipment, related_name='replaced')


	

