# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/LokiLuciferase/lolcatt/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                          |    Stmts |     Miss |   Cover |   Missing |
|---------------------------------------------- | -------: | -------: | ------: | --------: |
| lolcatt/\_\_init\_\_.py                       |        3 |        0 |    100% |           |
| lolcatt/app.py                                |       41 |        2 |     95% |     69-70 |
| lolcatt/casting/\_\_init\_\_.py               |        0 |        0 |    100% |           |
| lolcatt/casting/caster.py                     |      186 |      111 |     40% |69-81, 85-88, 96-114, 120-130, 136-141, 147-164, 170-176, 185-190, 196, 204, 212, 220, 228, 236-237, 244-256, 258, 260, 275-283, 293, 301, 310, 313-314, 320-345, 354-365 |
| lolcatt/casting/youtube\_playlist\_handler.py |       19 |        8 |     58% |11-13, 30, 36-39 |
| lolcatt/cli.py                                |       30 |       30 |      0% |      2-67 |
| lolcatt/ui/\_\_init\_\_.py                    |        0 |        0 |    100% |           |
| lolcatt/ui/lolcatt\_controls.py               |      108 |       68 |     37% |48-51, 54-57, 60-73, 77-82, 86-89, 93-96, 100-103, 107-110, 114-117, 121-124, 128-131, 134-149 |
| lolcatt/ui/lolcatt\_device\_info.py           |       31 |       12 |     61% |18-23, 26-27, 30, 33, 36-37, 42 |
| lolcatt/ui/lolcatt\_devicelist.py             |       47 |       26 |     45% |15-18, 27-35, 38, 41-56, 59 |
| lolcatt/ui/lolcatt\_playback\_info.py         |       43 |       22 |     49% |20-34, 37-38, 41, 44, 47, 50, 55-57 |
| lolcatt/ui/lolcatt\_playlist.py               |       56 |       38 |     32% |13-15, 21-31, 34, 37-62, 65 |
| lolcatt/ui/lolcatt\_progress.py               |       64 |       34 |     47% |21-24, 28-34, 38-40, 49-58, 61-62, 67-77 |
| lolcatt/ui/lolcatt\_url\_input.py             |       46 |       20 |     57% |40, 46-48, 52-58, 62-67, 70, 73-74 |
| lolcatt/utils/\_\_init\_\_.py                 |        0 |        0 |    100% |           |
| lolcatt/utils/utils.py                        |       33 |       25 |     24% |17-21, 27-59 |
|                                     **TOTAL** |  **707** |  **396** | **44%** |           |


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