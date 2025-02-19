# DevTime

**English:**  
DevTime is an intelligent task scheduler for developers that operates via a command-line interface (CLI). It optimizes your work schedule by taking into account your personalized settings such as working hours, break intervals, and task priorities. DevTime helps you dynamically plan your day based on the current time and pending tasks.

**Українська:**  
DevTime — це інтелектуальний планувальник завдань для розробників, який працює через командний рядок (CLI). Він оптимізує ваш робочий графік, враховуючи ваші персональні налаштування (робочі години, інтервали перерв та пріоритети завдань). DevTime допомагає динамічно планувати ваш день, виходячи з поточного часу та невиконаних завдань.

---

## Features / Функціональності

**English:**
- **Task Input:** Easily add tasks with a name, duration, deadline (in flexible formats), and priority.
- **Dynamic Scheduling:** Generates a work schedule based on the current time and your personal settings.
- **Task Splitting:** If a task’s duration exceeds your maximum concentration period, it is split into multiple sessions with breaks in between.
- **Interactive Mode:** Enter commands in real time to quickly manage tasks.
- **Customization:** Update configuration files to change your working hours, concentration time, and break durations.

**Українська:**
- **Введення завдань:** Легко додавайте завдання із зазначенням назви, тривалості, дедлайну (у гнучких форматах) та пріоритету.
- **Динамічне планування:** Генерує робочий розклад на основі поточного часу та ваших налаштувань.
- **Розбиття завдань:** Якщо тривалість завдання перевищує максимально допустимий час концентрації, воно розбивається на декілька сесій з перервами.
- **Інтерактивний режим:** Вводьте команди в реальному часі для швидкого керування завданнями.
- **Налаштування:** Легко змінюйте конфігураційні файли для коригування робочих годин, часу концентрації та тривалості перерв.

---

## Getting Started / Як розпочати

### Prerequisites / Попередні вимоги
- Python 3.6+
- pip

### Installation from Source / Встановлення з вихідного коду

1. **Clone the repository / Клонуйте репозиторій:**
    ```bash
    git clone https://github.com/nmokh/devtime.git
    cd devtime
    ```

2. **Create a virtual environment (recommended) / Створіть віртуальне середовище (рекомендовано):**
    ```bash
    python -m venv venv
    source venv/bin/activate   # Linux/macOS
    venv\Scripts\activate      # Windows
    ```

3. **Install dependencies / Встановіть залежності:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Install the package locally / Локально встановіть пакет:**
    ```bash
    pip install .
    ```

---

## Usage / Використання

### Running DevTime / Запуск DevTime
**English:**
After installation, simply type:
```bash
devtime
```
This launches the interactive mode where you can type commands such as add, plan, edit, delete, and complete. You can also run individual commands like:

- **Add a task:**
    ```bash
    devtime add "Write report" 2.5 "10 15:00" 2
    ```
    This adds a task "Write report" with a duration of 2.5 hours, a deadline on the 10th day of the current month at 15:00, and a priority of medium.
- **Plan your schedule:**
    ```bash
    devtime plan
    ```
    This command dynamically generates and displays a schedule for today. The schedule starts from the current time if the workday is already underway; otherwise, it starts at the beginning of the workday.
- **Interactive Mode:**
    Just run:
    ```bash
    devtime
    ```
    and you’ll enter a mode where you can input commands one-by-one.

**Українська:**
Після встановлення достатньо набрати:
```bash
devtime
```
Це запустить інтерактивний режим, де ви можете вводити команди, такі як add, plan, edit, delete та complete. Також можна запускати окремі команди, наприклад:

- **Додати завдання:**
    ```bash
    devtime add "Написати звіт" 2.5 "10 15:00" 2
    ```
    Це додає завдання "Написати звіт" тривалістю 2.5 години, дедлайн встановлюється на 10 число поточного місяця о 15:00, а пріоритет – medium.
- **Планувати розклад:**
    ```bash
    devtime plan
    ```
    Ця команда динамічно генерує та відображає розклад на сьогодні. Якщо робочий день уже триває, розклад починається від поточного часу, інакше – з початку робочого дня.
- **Інтерактивний режим:**
    Просто запустіть:
    ```bash
    devtime
    ```
    і ви потрапите в режим, де можна вводити команди послідовно.

### Changing Configuration Files / Зміна файлів конфігурації

**English:**
DevTime reads its configuration from a file named config.json. To adjust your working hours, break durations, maximum concentration time, or other settings, simply edit the config.json file in the root directory of the project. After making changes, you can re-run the scheduling command to see the updated schedule.

**Українська:**
DevTime використовує для налаштувань файл config.json. Щоб змінити свої робочі години, тривалість перерв, максимальний час концентрації чи інші налаштування, відредагуйте файл config.json у кореневій теці проєкту. Після внесення змін знову запустіть команду планування, щоб побачити оновлений розклад.

---

## Contributing / Внесок

**English:**
Contributions are always welcome! If you have ideas or improvements, please fork the repository, create your feature branch, commit your changes, and open a pull request.

**Українська:**
Внески завжди вітаються! Якщо у вас є ідеї або покращення, будь ласка, форкуйте репозиторій, створюйте окрему гілку, комітуйте зміни та відкривайте pull request.

---

## License / Ліцензія

This project is licensed under the MIT License.
Цей проєкт ліцензовано за MIT License.

---

## Author / Автор

Developed by Nazar Mokh (Назар Мох)

---

## Acknowledgements / Подяки

Special thanks to the open-source community and to everyone supporting Ukraine during these challenging times.
Особлива подяка спільноті open-source та всім, хто підтримує Україну в ці важкі часи.

---

## 📖 Want to learn more? / Хочете дізнатися більше?  
Check out the [Extended Documentation](docs/Extended_Documentation.md) for a detailed overview of features, installation, architecture, and future improvements.  

Ознайомтеся з [Розширеною документацією](docs/Extended_Documentation.md), щоб дізнатися більше про функціональність, встановлення, архітектуру та майбутні покращення.
