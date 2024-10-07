import React, { useState } from 'react';
import styled from 'styled-components';

const Form = styled.form`
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 45px;
`;

const Inpt = styled.input`
  display: none;
`;

const Label = styled.label`
  border: 2px dashed #000;
  height: 200px;
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

// Main file uploader component
const FileUploader = ({ file, setFile }) => {
  const [isDragging, setIsDragging] = useState(false);
  const [progress, setProgress] = useState(0);

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
    </Form>
  );
};

export default FileUploader;
