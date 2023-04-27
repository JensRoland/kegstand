from unittest import mock

from kegstandcli.cli.build import build_api

# build_api(config: dict, verbose: bool, project_dir: str, module_build_dir: str):


@mock.patch("shutil.copyfile", mock.Mock())
@mock.patch("shutil.copytree", mock.Mock())
def test_build_calls_poetry_export(fp):
    fp.keep_last_process(True)
    fp.register(["poetry", "export", fp.any()])
    fp.register(["pip", "install", "-r", fp.any()])

    config = {"api": {"entrypoint": "api.lambda.handler"}}
    project_dir = "./test_project_dir"
    module_build_dir = "./test_project_dir/dist/api_src"
    build_api(config, False, project_dir, module_build_dir)

    assert fp.call_count(["poetry", "export", fp.any()]) == 1
    assert fp.call_count(["pip", "install", "-r", fp.any()]) == 1
