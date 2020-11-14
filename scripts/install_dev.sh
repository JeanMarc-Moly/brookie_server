#!/bin/sh

conda env create\
 --file envs/base/environment.prod.yml\
 --prefix .python_env

conda env update\
 --file envs/base/environment.dev.yml\
 --prefix .python_env
