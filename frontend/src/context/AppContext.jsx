import React, { createContext, useContext, useState } from "react";

const AppContext = createContext(null);

export const AppProvider = ({ children }) => {
  const [uploadedFile, setUploadedFile] = useState(null);
  const [summary, setSummary] = useState(null);
  const [topic, setTopic] = useState(null);

  return (
    <AppContext.Provider value={{ uploadedFile, setUploadedFile, summary, setSummary, topic, setTopic }}>
      {children}
    </AppContext.Provider>
  );
};

export const useAppContext = () => useContext(AppContext);
