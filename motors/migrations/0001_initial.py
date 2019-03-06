# Generated by Django 2.0.2 on 2019-03-05 13:07

import DjangoUeditor.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bearing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='Name of asset')),
                ('sn', models.CharField(max_length=128, unique=True, verbose_name='Serial number')),
                ('statu', models.SmallIntegerField(choices=[(0, 'Excellent'), (1, 'Good'), (2, 'Moderate'), (3, 'Poor'), (4, 'Offline')], default=2, verbose_name='Asset statu')),
                ('lr_time', models.DateTimeField(blank=True, null=True, verbose_name='Last repair/check date')),
                ('pr_time', models.DateTimeField(blank=True, null=True, verbose_name='Purchase date')),
                ('md_time', models.DateTimeField(auto_now=True, verbose_name='Modified date')),
                ('cr_time', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('sr_time', models.DateTimeField(blank=True, null=True, verbose_name='Start running date')),
                ('inner_race_diameter', models.FloatField(blank=True, null=True, verbose_name='Inner race diameter /mm')),
                ('inner_race_width', models.FloatField(blank=True, null=True, verbose_name='Inner race width /mm')),
                ('outter_race_diameter', models.FloatField(blank=True, null=True, verbose_name='Outter race diameter /mm')),
                ('outter_race_width', models.FloatField(blank=True, null=True, verbose_name='Outter race width /mm')),
                ('roller_diameter', models.FloatField(blank=True, null=True, verbose_name='Roller diameter /mm')),
                ('roller_number', models.SmallIntegerField(blank=True, null=True, verbose_name='Number of rollers')),
                ('contact_angle', models.FloatField(blank=True, null=True, verbose_name='Contact angle ')),
                ('memo', DjangoUeditor.models.UEditorField(default='', verbose_name='Memory')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CurrentSignalPack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='Collected Time')),
                ('sampling_rate', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='Manufacturer name')),
                ('telephone', models.CharField(blank=True, max_length=30, null=True, verbose_name='Telephone')),
                ('memo', models.CharField(blank=True, max_length=128, null=True, verbose_name='Memory')),
            ],
        ),
        migrations.CreateModel(
            name='MonthlyRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_day', models.DateField(auto_now_add=True, verbose_name='Created time')),
                ('description', DjangoUeditor.models.UEditorField(default='', verbose_name='Content')),
            ],
        ),
        migrations.CreateModel(
            name='Motor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='Name of asset')),
                ('sn', models.CharField(max_length=128, unique=True, verbose_name='Serial number')),
                ('statu', models.SmallIntegerField(choices=[(0, 'Excellent'), (1, 'Good'), (2, 'Moderate'), (3, 'Poor'), (4, 'Offline')], default=2, verbose_name='Asset statu')),
                ('lr_time', models.DateTimeField(blank=True, null=True, verbose_name='Last repair/check date')),
                ('pr_time', models.DateTimeField(blank=True, null=True, verbose_name='Purchase date')),
                ('md_time', models.DateTimeField(auto_now=True, verbose_name='Modified date')),
                ('cr_time', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('sr_time', models.DateTimeField(blank=True, null=True, verbose_name='Start running date')),
                ('phase_number', models.SmallIntegerField(blank=True, null=True, verbose_name='Number of phases ')),
                ('pole_pairs_number', models.SmallIntegerField(blank=True, null=True, verbose_name='Number of pole_pairs ')),
                ('turn_number', models.SmallIntegerField(blank=True, null=True, verbose_name='Number of turns ')),
                ('rated_voltage', models.FloatField(blank=True, null=True, verbose_name='Rated voltage /V')),
                ('rated_speed', models.FloatField(blank=True, null=True, verbose_name='Rated speed /rpm')),
                ('memo', DjangoUeditor.models.UEditorField(default='', verbose_name='Memory')),
                ('admin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Administrator')),
                ('manufacturer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='motors.Manufacturer', verbose_name='Manufacturer')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Rotor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='Name of asset')),
                ('sn', models.CharField(max_length=128, unique=True, verbose_name='Serial number')),
                ('statu', models.SmallIntegerField(choices=[(0, 'Excellent'), (1, 'Good'), (2, 'Moderate'), (3, 'Poor'), (4, 'Offline')], default=2, verbose_name='Asset statu')),
                ('lr_time', models.DateTimeField(blank=True, null=True, verbose_name='Last repair/check date')),
                ('pr_time', models.DateTimeField(blank=True, null=True, verbose_name='Purchase date')),
                ('md_time', models.DateTimeField(auto_now=True, verbose_name='Modified date')),
                ('cr_time', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('sr_time', models.DateTimeField(blank=True, null=True, verbose_name='Start running date')),
                ('length', models.FloatField(blank=True, null=True, verbose_name='Length /mm')),
                ('outer_diameter', models.FloatField(blank=True, null=True, verbose_name='Outer diameter /mm')),
                ('inner_diameter', models.FloatField(blank=True, null=True, verbose_name='Inner diameter /mm')),
                ('slot_number', models.SmallIntegerField(blank=True, null=True, verbose_name='Number of slots')),
                ('memo', DjangoUeditor.models.UEditorField(default='', verbose_name='Memory')),
                ('manufacturer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='motors.Manufacturer', verbose_name='Manufacturer')),
                ('motor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='motors.Motor')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Stator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='Name of asset')),
                ('sn', models.CharField(max_length=128, unique=True, verbose_name='Serial number')),
                ('statu', models.SmallIntegerField(choices=[(0, 'Excellent'), (1, 'Good'), (2, 'Moderate'), (3, 'Poor'), (4, 'Offline')], default=2, verbose_name='Asset statu')),
                ('lr_time', models.DateTimeField(blank=True, null=True, verbose_name='Last repair/check date')),
                ('pr_time', models.DateTimeField(blank=True, null=True, verbose_name='Purchase date')),
                ('md_time', models.DateTimeField(auto_now=True, verbose_name='Modified date')),
                ('cr_time', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('sr_time', models.DateTimeField(blank=True, null=True, verbose_name='Start running date')),
                ('length', models.FloatField(blank=True, null=True, verbose_name='Length /mm')),
                ('outer_diameter', models.FloatField(blank=True, null=True, verbose_name='Outer diameter /mm')),
                ('inner_diameter', models.FloatField(blank=True, null=True, verbose_name='Inner diameter /mm')),
                ('slot_number', models.SmallIntegerField(blank=True, null=True, verbose_name='Number of slots')),
                ('memo', DjangoUeditor.models.UEditorField(default='', verbose_name='Memory')),
                ('manufacturer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='motors.Manufacturer', verbose_name='Manufacturer')),
                ('motor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='motors.Motor')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SymComponent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nagative_sequence', models.TextField(blank=True, null=True, verbose_name='Negative sequence waveform')),
                ('positive_sequence', models.TextField(blank=True, null=True, verbose_name='Positive sequence waveform')),
                ('zero_sequence', models.TextField(blank=True, null=True, verbose_name='Zero sequence waveform')),
                ('n_sequence_rms', models.FloatField(default=0, verbose_name='Negative sequence root-mean-square')),
                ('p_sequence_rms', models.FloatField(default=0, verbose_name='Positive sequence root-mean-square')),
                ('z_sequence_rms', models.FloatField(default=0, verbose_name='Zero sequence root-mean-square')),
                ('imbalance', models.FloatField(default=0, verbose_name='Current imbanlance %')),
                ('signal_pack', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='motors.CurrentSignalPack', verbose_name='Parent pack')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='Tag name')),
                ('c_day', models.DateField(auto_now_add=True, verbose_name='Created time')),
            ],
        ),
        migrations.CreateModel(
            name='Ufeature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rms', models.FloatField(default=0, verbose_name='U phase root-mean-square')),
                ('thd', models.FloatField(default=0, verbose_name='Total harmonic distortion %')),
                ('harmonics', models.TextField(verbose_name='1st-20th harmonic energy')),
                ('fbrb', models.FloatField(default=0, verbose_name='Broken rotor bar characteristic frequency')),
                ('fbpfi', models.FloatField(default=0, verbose_name='Defect inner race bearing characteristic frequency')),
                ('fbpfo', models.FloatField(default=0, verbose_name='Defect outter race bearing characteristic frequency')),
                ('fbsf', models.FloatField(default=0, verbose_name='Defect rolling element characteristic frequency')),
                ('signal_pack', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='motors.CurrentSignalPack', verbose_name='Parent pack')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Uphase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('signal', models.TextField(verbose_name='Collected Signal vector')),
                ('complex_signal', models.TextField(blank=True, null=True, verbose_name='Complex signal')),
                ('signal_pack', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='motors.CurrentSignalPack', verbose_name='Parent pack')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Uprocessed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spec', models.TextField(blank=True, null=True, verbose_name='Spectrum')),
                ('env', models.TextField(blank=True, null=True, verbose_name='Envelope')),
                ('env_spec', models.TextField(blank=True, null=True, verbose_name='Spectrum of Envelope')),
                ('signal_pack', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='motors.CurrentSignalPack', verbose_name='Parent pack')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Vfeature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rms', models.FloatField(default=0, verbose_name='U phase root-mean-square')),
                ('thd', models.FloatField(default=0, verbose_name='Total harmonic distortion %')),
                ('harmonics', models.TextField(verbose_name='1st-20th harmonic energy')),
                ('fbrb', models.FloatField(default=0, verbose_name='Broken rotor bar characteristic frequency')),
                ('fbpfi', models.FloatField(default=0, verbose_name='Defect inner race bearing characteristic frequency')),
                ('fbpfo', models.FloatField(default=0, verbose_name='Defect outter race bearing characteristic frequency')),
                ('fbsf', models.FloatField(default=0, verbose_name='Defect rolling element characteristic frequency')),
                ('signal_pack', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='motors.CurrentSignalPack', verbose_name='Parent pack')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Vphase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('signal', models.TextField(verbose_name='Collected Signal vector')),
                ('complex_signal', models.TextField(blank=True, null=True, verbose_name='Complex signal')),
                ('signal_pack', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='motors.CurrentSignalPack', verbose_name='Parent pack')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Vprocessed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spec', models.TextField(blank=True, null=True, verbose_name='Spectrum')),
                ('env', models.TextField(blank=True, null=True, verbose_name='Envelope')),
                ('env_spec', models.TextField(blank=True, null=True, verbose_name='Spectrum of Envelope')),
                ('signal_pack', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='motors.CurrentSignalPack', verbose_name='Parent pack')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WarningLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_day', models.DateTimeField(auto_now_add=True, verbose_name='Created time')),
                ('description', models.TextField(verbose_name='Warning description')),
                ('severity', models.SmallIntegerField(blank=True, choices=[(0, 'Attention'), (1, 'Serious')], null=True, verbose_name='Warning severity')),
                ('motor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='motors.Motor', verbose_name='Related motor')),
            ],
        ),
        migrations.CreateModel(
            name='WeeklyRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_day', models.DateField(auto_now_add=True, verbose_name='Created time')),
                ('description', DjangoUeditor.models.UEditorField(default='', verbose_name='Content')),
            ],
        ),
        migrations.CreateModel(
            name='Wfeature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rms', models.FloatField(default=0, verbose_name='U phase root-mean-square')),
                ('thd', models.FloatField(default=0, verbose_name='Total harmonic distortion %')),
                ('harmonics', models.TextField(verbose_name='1st-20th harmonic energy')),
                ('fbrb', models.FloatField(default=0, verbose_name='Broken rotor bar characteristic frequency')),
                ('fbpfi', models.FloatField(default=0, verbose_name='Defect inner race bearing characteristic frequency')),
                ('fbpfo', models.FloatField(default=0, verbose_name='Defect outter race bearing characteristic frequency')),
                ('fbsf', models.FloatField(default=0, verbose_name='Defect rolling element characteristic frequency')),
                ('signal_pack', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='motors.CurrentSignalPack', verbose_name='Parent pack')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Wphase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('signal', models.TextField(verbose_name='Collected Signal vector')),
                ('complex_signal', models.TextField(blank=True, null=True, verbose_name='Complex signal')),
                ('signal_pack', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='motors.CurrentSignalPack', verbose_name='Parent pack')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Wprocessed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spec', models.TextField(blank=True, null=True, verbose_name='Spectrum')),
                ('env', models.TextField(blank=True, null=True, verbose_name='Envelope')),
                ('env_spec', models.TextField(blank=True, null=True, verbose_name='Spectrum of Envelope')),
                ('signal_pack', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='motors.CurrentSignalPack', verbose_name='Parent pack')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='stator',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='motors.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='rotor',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='motors.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='motor',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='motors.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='currentsignalpack',
            name='motor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='motors.Motor'),
        ),
        migrations.AddField(
            model_name='bearing',
            name='manufacturer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='motors.Manufacturer', verbose_name='Manufacturer'),
        ),
        migrations.AddField(
            model_name='bearing',
            name='motor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='motors.Motor'),
        ),
        migrations.AddField(
            model_name='bearing',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='motors.Tag', verbose_name='Tags'),
        ),
    ]
