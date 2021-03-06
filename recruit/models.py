from django.db import models
from django.contrib.auth import get_user_model
from users.models import *
import ulid

class LocationModel(models.Model):
    location = models.CharField(verbose_name="地域",max_length=64, null=False, blank=False)
    class Meta:
        db_table = "location"
    
    def __str__(self):
        return self.location


class IndustryModel(models.Model):
    industry = models.CharField(verbose_name="業界",max_length=64, null=False, blank=False)
    class Meta:
        db_table = "industry"
    
    def __str__(self):
        return self.industry

class SectorModel(models.Model):
    sector = models.CharField(verbose_name="業種",max_length=64, null=False, blank=False)
    class Meta:
        db_table = "sector"
    
    def __str__(self):
        return self.sector


class ItemModel(models.Model):
    id = models.CharField(max_length=32, default=ulid.new, primary_key=True, editable=False)
    name = models.CharField(verbose_name="求人題名",max_length=256, null=False, blank=False)#title
    sub_title = models.CharField(verbose_name="求人題名補助短文",max_length=256, null=True, blank=True)
    location = models.ForeignKey(LocationModel, verbose_name="勤務地", null=True, blank=True,on_delete=models.SET_DEFAULT, default=1 )
    company = models.ForeignKey(CompanyUser, verbose_name="企業", db_column="company_id", on_delete=models.CASCADE, null=False, blank=False)
    description = models.TextField(verbose_name="仕事内容",null=True, blank=True)
    feature_flag = models.IntegerField(verbose_name="おすすめ求人フラグ", blank=False, default=0)
    employment_status = models.CharField(verbose_name="雇用形態",max_length=64, null=True, blank=True)
    industry = models.ForeignKey(IndustryModel, verbose_name="業界", null=True, blank=True,on_delete=models.SET_DEFAULT, default=1 )
    sector = models.ForeignKey(SectorModel, verbose_name="職種", null=True, blank=True,on_delete=models.SET_DEFAULT, default=1 )
    salary = models.IntegerField(verbose_name="給料", null=True, blank=True)
    # 勤務時間
    # 休日・休暇
    # 待遇・福利厚生
    # 求めている人材
    # 採用人数
    # 選考内容
    # 応募締切
    created_at = models.DateTimeField(verbose_name="作成日時", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新日時", auto_now=True)
    deleted_at = models.DateTimeField(verbose_name="削除日時", blank=True,null=True)

    class Meta:
        verbose_name = "求人"
        verbose_name_plural = "求人"
        db_table = "item"

    def __str__(self):
        return self.name
        



class UserFavoriteItemModel(models.Model):
    id = models.CharField(max_length=32, default=ulid.new, primary_key=True, editable=False)
    #no = models.CharField(max_length=32, default=0, editable=False)
    item = models.ForeignKey(ItemModel, db_column="item_id", on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(get_user_model(), db_column="user_id", on_delete=models.CASCADE, null=False, blank=False)
    created_at = models.DateTimeField(verbose_name="作成日時", auto_now_add=True)
    delete_flg = models.IntegerField(verbose_name="削除フラグ", blank=True, default=0)
    
    class Meta:
        verbose_name = "求職者から求人へのいいね"
        verbose_name_plural = "求職者から求人へのいいね"
        db_table = "user_favorite_item"


    def __str__(self):
        return self.id
    
    # def save(self, *args, **kwargs):
    #     self.no= self.no + 1
    #     super().save(*args, **kwargs)  # Call the "real" save() method.
        