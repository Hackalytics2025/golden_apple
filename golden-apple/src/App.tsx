import React from "react";
import { Routes, Route } from "react-router-dom";
import WelcomeScreen from "./pages/WelcomeScreen";

const App: React.FC = () => {
  return (
    <Routes>
      <Route path="/" element={<WelcomeScreen />} />
    </Routes>
  );
};

export default App;
