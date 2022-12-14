import os
import re

from .conftest import root_dir


class TestWorkflow:

    def test_workflow(self):
        backend_basename = 'foodgram_workflow'

        yaml = f'{backend_basename}.yaml'
        is_yaml = yaml in os.listdir(os.path.join(root_dir, ".github", "workflows"))

        yml = f'{backend_basename}.yml'
        is_yml = yml in os.listdir(os.path.join(root_dir, ".github", "workflows"))

        if not is_yaml and not is_yml:
            assert False, (
                f'В каталоге {root_dir} не найден файл с описанием workflow '
                f'{yaml} или {yml}.\n'
                '(Это нужно для проверки тестами на платформе)'
            )

        if is_yaml and is_yml:
            assert False, (
                f'В каталоге {root_dir} не должно быть двух файлов {backend_basename} '
                'с расширениями .yaml и .yml\n'
                'Удалите один из них'
            )

        filename = yaml if is_yaml else yml

        try:
            with open(f'{os.path.join(root_dir, ".github", "workflows", filename)}', 'r') as f:
                foodgram = f.read()
        except FileNotFoundError:
            assert False, f'Проверьте, что добавили файл {filename} в каталог {root_dir} для проверки'

        assert (
                re.search(r'on:\s*push:\s*branches:\s*-\smaster', foodgram) or
                'on: [push]' in foodgram or
                'on: push' in foodgram
        ), f'Проверьте, что добавили действие при пуше в файл {filename}'
        assert 'pytest' in foodgram, f'Проверьте, что добавили pytest в файл {filename}'
        assert 'appleboy/ssh-action' in foodgram, f'Проверьте, что добавили деплой в файл {filename}'
        assert 'appleboy/telegram-action' in foodgram, (
            'Проверьте, что настроили отправку telegram сообщения '
            f'в файл {filename}'
        )
