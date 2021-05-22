from pathlib import Path

BASE_ENV = Path("envs/base")
BASE_ENV_DEV = BASE_ENV / "environment.dev.yml"
BASE_ENV_PROD = BASE_ENV / "environment.prod.yml"

MAMBA = "mamba"
PYTHON_ENV = Path(".python_env")

PYTHON_BIN = PYTHON_ENV / "bin"
PYTHON_EXE = PYTHON_BIN / "python"
ISORT_EXE = PYTHON_BIN / "isort"
BLACK_EXE = PYTHON_BIN / "black"
UTEST_EXE = PYTHON_BIN / "unittest/__init__.py"
PYLINT_EXE = PYTHON_BIN / "pylint"
PYREVERSE_EXE = PYTHON_BIN / "pyreverse"

PYTHON_INCLUDE = PYTHON_ENV / "include"
GRAPHVIZ = PYTHON_INCLUDE / "graphviz/graphviz_version.h"

SRC = "src"
# TEST = "test"
DEPENDENCIES = "requirements.txt"


def task_base_env():
    return dict(
        file_dep=[BASE_ENV_PROD],
        actions=[
            ["git", "config", "core.hooksPath", ".git-hooks"],
            ["conda", "install", "-n", "base", "-c", "conda-forge", MAMBA, "--yes"],
            [
                MAMBA,
                "env",
                "update",
                "--quiet",
                # "--yes",
                "--file",
                BASE_ENV_PROD,
                "--prefix",
                PYTHON_ENV,
            ],
        ],
        targets=[PYTHON_EXE, UTEST_EXE],
        uptodate=[True],
    )


# conda create --name <envname> --file requirements.txt
def task_dev_env():
    return dict(
        file_dep=[PYTHON_EXE, BASE_ENV_DEV],
        actions=[
            [
                MAMBA,
                "env",
                "update",
                "--quiet",
                # "--yes",
                "--file",
                BASE_ENV_DEV,
                "--prefix",
                PYTHON_ENV,
            ]
        ],
        targets=[BLACK_EXE, ISORT_EXE, GRAPHVIZ, PYREVERSE_EXE, PYLINT_EXE],
        uptodate=[True],
    )


def task_env_upgrade():
    return dict(
        file_dep=[PYTHON_EXE],
        actions=[
            [MAMBA, "update", "--update-all", "--yes"],
        ],
    )


def task_env_freeze():
    return dict(
        file_dep=[PYTHON_EXE],
        actions=[
            [f""""{MAMBA}" list --export > "{DEPENDENCIES}".export"""],
            [f""""{MAMBA}" list --explicit > "{DEPENDENCIES}".explicit"""],
        ],
        targets=[DEPENDENCIES],
    )


def task_format():
    return dict(
        file_dep=[BLACK_EXE, ISORT_EXE],
        actions=[
            [ISORT_EXE, SRC],
            [BLACK_EXE, SRC],
            # [ISORT_EXE, TEST],
            # [BLACK_EXE, TEST],
            [BLACK_EXE, "dodo.py"],
        ],
        uptodate=[False],
    )


# def task_test():
#     return dict(
#         file_dep=[PYTHON_EXE, UTEST_EXE],
#         actions=[[PYTHON_EXE, "-m", "unittest", "discover", "--start-directory", TEST]],
#         uptodate=[False],
#     )


# def task_doc():
#     return dict(
#         file_dep=[GRAPHVIZ, PYREVERSE_EXE],
#         actions=[[PYREVERSE_EXE, "-o", "pdf", $SRC]],
#         # TODO: targets
#         uptodate=[False],
#     )


def task_lint():
    return dict(
        file_dep=[PYLINT_EXE],
        actions=[[PYLINT_EXE, SRC]],
        uptodate=[False],
    )
