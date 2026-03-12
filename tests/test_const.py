"""Tests for the constants module."""

from poolcop.const import (
    AUX_LABEL_NAMES,
    AUX_LABEL_POOL_LIGHT,
    AUX_LABEL_SUCTION_VALVE,
    AUX_MAX_CCU,
    AUX_MAX_XM8,
    INPUT_FUNC_AVAILABLE,
    INPUT_FUNC_AUX_CONTROL,
    INPUT_FUNC_NAMES,
)


def test_aux_label_names_complete():
    """Test that all aux labels 0-27 have names."""
    for i in range(28):
        assert i in AUX_LABEL_NAMES, f"Missing name for aux label {i}"


def test_aux_label_constants_range():
    """Test aux label constant boundaries."""
    assert AUX_LABEL_POOL_LIGHT == 0
    assert AUX_LABEL_SUCTION_VALVE == 27


def test_aux_port_constraints():
    """Test port constraint constants."""
    assert AUX_MAX_CCU == 7
    assert AUX_MAX_XM8 == 15


def test_input_func_names_complete():
    """Test that all input functions 0-20 have names."""
    for i in range(21):
        assert i in INPUT_FUNC_NAMES, f"Missing name for input function {i}"


def test_input_func_constants_range():
    """Test input function constant boundaries."""
    assert INPUT_FUNC_AVAILABLE == 0
    assert INPUT_FUNC_AUX_CONTROL == 20
