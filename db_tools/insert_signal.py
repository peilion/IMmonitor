from motors.models import CurrentSignalPack, Motor, Uphase, Vphase, Wphase
import os
import datetime
import numpy as np
import scipy.io as sio

SAMPLING_RATE = 20480
ROOT_PATHS = [r"F:\Motor fusion\30HzData", r"F:\Motor fusion\40HzData", r"F:\Motor fusion\50HzData"]
j = 1
PHASE_SHIFT = [228, 171, 137]

for root_path, shift in zip(ROOT_PATHS, PHASE_SHIFT):
    target_motor = Motor.objects.get(name='Motor#' + str(j))
    files = os.listdir(root_path)
    for file in files:
        loadtext = root_path + '/' + file
        data = sio.loadmat(loadtext)['data'][500000:1000000, 0]
        for i in range(10):
            signal_pack = CurrentSignalPack.objects.create(motor=target_motor,
                                                           sampling_rate=SAMPLING_RATE)
            Uphase.objects.create(signal_pack=signal_pack,
                                  signal=data[1000 + i * 10000 - shift: 1000 + i * 10000 + 8192 - shift].tostring())
            Vphase.objects.create(signal_pack=signal_pack,
                                  signal=data[1000 + i * 10000: 1000 + i * 10000 + 8192].tostring())
            Wphase.objects.create(signal_pack=signal_pack,
                                  signal=data[1000 + i * 10000 + shift: 1000 + i * 10000 + 8192 + shift].tostring())

    initial_datetime = datetime.datetime(2016, 1, 1, 0, 0, 0, 0)
    signal_packs = CurrentSignalPack.objects.filter(motor=target_motor)
    for signal in signal_packs:
        signal.time = initial_datetime
        signal.save()
        initial_datetime += datetime.timedelta(days=1)
    j = j + 1
