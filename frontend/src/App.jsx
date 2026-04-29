import { Routes, Route } from 'react-router-dom'
// import reactLogo from './assets/react.svg'
// import viteLogo from './assets/vite.svg'
// import heroImg from './assets/hero.png'
import LoginPage from './Components/Login Page/LoginPage'
import Dashboard from './Components/Admin/Dashboard'
import Registeration from './Components/RegisterationPage/Registeration'
import './App.css'

function App() {
  return (
    <Routes>
      <Route path="/" element={<LoginPage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/registration" element={<Registeration />} />
    </Routes>
  )
}

export default App
