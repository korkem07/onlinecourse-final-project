# Django OnlineCourse — Final Project (7 tasks)

Учебная версия проекта для заданий Coursera IBM: Django Application Development with SQL and Databases.
Работающий сайт позволяет зарегистрироваться, записаться на курс, пройти тест и увидеть результат.

## Запуск в Visual Studio Code (Windows)

1. Установить Python 3.10+ с python.org (отметить Add python.exe to PATH).
2. Распаковать архив `onlinecourse_final_project.zip` и выбрать в VS Code File > Open Folder: `onlinecourse_final_project`.
3. Открыть Terminal > New Terminal (PowerShell). Терминал должен находиться там же, где manage.py.
4. Ввести:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py makemigrations
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py seed_demo
.\.venv\Scripts\python.exe manage.py createsuperuser
.\.venv\Scripts\python.exe manage.py runserver
```

Если `py` не найден, вместо `py -m venv .venv` использовать `python -m venv .venv`.
При `createsuperuser` установить свой логин и пароль — они НЕ должны попасть на скриншоты.

5. Открыть **http://127.0.0.1:8000/admin/** — авторизоваться суперпользователем.
6. Сделать настоящий скриншот админки, чтобы были видны Authentication and Authorization + Onlinecourse. Сохранить **03-admin-site.png**.
7. В новой вкладке открыть **http://127.0.0.1:8000/onlinecourse/**.
8. Нажать **Sign up**, создать обычного пользователя, затем в курсе нажать **Enroll**, **Enter course**.
9. Выбрать правильные ответы: **A Python web framework** и **Work with a database using Python objects**.
10. Нажать **Submit exam**. Откроется страница с **Congratulations!**, **100.0%** и **Exam results**.
11. Сделать настоящий скриншот результата **07-final.png**.

## Отправка в GitHub

Создать свой новый **PUBLIC** репозиторий `onlinecourse-final-project` на GitHub, без галочки Create README.
Затем в терминале с папкой проекта:

```powershell
git init
git add .
git commit -m "Complete Django OnlineCourse final project"
git branch -M main
git remote add origin https://github.com/ВАШ_USERNAME/onlinecourse-final-project.git
git push -u origin main
```

Важно: `git push` требует входа в GitHub. Если Git не установлен — скачать с git-scm.com.

## Ссылки для сдачи

Заменить `ВАШ_USERNAME` на GitHub username:

1. `https://github.com/ВАШ_USERNAME/onlinecourse-final-project/blob/main/onlinecourse/models.py`
2. `https://github.com/ВАШ_USERNAME/onlinecourse-final-project/blob/main/onlinecourse/admin.py`
3. Загрузить настоящий скриншот `03-admin-site.png`
4. `https://github.com/ВАШ_USERNAME/onlinecourse-final-project/blob/main/onlinecourse/templates/onlinecourse/course_details_bootstrap.html`
5. `https://github.com/ВАШ_USERNAME/onlinecourse-final-project/blob/main/onlinecourse/views.py`
6. `https://github.com/ВАШ_USERNAME/onlinecourse-final-project/blob/main/onlinecourse/urls.py`
7. Загрузить настоящий скриншот `07-final.png`

## Проверка

Остановить сервер CTRL+C. Для тестов выполнить:

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test
```

## Предупреждение

Это локальный учебный проект, НЕ production deployment. DEBUG=True, development SECRET_KEY и SQLite подходят только для теста на компьютере. Не коммитить .env, пароли или базу данных.

Основано на публичном учебном IBM starter (Apache-2.0):
https://github.com/ibm-developer-skills-network/final-cloud-app-with-database
