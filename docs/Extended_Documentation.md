# Extended Documentation for DevTime

## 1. Introduction / Вступ

### English
DevTime is an innovative command-line task scheduler designed specifically for developers. In today's fast-paced development environment, managing tasks efficiently is essential for maintaining productivity and reducing stress. DevTime helps you optimize your workday by dynamically generating schedules based on your personal configuration—such as working hours, break durations, and task priorities.

This documentation provides an in-depth look at DevTime's features, design principles, and implementation details. You will learn how to install the tool, configure your settings, and use its interactive and dynamic scheduling capabilities. The aim is to offer clear guidance that enables you to quickly integrate DevTime into your workflow and customize it to your needs.

### Українська
DevTime — це інноваційний планувальник завдань, розроблений спеціально для розробників, який працює через командний рядок. У сучасному швидкоплинному середовищі розробки ефективне управління завданнями є ключовим для підтримки продуктивності та зниження стресу. DevTime допомагає оптимізувати ваш робочий день, динамічно формуючи розклади на основі ваших персональних налаштувань, таких як робочі години, тривалість перерв та пріоритети завдань.

Ця документація містить детальний огляд функціоналу, принципів дизайну та технічних аспектів реалізації DevTime. Ви дізнаєтесь, як встановити програму, налаштувати конфігурацію та використовувати її інтерактивний режим і динамічне планування. Мета документації — надати чіткі інструкції, які допоможуть швидко інтегрувати DevTime у ваш робочий процес та адаптувати його до власних потреб.

---

## 2. Features and Benefits / Функціональності та переваги

### English

DevTime is designed to simplify task management for developers by providing a robust, flexible, and dynamic scheduling solution. Here are the key features and benefits of using DevTime:

- **Flexible Task Input:** Easily add tasks with a name, duration, deadline (supporting various formats), and priority.  
- **Dynamic Scheduling:** DevTime generates a daily work schedule based on your current time and personalized settings such as working hours and break intervals.  
- **Task Splitting:** If a task’s duration exceeds your maximum concentration period, it is automatically split into manageable sessions with breaks, helping you avoid burnout.  
- **Interactive Mode:** Run DevTime in interactive mode to enter commands in real time for adding, editing, or completing tasks, making task management seamless.  
- **Customization:** Configure your work schedule by editing the configuration file (e.g., `config.json`), so that the generated schedule aligns perfectly with your daily routine.  
- **Cross-Platform Support:** As a Python-based CLI application, DevTime works on Windows, Linux, and macOS, ensuring accessibility in any terminal environment.

---

### Українська

DevTime розроблено для спрощення управління завданнями розробників, надаючи надійне, гнучке та динамічне рішення для планування. Ось основні функції та переваги використання DevTime:

- **Гнучке введення завдань:** Легко додавайте завдання із зазначенням назви, тривалості, дедлайну (підтримуються різні формати) та пріоритету.  
- **Динамічне планування:** DevTime генерує щоденний розклад роботи на основі поточного часу та ваших персональних налаштувань, таких як робочі години та інтервали перерв.  
- **Розбиття завдань:** Якщо тривалість завдання перевищує максимально допустимий час концентрації, воно автоматично розбивається на керовані сесії з перервами, що допомагає уникнути перевтоми.  
- **Інтерактивний режим:** Запускайте DevTime в інтерактивному режимі, де можна вводити команди в реальному часі для додавання, редагування або виконання завдань, що робить управління максимально зручним.  
- **Налаштування:** Ви можете налаштувати свій робочий графік, максимальний час концентрації та тривалість перерв, відредагувавши конфігураційний файл (наприклад, `config.json`), що забезпечує ідеальне відповідність розкладу вашим потребам.  
- **Крос-платформеність:** DevTime – це CLI-застосунок на Python, який працює на Windows, Linux та macOS, що гарантує доступність у будь-якому термінальному середовищі.

---

## 3. Installation and Setup / Встановлення та налаштування

### English

#### Prerequisites:
- Python 3.6 or higher
- pip

#### Installation from Source:
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/nmokh/devtime.git
   cd devtime
   ```

2. **Create a Virtual Environment (Recommended):**
   ```bash
   python -m venv venv
   # On Linux/macOS:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install the Package Locally:**
   ```bash
   pip install .
   ```

5. **Configuration:**
   DevTime reads its configuration from a file named `config.json` located in the project root. To customize your working hours, maximum concentration time, and break durations, simply open and edit `config.json`. For example:
   ```json
   {
       "work_hours": {
           "Monday": {"start": 9, "end": 17},
           "Tuesday": {"start": 9, "end": 17},
           "Wednesday": {"start": 9, "end": 17},
           "Thursday": {"start": 9, "end": 17},
           "Friday": {"start": 9, "end": 17},
           "Saturday": {"start": null, "end": null},
           "Sunday": {"start": null, "end": null}
       },
       "max_concentration_hours": 1,
       "min_break_minutes": 10
   }
   ```
   Adjust these values as needed to match your daily routine.

