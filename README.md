# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/LokiLuciferase/lolcatt/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                  |    Stmts |     Miss |   Cover |   Missing |
|-------------------------------------- | -------: | -------: | ------: | --------: |
| lolcatt/\_\_init\_\_.py               |        3 |        0 |    100% |           |
| lolcatt/app.py                        |       23 |        5 |     78% |17, 37-38, 42-43 |
| lolcatt/casting/\_\_init\_\_.py       |        0 |        0 |    100% |           |
| lolcatt/casting/caster.py             |       76 |       37 |     51% |51-69, 77-78, 88-100, 102, 107-114, 122, 130, 139-150, 161 |
| lolcatt/cli.py                        |       17 |       17 |      0% |      2-45 |
| lolcatt/ui/\_\_init\_\_.py            |        0 |        0 |    100% |           |
| lolcatt/ui/lolcatt\_controls.py       |       81 |       47 |     42% |41-49, 52-55, 58-69, 73-78, 82-85, 89, 93, 97-100, 104-107, 110-119 |
| lolcatt/ui/lolcatt\_device\_info.py   |       29 |       15 |     48% |13-15, 18-23, 26-27, 30, 33, 36-37, 42 |
| lolcatt/ui/lolcatt\_playback\_info.py |       33 |       19 |     42% |13-15, 18-29, 32-33, 36, 39, 42, 45 |
| lolcatt/ui/lolcatt\_progress.py       |       53 |       33 |     38% |19-22, 25-31, 34-37, 40-48, 51-52, 57-67, 70 |
| lolcatt/ui/lolcatt\_url\_input.py     |       20 |       10 |     50% |9-11, 15-19, 22, 25 |
| lolcatt/utils/\_\_init\_\_.py         |        0 |        0 |    100% |           |
| lolcatt/utils/utils.py                |       25 |       22 |     12% |14-19, 24-43 |
|                             **TOTAL** |  **360** |  **205** | **43%** |           |


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/LokiLuciferase/lolcatt/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/LokiLuciferase/lolcatt/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/LokiLuciferase/lolcatt/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/LokiLuciferase/lolcatt/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2FLokiLuciferase%2Flolcatt%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/LokiLuciferase/lolcatt/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.