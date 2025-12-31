import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuth } from './context/AuthContext'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import Layout from './components/Layout/Layout'
import Users from './pages/admin/Users'
import Banks from './pages/admin/Banks'
import SubmitData from './pages/bank/SubmitData'
import CreditInquiry from './pages/bank/CreditInquiry'
import CreditReport from './pages/consumer/CreditReport'

function App() {
  const { user, loading } = useAuth()

  if (loading) {
    return <div>Loading...</div>
  }

  return (
    <Routes>
      <Route path="/login" element={!user ? <Login /> : <Navigate to="/dashboard" />} />
      <Route path="/register" element={!user ? <Register /> : <Navigate to="/dashboard" />} />
      <Route
        path="/dashboard"
        element={user ? <Layout><Dashboard /></Layout> : <Navigate to="/login" />}
      />
      <Route
        path="/admin/users"
        element={user ? <Layout><Users /></Layout> : <Navigate to="/login" />}
      />
      <Route
        path="/admin/banks"
        element={user ? <Layout><Banks /></Layout> : <Navigate to="/login" />}
      />
      <Route
        path="/bank/submit-data"
        element={user ? <Layout><SubmitData /></Layout> : <Navigate to="/login" />}
      />
      <Route
        path="/bank/inquiry"
        element={user ? <Layout><CreditInquiry /></Layout> : <Navigate to="/login" />}
      />
      <Route
        path="/consumer/report"
        element={user ? <Layout><CreditReport /></Layout> : <Navigate to="/login" />}
      />
      <Route path="/*" element={<Navigate to="/dashboard" />} />
    </Routes>
  )
}

export default App

