import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import ScanHistory from './pages/ScanHistory'
import StartScan from './pages/StartScan'
import ScanResult from './pages/ScanResult'
import Navbar from './components/Navbar'

function PrivateRoute({ children }) {
  const token = localStorage.getItem('token')
  return token ? children : <Navigate to="/login" />
}

function Layout({ children }) {
  return (
    <>
      <Navbar />
      <main>{children}</main>
    </>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/" element={
          <PrivateRoute>
            <Layout><Dashboard /></Layout>
          </PrivateRoute>
        } />
        <Route path="/scan/new" element={
          <PrivateRoute>
            <Layout><StartScan /></Layout>
          </PrivateRoute>
        } />
        <Route path="/scan/history" element={
          <PrivateRoute>
            <Layout><ScanHistory /></Layout>
          </PrivateRoute>
        } />
        <Route path="/scan/:id" element={
          <PrivateRoute>
            <Layout><ScanResult /></Layout>
          </PrivateRoute>
        } />
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </BrowserRouter>
  )
}
