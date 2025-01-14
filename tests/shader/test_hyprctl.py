import subprocess
from pathlib import Path

import pytest

from hyprshade.shader import hyprctl


@pytest.mark.requires_hyprland()
def test_hyprctl(shader_path: Path):
    hyprctl.set_screen_shader(str(shader_path))
    assert hyprctl.get_screen_shader() == str(shader_path)

    hyprctl.clear_screen_shader()
    assert hyprctl.get_screen_shader() is None


@pytest.mark.usefixtures("_mock_hyprctl_failure")
def test_hyprctl_failure():
    with pytest.raises(hyprctl.HyprctlError):
        hyprctl.get_screen_shader()

    with pytest.raises(hyprctl.HyprctlError):
        hyprctl.set_screen_shader("")


@pytest.mark.usefixtures("_mock_hyprctl_invalid_json")
def test_json_error():
    with pytest.raises(hyprctl.HyprctlJSONError):
        hyprctl.get_screen_shader()


@pytest.mark.usefixtures("_mock_hyprctl_json_no_str")
def test_json_no_str():
    with pytest.raises(hyprctl.HyprctlJSONError):
        hyprctl.get_screen_shader()


@pytest.fixture()
def _mock_hyprctl_failure(monkeypatch: pytest.MonkeyPatch):
    def _subprocess_run_failure(args, **kwargs) -> subprocess.CompletedProcess:
        raise subprocess.CalledProcessError(1, args)

    monkeypatch.setattr(hyprctl.subprocess, "run", _subprocess_run_failure)


@pytest.fixture()
def _mock_hyprctl_invalid_json(monkeypatch: pytest.MonkeyPatch):
    def _subprocess_run_invalid_json(args, **kwargs) -> subprocess.CompletedProcess:
        return subprocess.CompletedProcess(
            args=args,
            returncode=0,
            stdout='{"str": "test}',
            stderr="",
        )

    monkeypatch.setattr(hyprctl.subprocess, "run", _subprocess_run_invalid_json)


@pytest.fixture()
def _mock_hyprctl_json_no_str(monkeypatch: pytest.MonkeyPatch):
    def _subprocess_run_no_str(args, **kwargs) -> subprocess.CompletedProcess:
        return subprocess.CompletedProcess(
            args=args, returncode=0, stdout='{"int": 1}', stderr=""
        )

    monkeypatch.setattr(hyprctl.subprocess, "run", _subprocess_run_no_str)
