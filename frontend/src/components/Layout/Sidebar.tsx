import { } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import {
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Box,
  Typography,
  Avatar,
} from '@mui/material'
import {
  Dashboard as DashboardIcon,
  People as PeopleIcon,
  AccountBalance as BankIcon,
  Assessment as ReportIcon,
  Description as DataIcon,
  Search as InquiryIcon,
  Gavel as DisputeIcon,
  Settings as SettingsIcon,
  Logout as LogoutIcon,
} from '@mui/icons-material'
import { useAuth } from '../../context/AuthContext'

const drawerWidth = 260

interface SidebarProps {
  open: boolean
  onClose: () => void
}

export default function Sidebar({ open, onClose }: SidebarProps) {
  const navigate = useNavigate()
  const location = useLocation()
  const { user, logout } = useAuth()

  const getMenuItems = () => {
    const role = user?.role || ''
    
    if (role === 'ADMIN') {
      return [
        { text: 'Dashboard', icon: <DashboardIcon />, path: '/dashboard' },
        { text: 'Users', icon: <PeopleIcon />, path: '/admin/users' },
        { text: 'Banks', icon: <BankIcon />, path: '/admin/banks' },
        { text: 'Audit Logs', icon: <SettingsIcon />, path: '/admin/audit' },
      ]
    } else if (role === 'BANK_MANAGER' || role === 'BANK_USER') {
      return [
        { text: 'Dashboard', icon: <DashboardIcon />, path: '/dashboard' },
        { text: 'Submit Data', icon: <DataIcon />, path: '/bank/submit-data' },
        { text: 'Credit Inquiry', icon: <InquiryIcon />, path: '/bank/inquiry' },
        { text: 'Inquiry History', icon: <ReportIcon />, path: '/bank/history' },
      ]
    } else if (role === 'CONSUMER') {
      return [
        { text: 'Dashboard', icon: <DashboardIcon />, path: '/dashboard' },
        { text: 'Credit Report', icon: <ReportIcon />, path: '/consumer/report' },
        { text: 'Disputes', icon: <DisputeIcon />, path: '/consumer/disputes' },
        { text: 'Consent', icon: <SettingsIcon />, path: '/consumer/consent' },
      ]
    }
    return []
  }

  const menuItems = getMenuItems()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <Drawer
      variant="persistent"
      open={open}
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: drawerWidth,
          boxSizing: 'border-box',
          borderRight: '1px solid rgba(0, 0, 0, 0.12)',
          display: 'flex',
          flexDirection: 'column',
        },
      }}
    >
      <Box sx={{ p: 2, borderBottom: '1px solid rgba(0, 0, 0, 0.12)' }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <Avatar sx={{ bgcolor: 'primary.main', width: 40, height: 40 }}>
            CC
          </Avatar>
          <Box>
            <Typography variant="h6" sx={{ fontWeight: 600 }}>
              Credit Check
            </Typography>
            <Typography variant="caption" color="text.secondary">
              Marshall Islands
            </Typography>
          </Box>
        </Box>
      </Box>

      <List sx={{ pt: 2, flexGrow: 1 }}>
        {menuItems.map((item) => (
          <ListItem key={item.path} disablePadding>
            <ListItemButton
              selected={location.pathname === item.path}
              onClick={() => {
                navigate(item.path)
                onClose()
              }}
              sx={{
                mx: 1,
                mb: 0.5,
                borderRadius: 1,
                '&.Mui-selected': {
                  backgroundColor: 'primary.main',
                  color: 'white',
                  '&:hover': {
                    backgroundColor: 'primary.dark',
                  },
                  '& .MuiListItemIcon-root': {
                    color: 'white',
                  },
                },
              }}
            >
              <ListItemIcon sx={{ minWidth: 40 }}>
                {item.icon}
              </ListItemIcon>
              <ListItemText primary={item.text} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>

      <Box sx={{ p: 2, borderTop: '1px solid rgba(0, 0, 0, 0.12)' }}>
        <Box sx={{ mb: 2, p: 1.5, bgcolor: 'background.default', borderRadius: 1 }}>
          <Typography variant="body2" fontWeight={500}>
            {user?.full_name}
          </Typography>
          <Typography variant="caption" color="text.secondary">
            {user?.role?.replace('_', ' ')}
          </Typography>
        </Box>
        <ListItemButton 
          onClick={handleLogout} 
          sx={{ borderRadius: 1 }}
        >
          <ListItemIcon>
            <LogoutIcon />
          </ListItemIcon>
          <ListItemText primary="Logout" />
        </ListItemButton>
      </Box>
    </Drawer>
  )
}

