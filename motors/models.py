from django.db import models
from django.contrib.auth.models import User
from DjangoUeditor.models import UEditorField


class Asset(models.Model):
    """
    This is a abstract model
    """
    asset_status = (
        (0, 'Excellent'),
        (1, 'Good'),
        (2, 'Moderate'),
        (3, 'Poor'),
        (4, 'Offline'),
    )

    name = models.CharField(max_length=64, unique=True, verbose_name='Name of asset')
    sn = models.CharField(max_length=128, unique=True, verbose_name='Serial number')
    statu = models.SmallIntegerField(choices=asset_status, default=2, verbose_name='Asset statu')
    manufacturer = models.ForeignKey('Manufacturer', null=True, blank=True, on_delete=models.SET_NULL,
                                     verbose_name='Manufacturer')
    tags = models.ManyToManyField('Tag', blank=True, verbose_name='Tags')

    lr_time = models.DateTimeField(null=True, blank=True, verbose_name='Last repair/check date')
    pr_time = models.DateTimeField(null=True, blank=True, verbose_name='Purchase date')
    md_time = models.DateTimeField(auto_now=True, verbose_name='Modified date')
    cr_time = models.DateTimeField(auto_now_add=True, verbose_name='Created date')
    sr_time = models.DateTimeField(null=True, blank=True, verbose_name='Start running date')

    class Meta:
        abstract = True


class Motor(Asset):
    phase_number = models.SmallIntegerField(null=True, blank=True, verbose_name='Number of phases ')  # 相数
    pole_pairs_number = models.SmallIntegerField(null=True, blank=True, verbose_name='Number of pole_pairs ')  # 极对数
    turn_number = models.SmallIntegerField(null=True, blank=True, verbose_name='Number of turns ')  # 匝数
    rated_voltage = models.FloatField(null=True, blank=True, verbose_name='Rated voltage /V')  # 额定电压
    rated_speed = models.FloatField(null=True, blank=True, verbose_name='Rated speed /rpm')  # 额定转速
    memo = UEditorField(verbose_name=u"Memory", imagePath="motor/images/", width=1000, height=300,
                        filePath="motor/files/", default='')
    admin = models.ForeignKey(User, null=True, blank=True, verbose_name='Administrator', on_delete=models.SET_NULL)


class Bearing(Asset):
    motor = models.ForeignKey(Motor, on_delete=models.CASCADE, related_name='bearings')  # 一对一与机组共有资产表关联

    inner_race_diameter = models.FloatField(null=True, blank=True, verbose_name='Inner race diameter /mm')  # 内径
    inner_race_width = models.FloatField(null=True, blank=True, verbose_name='Inner race width /mm')  # 内圈宽度

    outter_race_diameter = models.FloatField(null=True, blank=True, verbose_name='Outter race diameter /mm')  # 外径
    outter_race_width = models.FloatField(null=True, blank=True, verbose_name='Outter race width /mm')  # 外圈宽度

    roller_diameter = models.FloatField(null=True, blank=True, verbose_name='Roller diameter /mm')  # 滚动体直径
    roller_number = models.SmallIntegerField(null=True, blank=True, verbose_name='Number of rollers')  # 滚动体个数
    contact_angle = models.FloatField(null=True, blank=True, verbose_name='Contact angle ')  # 接触角
    memo = UEditorField(verbose_name=u"Memory", imagePath="bearing/images/", width=1000, height=300,
                        filePath="bearing/files/", default='')


class Rotor(Asset):
    motor = models.ForeignKey(Motor, on_delete=models.CASCADE, related_name='rotors')  # 一对一与机组共有资产表关联
    length = models.FloatField(null=True, blank=True, verbose_name='Length /mm')  # 铁心长度
    outer_diameter = models.FloatField(null=True, blank=True, verbose_name='Outer diameter /mm')  # 外径
    inner_diameter = models.FloatField(null=True, blank=True, verbose_name='Inner diameter /mm')  # 内径
    slot_number = models.SmallIntegerField(null=True, blank=True, verbose_name='Number of slots')  # 槽数
    memo = UEditorField(verbose_name=u"Memory", imagePath="rotor/images/", width=1000, height=300,
                        filePath="rotor/files/", default='')


class Stator(Asset):
    motor = models.ForeignKey(Motor, on_delete=models.CASCADE, related_name='stators')  # 一对一与机组共有资产表关联
    length = models.FloatField(null=True, blank=True, verbose_name='Length /mm')  # 铁心长度
    outer_diameter = models.FloatField(null=True, blank=True, verbose_name='Outer diameter /mm')  # 外径
    inner_diameter = models.FloatField(null=True, blank=True, verbose_name='Inner diameter /mm')  # 内径
    slot_number = models.SmallIntegerField(null=True, blank=True, verbose_name='Number of slots')  # 槽数
    memo = UEditorField(verbose_name=u"Memory", imagePath="stator/images/", width=1000, height=300,
                        filePath="stator/files/", default='')


