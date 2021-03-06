# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

# pylint: skip-file

import os
import boto3
from pytest import fixture, raises
from .stubs import event, step_functions
from mock import Mock
from stepfunctions import StepFunctions


@fixture
def cls():
    cls = StepFunctions(
        boto3,
        '11111111111',
        'eu-central-1',
        ['region-1', 'region-2'],
        '99999999999'
    )

    cls.client = Mock()
    return cls


def test_statemachine_start(cls):
    cls.client.start_execution.return_value = step_functions.stub_start_execution
    cls._start_statemachine()
    assert cls.execution_arn == 'some_execution_arn'


def test_statemachine_get_status(cls):
    cls.client.describe_execution.return_value = step_functions.stub_describe_execution
    cls._start_statemachine()
    cls._fetch_statemachine_status()
    cls.execution_status == 'RUNNING'


def test_wait_failed_state_machine_execution(cls):
    step_functions.stub_describe_execution["status"] = "FAILED"
    cls.client.describe_execution.return_value = step_functions.stub_describe_execution
    cls._start_statemachine()
    cls._fetch_statemachine_status()
    assert cls.execution_status == 'FAILED'
    with raises(Exception):
        cls._wait_state_machine_execution()
