from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Table, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.dialects.postgresql import ENUM
import logging

logging.basicConfig(level=logging.CRITICAL)  # Глобально отключить все логи, кроме критических
for logger_name in ('sqlalchemy', 'sqlalchemy.engine', 'sqlalchemy.pool'):
    logging.getLogger(logger_name).setLevel(logging.CRITICAL)

# Database connection setup
DATABASE_URL = "postgresql://root:password@localhost:5432/sdo_db"
engine = create_engine(DATABASE_URL, echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)

RoleTypeEnum = ENUM('admin', 'teacher', 'student', name='role_type', create_type=True)

association_table = Table(
    'UserHasSubject',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('User.id'), primary_key=True),
    Column('subject_id', Integer, ForeignKey('Subject.id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'User'

    # Fields
    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    roleType = Column(RoleTypeEnum, nullable=False, default='student')
    studyGroup = Column(String(32))

    # Relationships
    solutions = relationship('Solution', back_populates='user', cascade="all, delete-orphan")
    subjects = relationship('Subject', secondary=association_table, back_populates='users')

class Subject(Base):
    __tablename__ = 'Subject'

    # Fields
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True, nullable=False)

    # Relationships
    tasks = relationship('Task', back_populates='subject')
    users = relationship('User', secondary=association_table, back_populates='subjects')

class Solution(Base):
    __tablename__ = 'Solution'

    # Fields
    id = Column(Integer, primary_key=True)
    code = Column(String, nullable=False)
    mark = Column(Integer, nullable=True)
    lengthTestResult = Column(Boolean, nullable=True)
    formulaTestResult = Column(Boolean, nullable=True)
    autoTestResult = Column(Integer, nullable=True)

    # ForeignKeys
    User_id = Column(Integer, ForeignKey('User.id'), nullable=False) 
    Task_id = Column(Integer, ForeignKey('Task.id'), nullable=True) # False

    # Relationships
    user = relationship('User', back_populates='solutions')
    task = relationship('Task', back_populates='solution', uselist=False)
    testResults = relationship('TestResult', back_populates='solution')

class Task(Base):
    __tablename__ = "Task"

    # Fields
    id = Column(Integer, primary_key=True)
    name = Column(String(128), unique=True, nullable=False)
    description = Column(String(2048), nullable=True)
    maxSymbolsCount = Column(Integer, nullable=True)
    maxStringsCount = Column(Integer, nullable=True)
    construction = Column(String(128), nullable=True)

    # ForeignKeys
    Subject_id = Column(Integer, ForeignKey('Subject.id'), nullable=False) 

    # Relationships
    solution = relationship('Solution', back_populates='task', uselist=False)
    subject = relationship('Subject', back_populates='tasks')
    testCases = relationship('TestCase', back_populates='task') 

class TestCase(Base):
    __tablename__ = 'TestCase'

    # Fields
    id = Column(Integer, primary_key=True)
    inp = Column(String(512), nullable=False)
    out = Column(String(512), nullable=False)

    # ForeignKeys
    Task_id = Column(Integer, ForeignKey('Task.id'), nullable=True) # False

    # Relationships
    task = relationship('Task', back_populates='testCases')
    testResult = relationship('TestResult', back_populates='testCase', uselist=False)

class TestResult(Base):
    __tablename__ = 'TestResult'

    # Fields
    id = Column(Integer, primary_key=True)
    passed = Column(Boolean, nullable=False)

    # ForeignKeys
    TestCase_id = Column(Integer, ForeignKey('TestCase.id'), nullable=False)
    Solution_id = Column(Integer, ForeignKey('Solution.id'), nullable=False)

    # Relationships
    testCase = relationship('TestCase', back_populates='testResult', uselist=False)
    solution = relationship('Solution', back_populates='testResults')


#добавлена функция получения пользователя для аутентификации
def get_user(username):
    with Session() as session:
        try:
            # Проверяем, существует ли пользователь с таким username
            user = session.query(User).filter_by(username=username).first()
            if not user:
                raise ValueError(f"User with username {username} not found.")

            # Возвращаем пользователя
            return user

        except Exception as e:
            print(f"{username}: {e}")
            raise


def add_user(username, password, role_type='student', study_group=None):
    """
    Добавляет нового пользователя в базу данных.

    :param username: Имя пользователя (уникальное)
    :param password: Пароль пользователя
    :param role_type: Роль пользователя (по умолчанию 'student')
    :param study_group: Учебная группа пользователя (опционально)
    :raises ValueError: Если пользователь с таким именем уже существует
    """
    # Проверка обязательных параметров
    if not username or not password:
        raise ValueError("Username and password are required fields.")

    # Создание сессии
    with Session() as session:
        try:
            # Проверка существующего пользователя с таким именем
            existing_user = session.query(User).filter_by(username=username).first()
            if existing_user:
                raise ValueError(f"User with username '{username}' already exists.")
            
            # Создание нового пользователя
            new_user = User(
                username=username,
                password=password,
                roleType=role_type,
                studyGroup=study_group
            )
            session.add(new_user)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error adding user: {e}")
            raise

def reg_user_in_subject(user_id, subject_identifier):
    """
    Зачисляет пользователя на дисциплину по ID пользователя и ID или имени дисциплины.

    :param user_id: ID пользователя
    :param subject_identifier: ID или имя дисциплины
    :raises ValueError: Если пользователь или дисциплина не найдены
    """
    with Session() as session:
        try:
            # Проверяем, существует ли пользователь с таким user_id
            user = session.query(User).filter_by(id=user_id).first()
            if not user:
                raise ValueError(f"User with ID {user_id} not found.")

            # Если передан ID дисциплины
            if isinstance(subject_identifier, int):
                subject = session.query(Subject).filter_by(id=subject_identifier).first()
            # Если передано имя дисциплины
            else:
                subject = session.query(Subject).filter_by(name=subject_identifier).first()

            if not subject:
                raise ValueError(f"Subject with identifier '{subject_identifier}' not found.")

            # Проверяем, не зачислен ли уже пользователь на эту дисциплину
            if subject in user.subjects:
                raise ValueError(f"User with ID {user_id} is already enrolled in the subject '{subject.name}'.")

            # Добавляем дисциплину в список предметов пользователя
            user.subjects.append(subject)
            session.commit()

        except Exception as e:
            session.rollback()  # Откат транзакции в случае ошибки
            print(f"Error enrolling user {user_id} in subject {subject_identifier}: {e}")
            raise

def get_user_subjects(user_id):
    """
    Получает все дисциплины, на которые зачислен пользователь по ID пользователя.

    :param user_id: ID пользователя
    :return: Список дисциплин, на которые зачислен пользователь
    :raises ValueError: Если пользователь с таким ID не найден
    """
    with Session() as session:
        try:
            # Проверяем, существует ли пользователь с таким user_id
            user = session.query(User).filter_by(id=user_id).first()
            if not user:
                raise ValueError(f"User with ID {user_id} not found.")

            # Возвращаем список всех дисциплин, на которые зачислен пользователь
            return user.subjects

        except Exception as e:
            print(f"Error retrieving subjects for user {user_id}: {e}")
            raise


def add_solution(code, user_id, task_id, mark=None, length_test_result=None, formula_test_result=None, auto_test_result=None):
    """
    Добавляет решение в базу данных.

    :param code: Код решения (обязательное поле)
    :param user_id: ID пользователя (обязательное поле)
    :param task_id: ID задачи (обязательное поле)
    :param mark: Оценка (опционально)
    :param length_test_result: Результат теста по длине (опционально)
    :param formula_test_result: Результат теста по формуле (опционально)
    :param auto_test_result: Результат автотеста (опционально)
    :raises ValueError: Если код решения не указан
    """
    if not code:
        raise ValueError("Code is a required field.")

    # Создание сессии
    with Session() as session:
        try:
            # Создание нового решения
            solution = Solution(
                code=code,
                mark=mark,
                lengthTestResult=length_test_result,
                formulaTestResult=formula_test_result,
                autoTestResult=auto_test_result,
                User_id=user_id,  # Привязка к пользователю
                Task_id=task_id   # Привязка к задаче
            )
            session.add(solution)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error adding solution: {e}")
            raise

    
def get_solutions_by_user(user_id):
    """
    Получает все решения, связанные с пользователем по его ID.

    :param user_id: ID пользователя
    :return: Список решений пользователя
    :raises ValueError: Если пользователь с таким ID не найден
    """
    with Session() as session:
        try:
            # Получение всех решений пользователя
            solutions = session.query(Solution).filter_by(User_id=user_id).all()

            # Если решений не найдено, можно вернуть пустой список или выбросить исключение
            if not solutions:
                print(f"No solutions found for user with ID {user_id}.")
                return []

            return solutions
        except Exception as e:
            print(f"Error retrieving solutions for user with ID {user_id}: {e}")
            raise


def add_subject(name):
    """
    Добавляет новый предмет в базу данных.

    :param name: Название предмета (уникальное)
    :raises ValueError: Если предмет с таким именем уже существует
    """
    if not name:
        raise ValueError("Subject name is required.")

    with Session() as session:
        try:
            # Проверка, существует ли уже предмет с таким именем
            existing_subject = session.query(Subject).filter_by(name=name).first()
            if existing_subject:
                raise ValueError(f"Subject with name '{name}' already exists.")

            # Создание нового предмета
            new_subject = Subject(name=name)
            session.add(new_subject)
            session.commit()
        except Exception as e:
            session.rollback()  # откат в случае ошибки
            print(f"Error adding subject: {e}")
            raise


def get_subjects():
    """
    Получает все предметы из базы данных.

    :return: Список всех предметов
    :raises Exception: Если произошла ошибка при извлечении данных
    """
    with Session() as session:
        try:
            # Извлечение всех предметов из базы данных
            subjects = session.query(Subject).all()

            # Если предметы не найдены, возвращаем пустой список
            if not subjects:
                print("No subjects found.")
                return []

            return subjects
        except Exception as e:
            print(f"Error retrieving subjects: {e}")
            raise



def add_task(name, subject_identifier, description=None, max_symbols_count=None, max_strings_count=None, construction=None):
    """
    Добавляет задачу к предмету. Идентификатором предмета может быть его ID или имя.

    :param name: Название задачи
    :param subject_identifier: ID или имя предмета
    :param description: Описание задачи (опционально)
    :param max_symbols_count: Максимальное количество символов (опционально)
    :param max_strings_count: Максимальное количество строк (опционально)
    :param construction: Дополнительная информация о задаче (опционально)
    """
    session = Session()

    try:
        # Поиск предмета
        if isinstance(subject_identifier, int):
            subject = session.query(Subject).filter_by(id=subject_identifier).first()
        else:
            subject = session.query(Subject).filter_by(name=subject_identifier).first()

        if not subject:
            raise ValueError(f"Subject '{subject_identifier}' not found.")

        # Создание задачи
        new_task = Task(
            name=name,
            description=description,
            maxSymbolsCount=max_symbols_count,
            maxStringsCount=max_strings_count,
            construction=construction,
            Subject_id=subject.id  # Используем найденный ID
        )
        session.add(new_task)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error adding task: {e}")
    finally:
        session.close()   

def get_tasks_by_subject(subject_identifier):
    """
    Получает все задачи, связанные с предметом по его ID или имени.

    :param subject_identifier: ID или имя предмета
    :return: Список задач, связанных с предметом
    :raises ValueError: Если предмет с таким идентификатором или именем не найден
    """
    with Session() as session:
        try:
            # Если передан ID, ищем по ID, если передано имя, ищем по имени
            if isinstance(subject_identifier, int):
                subject = session.query(Subject).filter_by(id=subject_identifier).first()
            else:
                subject = session.query(Subject).filter_by(name=subject_identifier).first()

            if not subject:
                raise ValueError(f"Subject with identifier '{subject_identifier}' not found.")

            # Получаем задачи, связанные с найденным предметом
            tasks = session.query(Task).filter_by(Subject_id=subject.id).all()

            # Если задачи не найдены, возвращаем пустой список
            if not tasks:
                print(f"No tasks found for subject '{subject_identifier}'.")
                return []

            return tasks

        except Exception as e:
            print(f"Error retrieving tasks for subject '{subject_identifier}': {e}")
            raise


def add_test_case(input_data, output_data, task_id):
    """
    Добавляет новый тестовый случай для задачи в базу данных.

    :param input_data: Входные данные для теста
    :param output_data: Ожидаемые выходные данные для теста
    :param task_id: ID задачи, к которой привязан тест
    :raises ValueError: Если входные или выходные данные не указаны или задача не найдена
    """
    if not input_data or not output_data:
        raise ValueError("Both input_data and output_data are required fields.")

    with Session() as session:
        try:
            # Проверяем существование задачи с переданным task_id
            task = session.query(Task).filter_by(id=task_id).first()
            if not task:
                raise ValueError(f"Task with ID {task_id} not found.")

            # Создаем новый тестовый случай
            test_case = TestCase(
                inp=input_data,
                out=output_data,
                Task_id=task_id
            )
            session.add(test_case)
            session.commit()

        except Exception as e:
            session.rollback()  # Откат транзакции в случае ошибки
            print(f"Error adding test case: {e}")
            raise


def get_test_cases_by_task(task_id):
    """
    Получает все тестовые случаи, связанные с задачей по её ID.

    :param task_id: ID задачи
    :return: Список тестовых случаев для указанной задачи
    :raises ValueError: Если задача с таким ID не найдена
    """
    with Session() as session:
        try:
            # Проверяем, существует ли задача с таким task_id
            task = session.query(Task).filter_by(id=task_id).first()
            if not task:
                raise ValueError(f"Task with ID {task_id} not found.")

            # Извлекаем все тестовые случаи, связанные с данной задачей
            test_cases = session.query(TestCase).filter_by(Task_id=task_id).all()

            # Если тестовые случаи не найдены, возвращаем пустой список
            if not test_cases:
                print(f"No test cases found for task with ID {task_id}.")
                return []

            return test_cases

        except Exception as e:
            print(f"Error retrieving test cases for task with ID {task_id}: {e}")
            raise

def get_user_testCase_results_by_solution(user_id, solution_id):
    """
    Возвращает результаты тестов пользователя для указанного решения.
    
    :param user_id: ID пользователя
    :param solution_id: ID задачи
    :return: Список результатов тестов для каждого теста, связанного с решением пользователя
    :raises ValueError: Если пользователь или задача не найдены
    """
    with Session() as session:
        try:
            # Проверяем, существует ли задача с таким task_id
            solution = session.query(Solution).filter_by(id=solution_id).first()
            if not solution:
                raise ValueError(f"Solution with ID {solution_id} not found.")
            user = session.query(User).filter_by(id=user_id).first()
            if not user:
                raise ValueError(f"User with ID {user_id} not found.")
            
            test_results = session.query(TestResult).filter_by(Solution_id=solution_id).all()


            # Если тестовые случаи не найдены, возвращаем пустой список
            if not test_results:
                print(f"No test results found for task with ID {solution_id}.")
                return []

            return test_results

        except Exception as e:
            print(f"Error retrieving test cases for task with ID {solution_id}: {e}")
            raise


    
def get_user_solutions_by_task(user_id, task_id):
    """
    Получает все решения пользователя для конкретной задачи по ID.

    :param user_id: ID пользователя
    :param task_id: ID задачи
    :return: Список решений пользователя для указанной задачи
    :raises ValueError: Если решения не найдены для указанного пользователя и задачи
    """
    with Session() as session:
        try:
            # Запрос решений пользователя для конкретной задачи
            solutions = session.query(Solution).filter_by(User_id=user_id, Task_id=task_id).all()

            # Если решения не найдены, возвращаем пустой список или выбрасываем ошибку
            if not solutions:
                print(f"No solutions found for user {user_id} and task {task_id}.")
                return []

            return solutions
        except Exception as e:
            print(f"Error retrieving solutions for user {user_id} and task {task_id}: {e}")
            raise

def add_test_result(passed, test_case_id, solution_id):
    """
    Добавляет результат теста для решения.

    :param passed: Boolean, указывает, прошел ли тест (True/False)
    :param test_case_id: ID теста (TestCase)
    :param solution_id: ID решения (Solution)
    :return: None
    """
    with Session() as session:
        try:
            # Создаем новый объект TestResult
            test_result = TestResult(
                passed=passed,
                TestCase_id=test_case_id,
                Solution_id=solution_id
            )
            
            # Добавляем результат в сессию
            session.add(test_result)
            # Сохраняем изменения
            session.commit()

        except Exception as e:
            # В случае ошибки откатываем изменения и выводим информацию об ошибке
            session.rollback()
            print(f"Error adding test result: {e}")
            raise

    
def get_users_by_group(study_group):
    """
    Получает всех пользователей, которые принадлежат указанной учебной группе.

    :param study_group: Название учебной группы
    :return: Список пользователей (объекты класса User)
    """
    with Session() as session:
        try:
            # Получаем всех пользователей, принадлежащих к указанной учебной группе
            users = session.query(User).filter_by(studyGroup=study_group).all()
            return users  # Возвращаем список пользователей
        except Exception as e:
            print(f"Error retrieving users for study group {study_group}: {e}")
            raise

def get_users_by_subject(subject_id):
    """
    Возвращает всех пользователей, зачисленных на предмет с заданным subject_id.

    :param subject_id: ID предмета
    :return: Список пользователей (объекты класса User)
    """
    with Session() as session:
        try:
            # Получаем предмет по его ID
            subject = session.query(Subject).filter_by(id=subject_id).first()
            if not subject:
                raise ValueError(f"Subject with ID {subject_id} not found.")

            # Получаем всех пользователей, зачисленных на данный предмет
            users = subject.users  # Используем связь many-to-many, определенную в модели

            return users  # Возвращаем список пользователей
        except Exception as e:
            print(f"Error retrieving users for subject {subject_id}: {e}")
            raise


def evaluate_solution(solution_id, new_mark):
    """
    Оценка решения пользователя для заданного решения.

    :param user_id: ID пользователя
    :param task_id: ID задачи
    :param new_mark: Новая оценка для решения
    :return: Строка с результатом обновления
    :raises ValueError: Если пользователь или задача не найдены, либо решение не найдено
    """
    with Session() as session:
        try:
            # Находим решение пользователя
            solution = session.query(Solution).filter_by(id=solution_id).first()
            if not solution:
                raise ValueError(f"No solution found for solution {solution_id}.")

            # Обновляем поле mark у найденного решения
            solution.mark = new_mark
            session.commit()  # Сохраняем изменения
            return True

        except Exception as e:
            session.rollback()  # Откатываем транзакцию в случае ошибки
            print(f"Error evaluating solution for {solution_id}: {e}")
            raise

def get_users():
    """
    Получает всех пользователей из базы данных.

    :return: Список пользователей (объекты класса User)
    """
    with Session() as session:
        try:
            users = session.query(User).all()  # Получаем всех пользователей
            return users  # Возвращаем список пользователей
        except Exception as e:
            print(f"Error retrieving users: {e}")
            raise


def delete_tables():
    Base.metadata.drop_all(engine)

def create_tables():
    Base.metadata.create_all(engine)
