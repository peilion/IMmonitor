# users/adminx.py
__author__ = 'fpl'

import xadmin
from xadmin import views
from motors.models import Tag, WarningLog, WeeklyRecord, Manufacturer, Motor, Bearing, Rotor, Stator, CurrentSignalPack


class BaseSetting(object):
    # 添加主题功能
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    # 全局配置，后台管理标题和页脚
    site_title = "Induction motor monitoring - Admin site"
    site_footer = "IN PROGRESS"
    # 菜单收缩
    menu_style = "accordion"


class MotorAdmin(object):
    # 显示的列
    list_display = ["name", "sn", "statu", "phase_number", 'pole_pairs_number']
    # 可以搜索的字段
    search_fields = ['name', ]
    # 列表页可以直接编辑的
    list_editable = ["status", ]
    # 过滤器
    list_filter = ["name", "sn", "statu", "phase_number", 'pole_pairs_number']
    # 富文本编辑器
    style_fields = {"memo": "ueditor",'tag':'m2m_transfer'}

    # 在添加商品的时候可以添加商品图片
    class BearingInline(object):
        model = Bearing
        exclude = ["lr_time", 'pr_time', 'md_time', 'cr_time', 'sr_time']
        extra = 1
        style = 'tab'

    class RotorInline(object):
        model = Rotor
        exclude = ["lr_time", 'pr_time', 'md_time', 'cr_time', 'sr_time']
        extra = 1
        style = 'tab'

    class StatorInline(object):
        model = Stator
        exclude = ["lr_time", 'pr_time', 'md_time', 'cr_time', 'sr_time']
        extra = 1
        style = 'tab'

    inlines = [BearingInline, RotorInline, StatorInline]


class ManufacturerAdmin(object):
    list_display = ['name', 'telephone']
    list_filter = ['name', 'telephone']
    search_fields = ['name']


class TagAdmin(object):
    style_fields = {'motor': 'm2m_transfer'}


class CurrentSignalPackAdmin(object):
    list_display = ['time', 'motor', 'sampling_rate']
    list_filter = ['time', 'motor', 'sampling_rate']


class WarningLogAdmin(object):
    list_display = ["severity", "motor", "c_day"]


class WeeklyRecordAdmin(object):
    list_display = ["c_day"]
    style_fields = {"description": "ueditor"}


xadmin.site.register(Motor, MotorAdmin)
xadmin.site.register(Manufacturer, ManufacturerAdmin)
xadmin.site.register(Tag, TagAdmin)
xadmin.site.register(CurrentSignalPack, CurrentSignalPackAdmin)

xadmin.site.register(WarningLog, WarningLogAdmin)
xadmin.site.register(WeeklyRecord, WeeklyRecordAdmin)

xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