6. **Running the Application:**
   To launch DevTime in interactive mode, simply type:
   ```bash
   devtime
   ```
   Alternatively, you can run:
   ```bash
   python -m devtime.cli
   ```

---

### Українська

#### Попередні вимоги:
- Python 3.6 або вище
- pip

#### Встановлення з вихідного коду:
1. **Клонуйте репозиторій:**
   ```bash
   git clone https://github.com/nmokh/devtime.git
   cd devtime
   ```

2. **Створіть віртуальне середовище (рекомендовано):**
   ```bash
   python -m venv venv
   # На Linux/macOS:
   source venv/bin/activate
   # На Windows:
   venv\Scripts\activate
   ```

3. **Встановіть залежності:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Локально встановіть пакет:**
   ```bash
   pip install .
   ```

5. **Налаштування:**
   DevTime використовує для налаштувань файл `config.json`, який знаходиться у кореневій теці проєкту. Щоб змінити свої робочі години, максимальний час концентрації та тривалість перерв, відкрийте файл `config.json` і внесіть потрібні зміни. Наприклад:
   ```json
   {
       "work_hours": {
           "Monday": {"start": 9, "end": 17},
           "Tuesday": {"start": 9, "end": 17},
           "Wednesday": {"start": 9, "end": 17},
           "Thursday": {"start": 9, "end": 17},
           "Friday": {"start": 9, "end": 17},
           "Saturday": {"start": null, "end": null},
           "Sunday": {"start": null, "end": null}
       },
       "max_concentration_hours": 1,
       "min_break_minutes": 10
   }
   ```
   Налаштуйте значення відповідно до вашого робочого ритму.

6. **Запуск програми:**
   Щоб запустити DevTime в інтерактивному режимі, достатньо набрати:
   ```bash
   devtime
   ```
   Або, альтернативно:
   ```bash
   python -m devtime.cli
   ```

---

## 4. Usage Guide / Інструкція з використання

### English

DevTime operates as a command-line interface (CLI) tool, allowing users to efficiently manage their tasks and schedules. Below is a detailed guide on how to use the program.

### Running DevTime
To start using DevTime, open your terminal and enter:
```bash
python -m devtime.cli
```
Alternatively, if installed globally, simply type:
```bash
devtime
```

### Available Commands
DevTime provides the following commands for task management:

#### 1. Adding a Task
To add a new task, use the following command:
```bash
devtime add "Task Name" <duration> [deadline] [priority]
```
- `<duration>` - Task duration in hours (e.g., `1.5` for 1 hour 30 minutes).
- `[deadline]` - (Optional) Deadline in `YYYY-MM-DD HH:MM` format.
- `[priority]` - (Optional) Task priority (`1` for high, `2` for medium, `3` for low). Defaults to `2`.

Example:
```bash
devtime add "Write report" 2 2025-03-01 14:00 1
```

#### 2. Viewing the Schedule
To generate and view today's schedule, run:
```bash
devtime plan
```
This will display an optimized schedule considering your available work hours and breaks.

#### 3. Editing a Task
Modify an existing task using:
```bash
devtime edit <task_id> --name "New Name" --duration <new_duration> --deadline "YYYY-MM-DD HH:MM" --priority <new_priority>
```
Example:
```bash
devtime edit 105 --name "Finalize report" --duration 3
```

#### 4. Completing a Task
Mark a task as completed with:
```bash
devtime complete <task_id>
```
Example:
```bash
devtime complete 105
```

#### 5. Deleting a Task
Remove a task using:
```bash
devtime delete <task_id>
```
Example:
```bash
devtime delete 105
```

#### 6. Viewing Task History (Upcoming Feature)
```bash
devtime history
```
Currently under development.

#### 7. Viewing Saved Schedules (Upcoming Feature)
```bash
devtime schedule
```
Currently under development.

#### 8. Interactive Mode
To launch interactive mode:
```bash
devtime
```
This allows real-time command input without needing to restart the program each time.

### Customization
DevTime allows personal customization through the `config.json` file. You can modify:
- **Work hours** (start and end time per day)
- **Maximum concentration time** (length of focused work sessions)
- **Break duration** (minimum break time between sessions)

Example configuration:
```json
{
  "work_hours": {
    "Monday": {"start": 9, "end": 18},
    "Tuesday": {"start": 9, "end": 18}
  },
  "max_concentration_hours": 1.5,
  "min_break_minutes": 10
}
```

---

### Українська

