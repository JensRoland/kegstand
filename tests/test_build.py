from unittest import mock
from pytest_subprocess import FakeProcess

from kegstandcli.cli.build import build_api

# build_api(config: dict, verbose: bool, project_dir: str, module_build_dir: str):


@mock.patch("shutil.copyfile", mock.Mock())
@mock.patch("shutil.copytree", mock.Mock())
def test_build_calls_uv_pip_compile(fake_process: FakeProcess):
    fake_process.keep_last_process(True)
    fake_process.register(["uv", "pip", "compile", fake_process.any()])
    fake_process.register(["uv", "pip", "install", "-r", fake_process.any()])

    config = {"api": {"entrypoint": "api.lambda.handler"}}
    project_dir = "./test_project_dir"
    module_build_dir = "./test_project_dir/dist/api_src"
    build_api(config, False, project_dir, module_build_dir)

    assert fake_process.call_count(["uv", "pip", "compile", fake_process.any()]) == 1
    assert fake_process.call_count(["uv", "pip", "install", "-r", fake_process.any()]) == 1
