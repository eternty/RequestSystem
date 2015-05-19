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
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = u'Компания'
        verbose_name_plural = u'Компании'

    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    manager = models.ForeignKey('System_User', related_name='manager_of', blank=True, null=True)
    focus = models.ForeignKey('System_User', related_name='focus_of', blank=True, null=True)

    def get_manager_name(self):
        managername= self.manager.get_full_name()
        return managername

    def get_manager_contacts(self):
        managercontacts = '%s %s' % (self.manager.phone, self.manager.email)
        return managercontacts
    def get_focus_name(self):
        focusname = self.focus.get_full_name()
        return focusname
    def get_focus_contacts(self):
        focuscontacts = '%s %s' % (self.focus.phone, self.focus.email)
        return


class User_type(models.Model):
    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'Тип пользователя'
        verbose_name_plural = u'Типы пользователей'

    name = models.CharField(max_length=20)
    info = models.CharField(max_length=100)


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
    patronymic = models.CharField(max_length=30, blank=True, null=True)

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    phone = models.CharField(max_length=15)
    company = models.ForeignKey(Company, null=True)
    usertype = models.ForeignKey(User_type, null=True)
    place = models.CharField(max_length=30, null=True, blank=True)

    def __unicode__(self):
        return self.username

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        full_name = '%s %s %s' % (self.first_name, self.patronymic, self.last_name)
        return full_name.strip()
    #def get_specialization(self):
      #  specials = Specialization.objects.filter(engineer = self)
      #   return specials
    def get_specialization(self):
        return Specialization.objects.filter(engineer = self).values('group')


class Contract(models.Model):
    def __unicode__(self):
        return self.number
    def get_company(self):
        return self.company
    class Meta:
        verbose_name = u'Договор'
        verbose_name_plural = u'Договоры'

    number = models.CharField(max_length=15)
    company = models.ForeignKey(Company)
    begin_date = models.DateField(auto_now=False, auto_now_add=False)
    finish_date = models.DateField(auto_now=False, auto_now_add=False)
    resume = models.CharField(max_length=200)


class Request_status(models.Model):
    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'Статус заявки'
        verbose_name_plural = u'Статусы заявок'

    name = models.CharField(max_length=30)
    info = models.CharField(max_length=100)


class Request_type(models.Model):
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = u'Тип заявки'
        verbose_name_plural = u'Типы заявок'

    name = models.CharField(max_length=15)
    info = models.CharField(max_length=100)


class Request_priority(models.Model):
    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'Приоритет заявки'
        verbose_name_plural = u'Приоритеты заявок'

    name = models.CharField(max_length=15)
    info = models.CharField(max_length=100)


class Equipment(models.Model):
    def __unicode__(self):
        full_recognition =  '%s %s' % (self.name, self.serial)
        return full_recognition.strip()

    def get_replacement(self):
        return Replacement.objects.filter(crashed = self).values('replace')

    class Meta:
        verbose_name = u'Оборудование'
        verbose_name_plural = u'Оборудование'

    name = models.CharField(max_length=30)
    serial = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    contract = models.ForeignKey(Contract)
    description = models.CharField(max_length=100)


class Normative_time(models.Model):

    def __unicode__(self):
        return self.time_value

    class Meta:
        verbose_name = u'Норматив на статус'
        verbose_name_plural = u'Нормативы на статусы'

    reqtype = models.ForeignKey(Request_type)
    priority = models.ForeignKey(Request_priority)
    status = models.ForeignKey(Request_status)
    time_value = models.TimeField(auto_now=False, auto_now_add=False)


class Groups_engineer(models.Model):
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = u'Группа инженеров'
        verbose_name_plural = u'Группы инженеров'

    name = models.CharField(max_length=30)
    head = models.ForeignKey(System_User, blank=True, null=True)
    info = models.CharField(max_length=100)


class Specialization(models.Model):
    class Meta:
        verbose_name = u'Специализация инженера'
        verbose_name_plural = u'Специализации инженеров'

    engineer = models.ForeignKey(System_User)
    group = models.ForeignKey(Groups_engineer)


class Request(models.Model):

    #def __unicode__(self):
    #   return self.id
    def exist_solution(self):
        return self.solution.__sizeof__()

    class Meta:
        verbose_name = u'Заявка'
        verbose_name_plural = u'Заявки'

    company = models.ForeignKey(Company,  verbose_name="компания")
    creator = models.ForeignKey(System_User, related_name='creator_of', verbose_name="заявитель" )
    reqtype = models.ForeignKey(Request_type, verbose_name="тип заявки")
    priority = models.ForeignKey(Request_priority, verbose_name="приоритет")
    header = models.CharField(max_length=30, verbose_name="заголовок")
    info = models.TextField(max_length=200, verbose_name="краткая информация")
    status = models.ForeignKey(Request_status, verbose_name="статус")
    dispatcher = models.ForeignKey(System_User, blank=True, null=True, related_name='dispatcher_of', verbose_name="диспетчер")
    group = models.ForeignKey(Groups_engineer, blank=True, null=True, verbose_name= "группа")
    engineer = models.ForeignKey(System_User, blank=True, null=True, related_name='engineer_of',verbose_name="исполнитель")
    createtime = models.DateTimeField(default=timezone.now)
    REQUEST_MARKS = (
        ('EF', 'Engineer_fault'),
        ('DF', 'Disp_fault'),
        ('ED', 'Disp_engineer_faults'),
        ('OK', 'All in time')
    )
    mark = models.CharField(max_length=2, choices=REQUEST_MARKS, default='OK', verbose_name="оценка выполнения SLA")
    equipment = models.ForeignKey(Equipment, blank=True, null=True, verbose_name="оборудование ")
    approvement = models.BooleanField(default=False, verbose_name= "подтверждение")
    solution = models.CharField(max_length=250, null=True, blank=True, verbose_name="решение")


class Execution_time(models.Model):
    def __unicode__(self):
        return self.start_exectime
    class Meta:
        verbose_name = u'Время выполнения на статус'
        verbose_name_plural = u'Время выполнения на статусы'

    request = models.ForeignKey(Request)
    rstatus = models.ForeignKey(Request_status)
    start_exectime = models.TimeField(default=timezone.now)
    finish_exectime = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True)


class Comment(models.Model):
    class Meta:
        verbose_name = u'Коммент'
        verbose_name_plural = u'Комменты'
    author = models.ForeignKey(System_User)
    content = models.CharField(max_length=250, verbose_name = "Комментарий")
    request = models.ForeignKey(Request)
    date_time = models.DateTimeField(default=timezone.now)


class Replacement(models.Model):
    class Meta:
        verbose_name = u' Функциональная замена'
        verbose_name_plural = u'Функциональная замена'

    crashed = models.ForeignKey(Equipment, related_name='crash')
    replace = models.ForeignKey(Equipment, related_name='replace')


class Storage(models.Model):
    class Meta:
        verbose_name = u'Учет оборудования'
        verbose_name_plural = u'Учет оборудования'
    equipment = models.ForeignKey(Equipment, related_name='storaged')
    income_date = models.DateField(auto_now=False, auto_now_add=True)
    outcome_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    target_equipment = models.ForeignKey(Equipment, related_name='replaced', null= True, blank= True)


	

