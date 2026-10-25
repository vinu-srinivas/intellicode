import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import "./App.css";
import Editor from "./pages/CodeEditor";

const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Editor />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;