import { Container, Typography, Box, Grid, Card, CardContent, Button } from '@mui/material'
import {
  People as PeopleIcon,
  AccountBalance as BankIcon,
  Assessment as ReportIcon,
  TrendingUp as TrendingUpIcon,
  Search as InquiryIcon,
  Gavel as DisputeIcon,
  Settings as SettingsIcon,
} from '@mui/icons-material'
import { useAuth } from '../context/AuthContext'
import { useNavigate } from 'react-router-dom'

export default function Dashboard() {
  const { user } = useAuth()
  const navigate = useNavigate()

  const getDashboardCards = () => {
    const role = user?.role || ''
    
    if (role === 'ADMIN') {
      return [
        {
          title: 'User Management',
          description: 'Manage users and permissions',
          path: '/admin/users',
          icon: <PeopleIcon sx={{ fontSize: 40 }} />,
          color: '#4285f4',
        },
        {
          title: 'Bank Management',
          description: 'Approve and manage banks',
          path: '/admin/banks',
          icon: <BankIcon sx={{ fontSize: 40 }} />,
          color: '#34a853',
        },
        {
          title: 'Audit Logs',
          description: 'View system audit logs',
          path: '/admin/audit',
          icon: <SettingsIcon sx={{ fontSize: 40 }} />,
          color: '#fbbc04',
        },
      ]
    } else if (role === 'BANK_MANAGER' || role === 'BANK_USER') {
      return [
        {
          title: 'Submit Credit Data',
          description: 'Submit credit account data',
          path: '/bank/submit-data',
          icon: <TrendingUpIcon sx={{ fontSize: 40 }} />,
          color: '#4285f4',
        },
        {
          title: 'Credit Inquiry',
          description: 'Request credit reports',
          path: '/bank/inquiry',
          icon: <InquiryIcon sx={{ fontSize: 40 }} />,
          color: '#34a853',
        },
        {
          title: 'Inquiry History',
          description: 'View past inquiries',
          path: '/bank/history',
          icon: <ReportIcon sx={{ fontSize: 40 }} />,
          color: '#fbbc04',
        },
      ]
    } else if (role === 'CONSUMER') {
      return [
        {
          title: 'My Credit Report',
          description: 'View your credit report',
          path: '/consumer/report',
          icon: <ReportIcon sx={{ fontSize: 40 }} />,
          color: '#4285f4',
        },
        {
          title: 'Disputes',
          description: 'Dispute credit information',
          path: '/consumer/disputes',
          icon: <DisputeIcon sx={{ fontSize: 40 }} />,
          color: '#ea4335',
        },
        {
          title: 'Consent Management',
          description: 'Manage data sharing consent',
          path: '/consumer/consent',
          icon: <SettingsIcon sx={{ fontSize: 40 }} />,
          color: '#34a853',
        },
      ]
    }
    
    return []
  }

  const cards = getDashboardCards()

  return (
    <Container maxWidth="lg">
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" fontWeight={600} gutterBottom>
          Welcome back, {user?.full_name}
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Manage your credit bureau activities from here
        </Typography>
      </Box>

      <Grid container spacing={3}>
        {cards.map((card, index) => (
          <Grid item xs={12} sm={6} md={4} key={index}>
            <Card
              sx={{
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                cursor: 'pointer',
                transition: 'all 0.3s ease',
                '&:hover': {
                  transform: 'translateY(-4px)',
                  boxShadow: 6,
                },
              }}
              onClick={() => navigate(card.path)}
            >
              <CardContent sx={{ flexGrow: 1, p: 3 }}>
                <Box
                  sx={{
                    width: 64,
                    height: 64,
                    borderRadius: 2,
                    bgcolor: `${card.color}15`,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: card.color,
                    mb: 2,
                  }}
                >
                  {card.icon}
                </Box>
                <Typography variant="h6" component="h2" fontWeight={600} gutterBottom>
                  {card.title}
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  {card.description}
                </Typography>
                <Button
                  variant="contained"
                  fullWidth
                  sx={{
                    bgcolor: card.color,
                    '&:hover': {
                      bgcolor: card.color,
                      opacity: 0.9,
                    },
                  }}
                >
                  Access {card.title}
                </Button>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Container>
  )
}

