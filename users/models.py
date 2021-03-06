from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db.models.fields import BLANK_CHOICE_DASH
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.mail import send_mail
import ulid

from app.const import USER_TYPE


class CustomUserManager(UserManager):
    '''
    Userを作成するための処理
    Userの項目が変更になっているので、こちらも変更の必要がある
    '''    
    
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    
    def create_user(self, email=None, password=None, **extra_fields):
        '''
        一般ユーザーを作成する処理
        '''
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    
    def create_superuser(self, email=None, password=None, **extra_fields):
        '''
        管理者ユーザーを作成する処理
        '''
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class NormalUser(models.Model):
    id = models.CharField(max_length=32, default=ulid.new, primary_key=True, editable=False) 
    first_name = models.CharField(_('名前'), max_length=32, blank=True)
    last_name = models.CharField(_('苗字'), max_length=32, blank=True)
    nickname = models.CharField(_('ニックネーム'), max_length=32, blank=True)
    gender = models.IntegerField(_('性別'), blank=True, default=0)
    phone_number = models.CharField(_('電話番号'), max_length=16, blank=True)
    address = models.TextField(_('住所'), blank=False)


    def __str__(self):
        return self.last_name + " " + self.first_name

    def is_blank(self):
        if not self.nickname:
            return True
        else:
            return False


    class Meta:
        verbose_name = "一般ユーザー"
        verbose_name_plural = "一般ユーザー"
        db_table = "normal_user"
        
        
class CompanyUser(models.Model):
    id = models.CharField(max_length=32, default=ulid.new, primary_key=True, editable=False) 
    company_name = models.CharField(_('法人名称'), max_length=32, blank=True)
    address = models.CharField(_('本社所在地'), max_length=256, blank=True)
    phone_number = models.CharField(_('電話番号'), max_length=16, blank=True)

    def __str__(self):
        return self.company_name

    def is_blank(self):
        if not self.company_name:
            return True
        else:
            return False

    class Meta:
        verbose_name = "企業ユーザー"
        verbose_name_plural = "企業ユーザー"
        db_table = "company_user"
        
    
class User(AbstractBaseUser, PermissionsMixin):
    '''
    カスタムUser
    AbstractBaseUser: 標準のUserモデル
    ※AbstractUserというモデルもあり、これを継承することもできるが、柔軟性が低くなるため非推奨(項目を追加するのみ等の微小なカスタマイズの場合はOK)
    PermissionsMixin: 権限関連のモデル
    '''    
    
    '''
    必須項目
    '''
    id = models.CharField(max_length=32, default=ulid.new, primary_key=True, editable=False) # idは推測されずらく重複しないように、ulidを使用する
    email = models.EmailField(_('メールアドレス'), blank=False, unique=True, db_index=True) 
    username = models.CharField(_('ユーザーネーム'), max_length=150, blank=True)
    user_type = models.IntegerField(_('ユーザータイプ'),  blank=False, default=0)
    normal_user = models.ForeignKey(NormalUser, db_column="normal_user_id" , blank=True, db_index=True, default=None, null=True, on_delete=models.SET_NULL)
    company_user = models.ForeignKey(CompanyUser,  db_column="company_user_id", blank=True, db_index=True, default=None, null=True, on_delete=models.SET_NULL)
    
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    
    # UserManagerを指定
    objects = CustomUserManager()

    '''
    カスタマイズ項目 必要な項目は以下のように追加する
    '''


    
    '''
    フィールド設定
    '''
    # emailの項目名を指定
    EMAIL_FIELD = 'email'
    # ログイン時にIDになる項目名を指定
    USERNAME_FIELD = 'email'
    # 必須入力とする項目名(USERNAME_FIELDに指定した項目は必ず指定する前提のため指定しない)
    REQUIRED_FIELDS = []
    
    
    class Meta:
        '''
        テーブル定義(基本は変更しない)
        '''
        verbose_name = _('ログイン用共通ユーザー')
        verbose_name_plural = _('ログイン用共通ユーザー')
        db_table = "auth_user"

    
    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)


    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def is_normal_user(self):
        return self.user_type == USER_TYPE.NORMAL_USER
    
    def is_company_user(self):
        return self.user_type == USER_TYPE.COMPANY_USER
    # def get_full_name(self):
    #     return self.last_name + " " + self.first_name


    # def get_short_name(self):
    #     return self.first_name
    

