import React from 'react';
import './StudentDashboard.css';

function StudentDashboard() {
  return (
    <div className="dashboard-container">
      <header className="header">
        {/* ВМЕСТО ТЕКСТА ДОБАВИТЬ ИНОКУ */}
        <h1>Московский Политех</h1>
        <nav className="nav">
          <button>Лабораторные работы</button>
          <button>Личный кабинет</button>
          <button>Выйти</button>
        </nav>
      </header>
      
      {/* Заголовок вынесен сюда */}
      <h2 className="breadcrumb">Главная / Личный кабинет</h2>

      <div className="main-content">
        <div className="student-info">
          <div className="info-block">
            <h2>ФИО студента:</h2>
            <p>Иванов Иван Иванович</p>
          </div>
          <div className="info-block">
            <h2>Номер группы:</h2>
            <p>221-111</p>
          </div>
          <div className="info-block">
            <h2>Форма обучения:</h2>
            <p>Очная</p>
          </div>
          <div className="info-block">
            <h2>Направление обучения:</h2>
            <p>Информационная безопасность</p>
          </div>
        </div>

        <div className="disciplines">
          <h2>Дисциплины:</h2>

          <div className="discipline-item">
            <span>Базы данных</span>
            <span className="progress">4/10</span>
            <button>Перейти</button>
          </div>

          <div className="discipline-item">
            <span>Программирование на языке C++</span>
            <span className="progress">5/10</span>
            <button>Перейти</button>
          </div>

          <div className="discipline-item">
            <span>Разработка web приложений</span>
            <span className="progress">6/10</span>
            <button>Перейти</button>
          </div>

          <div className="discipline-item">
            <span>Программирование на языке Python</span>
            <span className="progress">8/10</span>
            <button>Перейти</button>
          </div>

          <div className="discipline-item">
            <span>Методы и языки программирования</span>
            <span className="progress-completed">10/10</span>
            <button>Перейти</button>
          </div>
        </div>
      </div>

      <footer className="footer">
        Вы зашли под именем Иванов Иван
      </footer>
    </div>
  );
}

export default StudentDashboard;
