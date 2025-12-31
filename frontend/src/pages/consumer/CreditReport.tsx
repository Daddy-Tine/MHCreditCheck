import { useState } from 'react'
import {
  Container,
  Typography,
  Box,
  Paper,
  Button,
  Alert,
  CircularProgress,
  Card,
  CardContent,
  Grid,
  LinearProgress,
  Chip,
} from '@mui/material'
import { Assessment as AssessmentIcon } from '@mui/icons-material'
import { useAuth } from '../../context/AuthContext'
import api from '../../services/api'

interface CreditReport {
  id: number
  credit_score: number
  score_factors: Record<string, string>
  report_data: any
  generated_at: string
}

const getScoreColor = (score: number) => {
  if (score >= 750) return '#34a853'
  if (score >= 700) return '#4285f4'
  if (score >= 650) return '#fbbc04'
  return '#ea4335'
}

const getScoreLabel = (score: number) => {
  if (score >= 750) return 'Excellent'
  if (score >= 700) return 'Good'
  if (score >= 650) return 'Fair'
  if (score >= 600) return 'Poor'
  return 'Very Poor'
}

export default function CreditReport() {
  const { user } = useAuth()
  const [report, setReport] = useState<CreditReport | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const generateReport = async () => {
    setLoading(true)
    setError('')
    const consumerId = 1

    try {
      const response = await api.post('/api/v1/credit-reports/', {
        consumer_id: consumerId,
      })
      setReport(response.data.data)
    } catch (err: any) {
      setError(err.response?.data?.error?.detail || 'Failed to generate report')
    } finally {
      setLoading(false)
    }
  }

  const scoreColor = report ? getScoreColor(report.credit_score) : '#4285f4'

  return (
    <Container maxWidth="lg">
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 4 }}>
        <Box>
          <Typography variant="h4" component="h1" fontWeight={600} gutterBottom>
            Credit Report
          </Typography>
          <Typography variant="body1" color="text.secondary">
            View your credit score and report details
          </Typography>
        </Box>
        <Button
          variant="contained"
          size="large"
          startIcon={<AssessmentIcon />}
          onClick={generateReport}
          disabled={loading}
          sx={{ height: 48 }}
        >
          {loading ? <CircularProgress size={24} /> : 'Generate Report'}
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError('')}>
          {error}
        </Alert>
      )}

      {report && (
        <Grid container spacing={3}>
          {/* Credit Score Card */}
          <Grid item xs={12} md={4}>
            <Card
              sx={{
                background: `linear-gradient(135deg, ${scoreColor} 0%, ${scoreColor}dd 100%)`,
                color: 'white',
                position: 'relative',
                overflow: 'hidden',
              }}
            >
              <Box
                sx={{
                  position: 'absolute',
                  top: -50,
                  right: -50,
                  width: 200,
                  height: 200,
                  borderRadius: '50%',
                  bgcolor: 'rgba(255,255,255,0.1)',
                }}
              />
              <CardContent sx={{ position: 'relative', p: 4 }}>
                <Typography variant="overline" sx={{ opacity: 0.9, mb: 1 }}>
                  Credit Score
                </Typography>
                <Typography
                  variant="h1"
                  sx={{ fontSize: '4rem', fontWeight: 700, mb: 1 }}
                >
                  {report.credit_score}
                </Typography>
                <Chip
                  label={getScoreLabel(report.credit_score)}
                  sx={{
                    bgcolor: 'rgba(255,255,255,0.2)',
                    color: 'white',
                    fontWeight: 600,
                    mb: 2,
                  }}
                />
                <Box sx={{ mt: 3 }}>
                  <Typography variant="caption" sx={{ opacity: 0.9 }}>
                    Score Range: 300 - 850
                  </Typography>
                  <LinearProgress
                    variant="determinate"
                    value={(report.credit_score / 850) * 100}
                    sx={{
                      mt: 1,
                      height: 8,
                      borderRadius: 4,
                      bgcolor: 'rgba(255,255,255,0.2)',
                      '& .MuiLinearProgress-bar': {
                        bgcolor: 'white',
                      },
                    }}
                  />
                </Box>
                <Typography variant="caption" sx={{ mt: 2, display: 'block', opacity: 0.9 }}>
                  Generated: {new Date(report.generated_at).toLocaleDateString()}
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          {/* Score Factors */}
          <Grid item xs={12} md={8}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" fontWeight={600} gutterBottom>
                Score Factors
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                These factors impact your credit score
              </Typography>
              {report.score_factors &&
                Object.entries(report.score_factors).map(([key, value]) => {
                  const numValue = parseFloat(value)
                  return (
                    <Box
                      key={key}
                      sx={{
                        mb: 3,
                        p: 2,
                        bgcolor: 'background.default',
                        borderRadius: 2,
                      }}
                    >
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                        <Typography variant="subtitle2" fontWeight={600}>
                          {key
                            .replace(/_/g, ' ')
                            .replace(/\b\w/g, (l) => l.toUpperCase())}
                        </Typography>
                        <Chip
                          label={value}
                          size="small"
                          color={
                            numValue >= 80
                              ? 'success'
                              : numValue >= 60
                              ? 'warning'
                              : 'error'
                          }
                        />
                      </Box>
                      <LinearProgress
                        variant="determinate"
                        value={numValue}
                        sx={{ height: 6, borderRadius: 3 }}
                        color={
                          numValue >= 80
                            ? 'success'
                            : numValue >= 60
                            ? 'warning'
                            : 'error'
                        }
                      />
                    </Box>
                  )
                })}
            </Paper>
          </Grid>

          {/* Account Details */}
          {report.report_data?.accounts && report.report_data.accounts.length > 0 && (
            <Grid item xs={12}>
              <Paper sx={{ p: 3 }}>
                <Typography variant="h6" fontWeight={600} gutterBottom>
                  Credit Accounts
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                  {report.report_data.accounts.length} account(s) found
                </Typography>
                <Grid container spacing={2}>
                  {report.report_data.accounts.map((account: any, index: number) => (
                    <Grid item xs={12} sm={6} md={4} key={index}>
                      <Card variant="outlined">
                        <CardContent>
                          <Typography variant="subtitle2" fontWeight={600} gutterBottom>
                            {account.type}
                          </Typography>
                          <Typography variant="body2" color="text.secondary" gutterBottom>
                            Status: {account.status}
                          </Typography>
                          <Typography variant="body2" color="text.secondary">
                            Balance: ${account.balance?.toLocaleString() || '0'}
                          </Typography>
                          {account.credit_limit && (
                            <Typography variant="body2" color="text.secondary">
                              Limit: ${account.credit_limit.toLocaleString()}
                            </Typography>
                          )}
                        </CardContent>
                      </Card>
                    </Grid>
                  ))}
                </Grid>
              </Paper>
            </Grid>
          )}
        </Grid>
      )}

      {!report && !loading && (
        <Paper
          sx={{
            p: 8,
            textAlign: 'center',
            bgcolor: 'background.default',
          }}
        >
          <AssessmentIcon sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
          <Typography variant="h6" gutterBottom>
            No Credit Report Available
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
            Generate your credit report to view your score and account details
          </Typography>
        </Paper>
      )}
    </Container>
  )
}