class Manufacturer(models.Model):
    name = models.CharField('Manufacturer name', max_length=64, unique=True)
    telephone = models.CharField('Telephone', max_length=30, blank=True, null=True)
    memo = models.CharField('Memory', max_length=128, blank=True, null=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=32, unique=True, verbose_name='Tag name')
    c_day = models.DateField(auto_now_add=True, verbose_name='Created time')

    def __str__(self):
        return self.name


class CurrentSignalPack(models.Model):
    time = models.DateTimeField(auto_now_add=True, verbose_name='Collected Time')
    motor = models.ForeignKey(Motor, on_delete=models.CASCADE, related_name='packs')
    sampling_rate = models.IntegerField(null=True, blank=True)


class phase(models.Model):
    signal = models.BinaryField(blank=False, null=False, verbose_name='Collected Signal vector')
    signal_pack = models.OneToOneField(CurrentSignalPack, verbose_name='Parent pack', on_delete=models.CASCADE)
    frequency = models.FloatField('PSF', default=0)
    amplitude = models.FloatField('AMP', default=0)
    initial_phase = models.FloatField('IPA',default=0)

    class Meta:
        abstract = True


class Uphase(phase):
    pass


class Vphase(phase):
    pass


class Wphase(phase):
    pass


class Feature(models.Model):
    signal_pack = models.OneToOneField(CurrentSignalPack, verbose_name='Parent pack', on_delete=models.CASCADE)
    rms = models.FloatField('U phase root-mean-square', default=0)
    thd = models.FloatField('Total harmonic distortion %', default=0)
    harmonics = models.BinaryField('1st-20th harmonic energy')
    max_current = models.FloatField('Maximum current value', default=0)
    min_current = models.FloatField('Minimum current value', default=0)
    fbrb = models.BinaryField('Frequencies of Broken rotor bar',null=True)
    class Meta:
        abstract = True


class Ufeature(Feature):
    pass


class Vfeature(Feature):
    pass


class Wfeature(Feature):
    pass


class SymComponent(models.Model):  # Only one phase syscomponents are calculated and stored
    signal_pack = models.OneToOneField(CurrentSignalPack, verbose_name='Parent pack', on_delete=models.CASCADE)
    n_sequence_rms = models.FloatField('Negative sequence root-mean-square', default=0)
    p_sequence_rms = models.FloatField('Positive sequence root-mean-square', default=0)
    z_sequence_rms = models.FloatField('Zero sequence root-mean-square', default=0)
    imbalance = models.FloatField('Current imbanlance %', default=0)


# class SpecEnvelope(models.Model):
#     signal_pack = models.OneToOneField(CurrentSignalPack, verbose_name='Parent pack', on_delete=models.CASCADE)
#     spec = models.BinaryField('Spectrum', blank=True, null=True)
#     env = models.BinaryField('Envelope', blank=True, null=True)
#     env_spec = models.BinaryField('Spectrum of Envelope', blank=True, null=True)
#
#     class Meta:
#         abstract = True
#
#
# class Uprocessed(SpecEnvelope):
#     pass
#
#
# class Vprocessed(SpecEnvelope):
#     pass
#
#
# class Wprocessed(SpecEnvelope):
#     pass


class WarningLog(models.Model):
    severity_choice = (
        (0, 'Attention'),
        (1, 'Serious'),

    )
    motor = models.ForeignKey(Motor, verbose_name='Related motor', on_delete=models.CASCADE)
    c_day = models.DateTimeField(auto_now_add=True, verbose_name='Created time')
    description = models.TextField(blank=False, null=False, verbose_name='Warning description')
    severity = models.SmallIntegerField(choices=severity_choice, null=True, blank=True,
                                        verbose_name='Warning severity')


class WeeklyRecord(models.Model):
    c_day = models.DateField(auto_now_add=True, verbose_name='Created time')
    description = UEditorField(verbose_name=u"Content", imagePath="weekly/images/", width=1000, height=300,
                               filePath="weekly/files/", default='')


class MonthlyRecord(models.Model):
    c_day = models.DateField(auto_now_add=True, verbose_name='Created time')
    description = UEditorField(verbose_name=u"Content", imagePath="monthly/images/", width=1000, height=300,
                               filePath="monthly/files/", default='')
