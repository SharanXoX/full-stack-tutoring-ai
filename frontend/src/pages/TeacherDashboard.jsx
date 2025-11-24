// src/pages/TeacherDashboard.jsx
import React from "react";
import FileUpload from "../components/FileUpload";

export default function TeacherDashboard(){
  return (
    <div>
      <FileUpload userId="teacher_demo" userRole="teacher" />
    </div>
  );
}