DevTime працює як інструмент командного рядка (CLI), що дозволяє ефективно керувати завданнями та розкладом. Нижче наведено детальний посібник із використання програми.

### Запуск DevTime
Щоб почати користуватися DevTime, відкрийте термінал і введіть:
```bash
python -m devtime.cli
```
Або, якщо програма встановлена глобально, просто введіть:
```bash
devtime
```

### Доступні команди
DevTime підтримує такі команди для керування завданнями:

#### 1. Додавання завдання
Щоб додати нове завдання, використовуйте команду:
```bash
devtime add "Назва завдання" <тривалість> [дедлайн] [пріоритет]
```
- `<тривалість>` - Час виконання в годинах (наприклад, `1.5` для 1 години 30 хвилин).
- `[дедлайн]` - (Опціонально) Дата та час у форматі `YYYY-MM-DD HH:MM`.
- `[пріоритет]` - (Опціонально) Пріоритет (`1` - високий, `2` - середній, `3` - низький). За замовчуванням `2`.

Приклад:
```bash
devtime add "Написати звіт" 2 2025-03-01 14:00 1
```

#### 2. Перегляд розкладу
Щоб створити та переглянути розклад на сьогодні, введіть:
```bash
devtime plan
```
Ця команда згенерує оптимізований розклад із урахуванням доступного робочого часу та перерв.

#### 3. Редагування завдання
Змінити завдання можна за допомогою команди:
```bash
devtime edit <id_завдання> --name "Нова назва" --duration <нова_тривалість> --deadline "YYYY-MM-DD HH:MM" --priority <новий_пріоритет>
```
Приклад:
```bash
devtime edit 105 --name "Завершити звіт" --duration 3
```

#### 4. Виконання завдання
Позначити завдання як виконане можна так:
```bash
devtime complete <id_завдання>
```
Приклад:
```bash
devtime complete 105
```

#### 5. Видалення завдання
Видалити завдання можна за допомогою команди:
```bash
devtime delete <id_завдання>
```
Приклад:
```bash
devtime delete 105
```

#### 6. Перегляд історії завдань (в розробці)
```bash
devtime history
```
Функція поки що в розробці.

#### 7. Перегляд збережених розкладів (в розробці)
```bash
devtime schedule
```
Функція поки що в розробці.

#### 8. Інтерактивний режим
Щоб запустити інтерактивний режим:
```bash
devtime
```
Це дозволяє вводити команди в реальному часі без необхідності перезапуску програми.

### Налаштування
DevTime дозволяє персоналізувати налаштування через файл `config.json`. Ви можете змінити:
- **Робочі години** (початок та кінець роботи для кожного дня)
- **Максимальний час концентрації** (тривалість зосередженої роботи)
- **Час перерви** (мінімальна тривалість відпочинку між сесіями)

Приклад конфігурації:
```json
{
  "work_hours": {
    "Monday": {"start": 9, "end": 18},
    "Tuesday": {"start": 9, "end": 18}
  },
  "max_concentration_hours": 1.5,
  "min_break_minutes": 10
}
```

---

## 5. Architecture and Design / Архітектура та дизайн

### English

DevTime is designed with modularity and maintainability in mind. It follows a structured approach where each component is responsible for a specific functionality, ensuring separation of concerns and ease of expansion.

### Project Structure
```
DevTime/
├── devtime/
│   ├── __init__.py
│   ├── cli.py         # Main entry point for command-line execution
│   ├── config.py      # Handles configuration settings
│   ├── scheduler.py   # Core scheduling logic
│   ├── storage.py     # Handles task persistence
├── tests/             # Unit tests for different components
│   ├── test_parsing.py
│   ├── test_scheduler.py
│   ├── test_storage.py
├── docs/              # Documentation
│   ├── Extended_Documentation.md
├── config.json        # User configuration file
├── setup.py           # Packaging script
├── requirements.txt   # Dependencies list
├── README.md          # Project description
```

### Core Components
- **CLI Interface (cli.py)**: Handles user input and interactive mode.
- **Scheduler (scheduler.py)**: Implements the core logic for task scheduling, prioritization, and time slot allocation.
- **Storage (storage.py)**: Manages loading, saving, and retrieving task data.
- **Configuration (config.py)**: Loads and updates user preferences, such as working hours and concentration limits.

### Design Principles
- **Modular Structure**: Each component is independent, allowing easy updates and scalability.
- **Cross-Platform Compatibility**: Built using Python, ensuring compatibility with Windows, macOS, and Linux.
- **Efficiency & Optimization**: The scheduling algorithm dynamically adjusts to changes in user input and system state.

---

### Українська

