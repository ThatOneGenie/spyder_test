# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Copyright © Spyder Project Contributors
#
# Licensed under the terms of the MIT License
# ----------------------------------------------------------------------------

"""Tests for the plugin."""

# Standard library imports
import os
import sys

# Third party imports
import pytest

# Local imports
from spyder.config.base import running_in_ci
from spyder.config.utils import is_anaconda
from spyder.plugins.maininterpreter.plugin import MainInterpreter


@pytest.fixture
def maininterpreter(qtbot):
    """Set up PathManager."""
    plugin = MainInterpreter(None)
    qtbot.addWidget(plugin.get_container())
    return plugin


@pytest.mark.skipif(not is_anaconda(), reason="Requires conda to be installed")
@pytest.mark.skipif(not running_in_ci(), reason="Only meant for CIs")
def test_conda_interpreters(maininterpreter, qtbot):
    """Test info from conda interpreters."""
    container = maininterpreter.get_container()
    container._interpreter = ''

    name_base = 'conda: base'
    name_test = 'conda: jedi-test-env'

    # Wait until envs are computed
    qtbot.wait(4000)

    # Update to the base conda environment
    path_base, version = container.envs[name_base]
    expected = 'conda: base ({})'.format(version)
    assert expected == container._get_env_info(path_base)

    # Update to the foo conda environment
    path_foo, version = container.envs[name_test]
    expected = 'conda: jedi-test-env ({})'.format(version)
    assert expected == container._get_env_info(path_foo)


def test_pyenv_interpreters(maininterpreter, qtbot):
    """Test info from pyenv interpreters."""
    container = maininterpreter.get_container()

    version = 'Python 3.6.6'
    name = 'pyenv: test'
    interpreter = os.sep.join(['some-other', 'bin', 'python'])
    container.envs = {name: (interpreter, version)}
    container.path_to_env = {interpreter: name}
    assert 'pyenv: test (Python 3.6.6)' == container._get_env_info(interpreter)


@pytest.mark.skipif(sys.platform != 'darwin', reason="Only valid on Mac")
def test_internal_interpreter(maininterpreter, qtbot, mocker):
    """Test info from internal interpreter."""
    container = maininterpreter.get_container()

    interpreter = os.sep.join(['Spyder.app', 'Contents', 'MacOS', 'Python'])
    name = 'system:'
    version = 'Python 3.6.6'
    container.envs = {name: (interpreter, version)}
    container.path_to_env = {interpreter: name}
    assert 'system: (Python 3.6.6)' == container._get_env_info(interpreter)
