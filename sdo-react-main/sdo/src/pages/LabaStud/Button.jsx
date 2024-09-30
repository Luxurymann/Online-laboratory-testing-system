// import React, { useState } from 'react';
// import styled from 'styled-components';

// const Form = styled.form`
//     display: flex;
//     flex-direction: column;
//     align-items: center;
//     gap: 45px;
// `;

// const Button = styled.button`
//     width: 1098px;
//     height: 75px;
//     background-color: #FFFFFF;
//     color: #000000;
//     cursor: pointer;
//     border-radius: 10px;
//     border-style: none;
//     font-family: 'Montserrat';
//     font-size: 16px;
//     margin-bottom: 20px;

//     &:hover {
//         background-color: #E2EDD0;
//         color: #000;
//         transition: 0.3s;
//     }
// `;

// const Inpt = styled.input`
//     display: none;
// `;

// const Label = styled.label`
//   border: 2px dashed #000;
//   height: 250px;
//   text-align: center;
//   border-radius: 7px;
//   margin-top: 10px;
//   width: 1098px;
//   transition: background-color 0.3s;
//   background-color: #FFFFFF;

//   &:hover {
//     background-color: #E2EDD08C;
//   }
// `;

// const Span = styled.span`
//     display: flex;
//     justify-content: center;
//     align-items: center;
//     width: 100%;
//     height: 100%;
//     background-color: ${({ isDragging }) => (isDragging ? '#F5F5F5' : 'transparent')};
//     transition: background-color 0.3s ease;
// `;

// const FileUploader = ({ file, setFile, onSubmit }) => {
//     const [isDragging, setIsDragging] = useState(false);
//     const [isHovered, setIsHovered] = useState(false);

//     const handleChange = (e) => {
//         if (e.target.files && e.target.files[0]) {
//             setFile(e.target.files[0]);
//         }
//     };

//     const handleDragEnter = (e) => {
//         e.preventDefault();
//         setIsDragging(true);
//     };

//     const handleDragLeave = () => {
//         setIsDragging(false);
//     };

//     const handleDrop = (e) => {
//         e.preventDefault();
//         setIsDragging(false);

//         if (e.dataTransfer.files && e.dataTransfer.files[0]) {
//             setFile(e.dataTransfer.files[0]);
//         }
//     };

//     return (
//         <Form
//             onDragEnter={handleDragEnter}
//             onDragOver={handleDragEnter}
//             onDragLeave={handleDragLeave}
//             onDrop={handleDrop}
//         >
//             <Label
//                 htmlFor="fileInput"
//                 isHovered={isHovered}
//                 onMouseEnter={() => setIsHovered(true)}
//                 onMouseLeave={() => setIsHovered(false)}
//             >
//                 <Span isDragging={isDragging}>
//                     {file ? file.name : 'Загрузите файл'}
//                 </Span>
//                 <Inpt
//                     id="fileInput"
//                     type="file"
//                     onChange={handleChange}
//                     onMouseEnter={() => setIsHovered(true)}
//                     onMouseLeave={() => setIsHovered(false)}
//                 />
//             </Label>
//             <Button type="button" onClick={onSubmit}>
//                 Отправить на проверку
//             </Button>
//         </Form>
//     );
// };

// export default FileUploader;
import React, { useState } from 'react';
import styled from 'styled-components';

// Стили для формы и элементов
const Form = styled.form`
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 45px;
`;

const Button = styled.button`
  width: 1098px;
  height: 75px;
  background-color: ${({ disabled }) => (disabled ? '#ccc' : '#FFFFFF')};
  color: ${({ disabled }) => (disabled ? '#999' : '#000')};
  cursor: ${({ disabled }) => (disabled ? 'not-allowed' : 'pointer')};
  border-radius: 10px;
  border-style: none;
  font-family: 'Montserrat';
  font-size: 16px;
  margin-bottom: 20px;
  transition: background-color 0.3s;

  &:hover {
    background-color: ${({ disabled }) => (disabled ? '#ccc' : '#E2EDD0')};
  }
`;

const Inpt = styled.input`
  display: none;
`;

const Label = styled.label`
  border: 2px dashed #000;
  height: 250px;
  text-align: center;
  border-radius: 7px;
  margin-top: 10px;
  width: 1098px;
  transition: background-color 0.3s;
  background-color: #FFFFFF;

  &:hover {
    background-color: #E2EDD08C;
  }
`;

const Span = styled.span`
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  background-color: ${({ isDragging }) => (isDragging ? '#F5F5F5' : 'transparent')};
  transition: background-color 0.3s ease;
`;

const ProgressContainer = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 1100px;
  margin-top: 20px;
`;

const ProgressBar = styled.div`
  flex-grow: 1;
  height: 30px;
  background-color: #fff;
  border-radius: 5px;
  margin-right: 10px;
`;

const ProgressFill = styled.div`
  height: 100%;
  width: ${({ progress }) => `${progress}%`};
  background-color: #76c7c0;
  border-radius: 5px;
  transition: width 0.3s ease;
`;

const ProgressText = styled.span`
  font-size: 16px;
`;

// Основной компонент для загрузки файла с прогресс-баром
const FileUploader = ({ file, setFile }) => {
  const [isDragging, setIsDragging] = useState(false);
  const [progress, setProgress] = useState(0); // Состояние для отслеживания прогресса
  const [isUploading, setIsUploading] = useState(false); // Состояние загрузки файла

  const handleChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleDragEnter = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
    }
  };

  // Функция для отправки файла и отслеживания прогресса
  const handleSubmit = async () => {
    if (file) {
      setIsUploading(true); // Установка состояния загрузки файла

      // Используем FormData для передачи файла напрямую
      const formData = new FormData();
      formData.append('file', file);

      // Используем XMLHttpRequest для отслеживания прогресса загрузки
      const xhr = new XMLHttpRequest();
      xhr.open('POST', 'http://0.0.0.0:8002/check/1', true);

      // Отслеживание прогресса загрузки
      xhr.upload.onprogress = (event) => {
        if (event.lengthComputable) {
          const percentComplete = Math.round((event.loaded / event.total) * 100);
          setProgress(percentComplete); // Установка процента выполнения
        }
      };

      // Обработка завершения загрузки
      xhr.onload = () => {
        setIsUploading(false); // Завершение загрузки
        if (xhr.status === 200) {
          console.log('Загрузка успешна:', xhr.responseText);
        } else {
          console.error('Ошибка загрузки:', xhr.statusText);
        }
      };

      xhr.onerror = () => {
        setIsUploading(false); // Ошибка при загрузке
        console.error('Ошибка загрузки');
      };

      xhr.send(formData); // Отправка файла через FormData
    } else {
      alert('Пожалуйста, выберите файл для загрузки.');
    }
  };

  return (
    <Form
      onDragEnter={handleDragEnter}
      onDragOver={handleDragEnter}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
    >
      <Label htmlFor="fileInput">
        <Span isDragging={isDragging}>
          {file ? file.name : 'Загрузите файл'}
        </Span>
        <Inpt id="fileInput" type="file" onChange={handleChange} />
      </Label>

      {file && (
        <ProgressContainer>
          <ProgressBar>
            <ProgressFill progress={progress} />
          </ProgressBar>
          <ProgressText>{progress}%</ProgressText>
        </ProgressContainer>
      )}

      <Button
        type="button"
        onClick={handleSubmit}
        disabled={!file || isUploading || progress < 100} // Блокируем кнопку до достижения 100%
      >
        {isUploading ? 'Загружается...' : 'Отправить на проверку'}
      </Button>
    </Form>
  );
};

export default FileUploader;
