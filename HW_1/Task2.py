import subprocess
import string

def execute_command_and_check_output(command, text_to_find, word_mode=False):
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)

        if result.returncode == 0:
            if word_mode:      # Режим поиска слов
                words_in_output = [''.join(c for c in word if c not in string.punctuation) for word in result.stdout.split()]
                return text_to_find in words_in_output
            else:
                return text_to_find in result.stdout   # Режим поиска текста
        else:
            return False
    except Exception as e:
        print(f"Ошибка при выполнении команды: {e}")
        return False

# Пример использования функции в режиме поиска текста
command_to_execute = "ls -l" 
text_to_find_in_output = "HW_1"

result = execute_command_and_check_output(command_to_execute, text_to_find_in_output)
print(result)

# Пример использования функции в режиме поиска слов
command_to_execute = "echo 'This is an example sentence.'"
word_to_find_in_output = "example"

result_word_mode = execute_command_and_check_output(command_to_execute, word_to_find_in_output, word_mode=True)
print(result_word_mode)