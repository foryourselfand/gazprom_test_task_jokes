=======================
Задание: Сервис шуток
=======================

.. image:: https://img.shields.io/pypi/v/gazprom_test_task_jokes.svg
        :target: https://pypi.python.org/pypi/gazprom_test_task_jokes

.. image:: https://img.shields.io/travis/foryourselfand/gazprom_test_task_jokes.svg
        :target: https://travis-ci.com/foryourselfand/gazprom_test_task_jokes

.. image:: https://readthedocs.org/projects/gazprom-test-task-jokes/badge/?version=latest
        :target: https://gazprom-test-task-jokes.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/foryourselfand/gazprom_test_task_jokes/shield.svg
     :target: https://pyup.io/repos/github/foryourselfand/gazprom_test_task_jokes/
     :alt: Updates

* Документация: https://gazprom-test-task-jokes.readthedocs.io.


Цели задания
------------
Показать умение ведения полного пайпалайна разработки Web API, что включает в себя: разработку сервера, документацию, тестирование и развертку системы.

Задача
------
Написать многопользовательский REST-сервис предоставляющий следующие эндпоинты:

1. Регистрация пользователя. Пользователь должен иметь возможность передать желаемый username, при этом он должен быть уникальным (другой пользователь не может зарегистрироваться с таким же именем).
2. Создать шутку, передав её сервису и сохранить в список “моих” шуток.
3. Сгенерировать шутку, получив её от внешнего сервиса и сохранить в список “моих” шуток.
4. Получить шутку по ID. При этом нельзя получить шутку другого пользователя.
5. Посмотреть список “моих” шуток.
6. Обновить текст своей шутки.
7. Удалить свою шутку.

Сервис должен также сохранять информацию о запросах - время обращения, данные пользователя, адрес пользователя.


В качестве генератора шуток можно использовать любой публично доступный API. Например, geek-jokes ( https://geek-jokes.sameerkumar.website/api ).

Техническое задание к приложению
--------------------------------

1. Приложение должно быть написано на Python 3.
2. Приложение должно представлять из себя REST API интерфейс для работы с шутками.
3. Приложение должно быть покрыто тестам.
4. Приложение должно быть подготовлено к локальной сборке и развертыванию с использованием Docker.
5. В приложение должны быть внедрены пайалайны для CI/CD, в частности автоматизированный прогон тестов и обновление testcov badge, сборка приложения в контейнер, развертывание приложения на сервере.
6. Приложение должно сопровождаться документацией.
7. Исходный код приложения необходимо предоставить в виде ссылки на GitHub / GitLab.
8. В качестве хранилища данных предлагается использовать технологии Elasticstash

Credits
-------

This package was created with Cookiecutter_ and the `harshanarayana/cookiecutter-sanic`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`harshanarayana/cookiecutter-sanic`: https://github.com/harshanarayana/cookiecutter-sanic


This project enables automated version management using bumpversion_ and gitchangelog_ projects.

.. _bumpversion: https://github.com/peritus/bumpversion
.. _gitchangelog: https://github.com/vaab/gitchangelog

