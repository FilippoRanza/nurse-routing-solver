#! /usr/bin/python

# Copyright (c) 2019 Filippo Ranza <filipporanza@gmail.com>

from collections import namedtuple
from .file_utils import load_instance


instance_obj = namedtuple('Instance', 
['nurses', 'nurse_work', 'hub_distances', 'patient_distances', 'services', 'patients', 'base_time'])


def parse_instance(file_name):
    instance = load_instance(file_name)

    out = instance_obj(
        nurses = instance['NURSES'],
        nurse_work = instance['NURSES_WORK_TIME'],
        hub_distances = instance['HUB_DISTANCE'],
        patient_distances = instance['PATIENTS_DISTANCE'],
        services = instance['SERVICES'],
        patients = [i['REQUEST'] for i in  instance['PATIENTS']],
        base_time = instance['BASE_TIME_SLOT']
    )

    return out