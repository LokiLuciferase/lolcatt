# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/LokiLuciferase/lolcatt/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                  |    Stmts |     Miss |   Cover |   Missing |
|-------------------------------------- | -------: | -------: | ------: | --------: |
| lolcatt/\_\_init\_\_.py               |        3 |        0 |    100% |           |
| lolcatt/app.py                        |       18 |        2 |     89% |    29, 36 |
| lolcatt/casting/\_\_init\_\_.py       |        0 |        0 |    100% |           |
| lolcatt/casting/caster.py             |       80 |       41 |     49% |40-52, 54, 59-64, 78-96, 104-105, 114-119, 127, 135, 144-155, 166 |
| lolcatt/cli.py                        |       17 |       17 |      0% |      2-45 |
| lolcatt/ui/\_\_init\_\_.py            |        0 |        0 |    100% |           |
| lolcatt/ui/caster\_static.py          |        6 |        0 |    100% |           |
| lolcatt/ui/lolcatt\_controls.py       |       72 |       30 |     58% |61, 66-77, 81-86, 90-93, 97, 101, 105-108, 112-115 |
| lolcatt/ui/lolcatt\_device\_info.py   |       29 |       12 |     59% |18-23, 26-27, 30, 33, 36-37, 40 |
| lolcatt/ui/lolcatt\_playback\_info.py |       33 |       16 |     52% |18-29, 32-33, 36, 39, 42, 45 |
| lolcatt/ui/lolcatt\_progress.py       |       47 |       24 |     49% |20-23, 26-29, 37-43, 46-47, 52-62, 65 |
| lolcatt/ui/lolcatt\_url\_input.py     |       20 |        7 |     65% |16-20, 23, 26 |
| lolcatt/utils/\_\_init\_\_.py         |        0 |        0 |    100% |           |
| lolcatt/utils/utils.py                |       25 |       22 |     12% |14-19, 24-43 |
|                             **TOTAL** |  **350** |  **171** | **51%** |           |


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