import React, { useState } from 'react';
import styled from 'styled-components';
import { Link, useParams } from 'react-router-dom';
import FileUploader from './Button';
import base64 from 'base-64';

// Стили для страницы
const Container = styled.div`
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 20px;
  font-family: "Montserrat", sans-serif;
  align-items: center;
`;

const BlockTask = styled.div`
  width: 1248px;
  background-color: #D5DEF6;
  padding: 30px;
  border-radius: 7px;
`;

const BlockTest = styled.div`
  width: 1248px;
  background-color: #E2EDD0;
  padding: 30px;
  border-radius: 7px;
`;

const BlockTry = styled.div`
  width: 1248px;
  background-color: #D9D9D9;
  padding: 30px;
  border-radius: 7px;
  display: flex;
  justify-content: center;
  align-items: center;
`;

const Title = styled.h2`
  font-size: 16px;
  margin-bottom: 10px;
`;

const Text = styled.p`
  font-size: 16px;
  line-height: 1.5;
`;

const Button = styled.button`
  padding: 10px;
  width: 1100px;
  background-color: white;
  border-style: none;
  border-radius: 7px;
  font-family: "Montserrat";
  font-size: 16px;
  display: flex;
  justify-content: center;
  align-items: center;

  &:hover {
    background: #E2EDD0;
    color: #000;
    transition: 0.3s;
  }
`;

const StyledLink = styled(Link)`
  text-decoration: none;  // Убираем подчеркивание
`;

// Компонент страницы с блоками
const LabaStud = () => {
  const [file, setFile] = useState(null);
  const { id } = useParams(); // Получаем id лабораторной

  const handleSubmit = async () => {
    if (file) {
      const reader = new FileReader();
      reader.readAsArrayBuffer(file);
      reader.onload = () => {
        const encodedFile = base64.encode(
          String.fromCharCode(...new Uint8Array(reader.result))
        );
        fetch(`http://0.0.0.0:8002/check/1`, {
          headers: {
            'Content-Type': 'application/json',
          },
          method: 'POST',
          body: JSON.stringify({ file: encodedFile }),
        })
          .then((response) => response.json())
          .then((data) => {
            console.log('Результаты тестов:', data);
          })
          .catch((error) => {
            console.error('Ошибка:', error);
          });
      };
    } else {
      alert('Пожалуйста, выберите файл для загрузки.');
    }
  };

  return (
    <Container>
      {/* Первый блок: Условие задачи */}
      <BlockTask>
        <Text>
          Даны три целых числа. Найдите наибольшее из них (программа должна вывести ровно одно целое число). Под наибольшим в этой задаче понимается число, которое не меньше, чем любое другое.
        </Text>
        <Text>
          <strong>Формат входных данных:</strong> Вводятся три числа.
        </Text>
        <Text>
          <strong>Формат выходных данных:</strong> Выведите ответ на задачу.
        </Text>
        <Text>
          <strong>Sample Input:</strong>
        </Text>
        <Text>1<br />2<br />3</Text>
        <Text>
          <strong>Sample Output:</strong>
        </Text>
        <Text>3</Text>
      </BlockTask>

      {/* Второй блок: Описание тестов */}
      <BlockTest>
        <Title>Типы тестов, используемые в данной лабораторной работе:</Title>
        <ul>
          <li>Проверка формулы</li>
          <br />
          <li>Автотесты</li>
          <br />
          <li>Проверка скорости выполнения</li>
          <br />
          <li>Проверка чего-нибудь еще</li>
        </ul>
      </BlockTest>

      {/* Третий блок */}
      <BlockTask>
        <Title>Ответ в виде файла:</Title>
        <FileUploader file={file} setFile={setFile} onSubmit={handleSubmit} />
      </BlockTask>

      {/* Четвертый блок: кнопка Мои попытки */}
      <BlockTry>
        <StyledLink to={`/attempts/${id}`}>
          <Button>
            <Text>Мои попытки</Text>
          </Button>
        </StyledLink>
      </BlockTry>
    </Container>
  );
};

export default LabaStud;