DevTime розроблено з урахуванням модульності та зручності в обслуговуванні. Програма дотримується структурованого підходу, де кожен компонент відповідає за певну функціональність, що забезпечує розділення відповідальності та легкість розширення.

### Структура проєкту
```
DevTime/
├── devtime/
│   ├── __init__.py
│   ├── cli.py         # Головний файл для запуску з командного рядка
│   ├── config.py      # Відповідає за налаштування
│   ├── scheduler.py   # Основна логіка планування
│   ├── storage.py     # Управління збереженням завдань
├── tests/             # Модульні тести для різних компонентів
│   ├── test_parsing.py
│   ├── test_scheduler.py
│   ├── test_storage.py
├── docs/              # Документація
│   ├── Extended_Documentation.md
├── config.json        # Файл налаштувань користувача
├── setup.py           # Скрипт для створення пакета
├── requirements.txt   # Список залежностей
├── README.md          # Опис проєкту
```

### Основні компоненти
- **Інтерфейс CLI (cli.py)**: Обробляє введення команд та інтерактивний режим.
- **Модуль планування (scheduler.py)**: Реалізує алгоритм розкладу, розподілу завдань за часом та пріоритетами.
- **Система збереження (storage.py)**: Відповідає за читання, запис та оновлення завдань.
- **Конфігурація (config.py)**: Завантажує та змінює налаштування користувача, включаючи робочі години та перерви.

### Принципи проєктування
- **Модульна структура**: Кожен компонент є незалежним, що спрощує оновлення та масштабування.
- **Кросплатформеність**: Використання Python забезпечує роботу на Windows, macOS та Linux.
- **Оптимізація та ефективність**: Алгоритм планування адаптується до змін у введених користувачем даних та стану системи.

---

## 6. Testing and Quality Assurance / Тестування та забезпечення якості

### English

Ensuring the reliability and stability of DevTime is a top priority. The project includes unit tests and different inspection practices to maintain high code quality and minimize potential issues.

### Unit Testing

- DevTime employs **unit tests** to verify the correctness of individual functions and modules.
- The tests are located in the `tests/` directory and cover key components such as task parsing, scheduling, and storage.
- To run the unit tests, use:
  ```bash
  python -m unittest discover tests
  ```

### Error Handling and Debugging

- DevTime includes robust error handling mechanisms to prevent crashes and unexpected behavior.

### Code Quality and Best Practices

- The project follows **PEP 8** coding standards to maintain clean and readable code.
- Code reviews and automated checks ensure maintainability and adherence to best practices.

---

### Українська

Забезпечення надійності та стабільності DevTime є пріоритетним завданням. Проєкт включає модульні тести та різні практики перевірки для підтримки високої якості коду та мінімізації можливих проблем.

### Модульне тестування

- DevTime використовує **модульні тести** для перевірки правильності роботи окремих функцій і модулів.
- Тести розташовані в каталозі `tests/` і охоплюють основні компоненти, такі як обробка завдань, планування та збереження даних.
- Для запуску модульних тестів використовуйте команду:
  ```bash
  python -m unittest discover tests
  ```

### Обробка помилок і налагодження

- DevTime містить надійні механізми обробки помилок, що запобігають збоям і неочікуваній поведінці.

### Якість коду та найкращі практики

- У проєкті дотримуються стандартів кодування **PEP 8**, що забезпечує чистий і зрозумілий код.
- Код проходить перевірку через рецензування та автоматизовані тести, що гарантує підтримку найкращих практик.

---

## 7. Future Improvements / Майбутні покращення

### English

Planned enhancements for future versions:

- **Extended Command Set:** New commands for exporting schedules and advanced filtering.
- **Lunch Break Support:** Automated scheduling of lunch breaks.

### Українська

Плани на майбутні версії:

- **Розширений набір команд:** Команди для експорту розкладу та розширених фільтрів.
- **Підтримка обідньої перерви:** Автоматичне планування обідніх перерв.

---

## 8. Contributing / Внесок

### English

We welcome contributions! To contribute:

1. Fork the repository.
2. Create a new branch.
3. Make changes and run tests.
4. Submit a pull request.

### Українська

Ми вітаємо внески! Щоб долучитися:

1. Форкніть репозиторій.
2. Створіть нову гілку.
3. Внесіть зміни та запустіть тести.
4. Відправте pull request.

---

## 9. License and Attribution / Ліцензія та авторство

### English

DevTime is licensed under the **MIT License**.

Developed by **Nazar Mokh**.

### Українська

DevTime ліцензовано за **MIT License**.

Розробник: **Назар Мох**.

---

## 10. Acknowledgements / Подяки

Special thanks to the open-source community and to everyone supporting Ukraine during these challenging times.
Особлива подяка спільноті open-source та всім, хто підтримує Україну в ці важкі часи. 🇺🇦
