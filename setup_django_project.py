import os
import subprocess
import sys


def create_virtualenv(env_name="venv"):
    """Создаем виртуальное окружение"""
    if not os.path.exists(env_name):
        print("Создание виртуального окружения...")
        subprocess.run([sys.executable, "-m", "venv", env_name])
    else:
        print(f"Виртуальное окружение '{env_name}' уже существует.")


def install_django():
    """Устанавливаем Django"""
    print("Установка Django...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "django"])


def create_django_project(project_name):
    """Создаем Django-проект"""
    if not os.path.exists(project_name):
        print(f"Создание Django-проекта '{project_name}'...")
        subprocess.run(["django-admin", "startproject", project_name])
    else:
        print(f"Проект '{project_name}' уже существует.")


def run_django_project(project_name):
    """Запускаем Django-проект"""
    manage_py_path = os.path.join(os.getcwd(), project_name, "manage.py")

    if os.path.exists(manage_py_path):
        print(f"Запуск Django-проекта '{project_name}'...")
        subprocess.run([sys.executable, manage_py_path, "runserver"])
    else:
        print(
            f"Не удалось найти manage.py в {project_name}. Проверь название проекта и путь."
        )


def freeze_requirements():
    """Сохраняем зависимости в файл requirements.txt"""
    print("Сохранение зависимостей в requirements.txt...")
    with open("requirements.txt", "w") as f:
        subprocess.run([sys.executable, "-m", "pip", "freeze"], stdout=f)


if __name__ == "__main__":
    project_name = "my_project"  # Название проекта

    create_virtualenv()  # Создаем виртуальное окружение
    install_django()  # Устанавливаем Django
    create_django_project(project_name)  # Создаем проект
    freeze_requirements()  # Замораживаем зависимости
    run_django_project(project_name)  # Запускаем сервер
