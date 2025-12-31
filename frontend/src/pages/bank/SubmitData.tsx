import { useState } from 'react'
import {
  Container,
  Typography,
  Box,
  Paper,
  TextField,
  Button,
  MenuItem,
  Alert,
  Grid,
  InputAdornment,
} from '@mui/material'
import { AccountBalance, CalendarToday, AttachMoney } from '@mui/icons-material'
import { useAuth } from '../../context/AuthContext'
import api from '../../services/api'

export default function SubmitData() {
  // const { user } = useAuth() // Reserved for future use
  const [loading, setLoading] = useState(false)
  const [success, setSuccess] = useState('')
  const [error, setError] = useState('')
  const [formData, setFormData] = useState({
    consumer_id: '',
    account_number: '',
    account_type: 'CREDIT_CARD',
    account_status: 'OPEN',
    payment_status: 'CURRENT',
    current_balance: '',
    credit_limit: '',
    open_date: '',
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    setSuccess('')

    try {
      await api.post('/api/v1/credit-data/', {
        ...formData,
        consumer_id: parseInt(formData.consumer_id),
        current_balance: parseFloat(formData.current_balance),
        credit_limit: formData.credit_limit
          ? parseFloat(formData.credit_limit)
          : null,
      })
      setSuccess('Credit data submitted successfully!')
      setFormData({
        consumer_id: '',
        account_number: '',
        account_type: 'CREDIT_CARD',
        account_status: 'OPEN',
        payment_status: 'CURRENT',
        current_balance: '',
        credit_limit: '',
        open_date: '',
      })
    } catch (err: any) {
      setError(err.response?.data?.error?.detail || 'Failed to submit data')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Container maxWidth="md">
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" fontWeight={600} gutterBottom>
          Submit Credit Data
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Submit credit account information for consumers
        </Typography>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError('')}>
          {error}
        </Alert>
      )}

      {success && (
        <Alert severity="success" sx={{ mb: 2 }} onClose={() => setSuccess('')}>
          {success}
        </Alert>
      )}

      <Paper sx={{ p: 3 }}>
        <form onSubmit={handleSubmit}>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <TextField
                label="Consumer ID"
                type="number"
                value={formData.consumer_id}
                onChange={(e) =>
                  setFormData({ ...formData, consumer_id: e.target.value })
                }
                fullWidth
                required
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <AccountBalance />
                    </InputAdornment>
                  ),
                }}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                label="Account Number"
                value={formData.account_number}
                onChange={(e) =>
                  setFormData({ ...formData, account_number: e.target.value })
                }
                fullWidth
                required
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                label="Account Type"
                select
                value={formData.account_type}
                onChange={(e) =>
                  setFormData({ ...formData, account_type: e.target.value })
                }
                fullWidth
                required
              >
                <MenuItem value="CREDIT_CARD">Credit Card</MenuItem>
                <MenuItem value="MORTGAGE">Mortgage</MenuItem>
                <MenuItem value="AUTO_LOAN">Auto Loan</MenuItem>
                <MenuItem value="PERSONAL_LOAN">Personal Loan</MenuItem>
                <MenuItem value="STUDENT_LOAN">Student Loan</MenuItem>
                <MenuItem value="LINE_OF_CREDIT">Line of Credit</MenuItem>
                <MenuItem value="OTHER">Other</MenuItem>
              </TextField>
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                label="Account Status"
                select
                value={formData.account_status}
                onChange={(e) =>
                  setFormData({ ...formData, account_status: e.target.value })
                }
                fullWidth
                required
              >
                <MenuItem value="OPEN">Open</MenuItem>
                <MenuItem value="CLOSED">Closed</MenuItem>
                <MenuItem value="DELINQUENT">Delinquent</MenuItem>
                <MenuItem value="CHARGE_OFF">Charge Off</MenuItem>
                <MenuItem value="COLLECTION">Collection</MenuItem>
                <MenuItem value="BANKRUPTCY">Bankruptcy</MenuItem>
              </TextField>
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                label="Payment Status"
                select
                value={formData.payment_status}
                onChange={(e) =>
                  setFormData({ ...formData, payment_status: e.target.value })
                }
                fullWidth
                required
              >
                <MenuItem value="CURRENT">Current</MenuItem>
                <MenuItem value="LATE_30">Late 30 Days</MenuItem>
                <MenuItem value="LATE_60">Late 60 Days</MenuItem>
                <MenuItem value="LATE_90">Late 90 Days</MenuItem>
                <MenuItem value="LATE_120_PLUS">Late 120+ Days</MenuItem>
                <MenuItem value="NO_PAYMENT">No Payment</MenuItem>
              </TextField>
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                label="Current Balance"
                type="number"
                value={formData.current_balance}
                onChange={(e) =>
                  setFormData({ ...formData, current_balance: e.target.value })
                }
                fullWidth
                required
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <AttachMoney />
                    </InputAdornment>
                  ),
                }}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                label="Credit Limit"
                type="number"
                value={formData.credit_limit}
                onChange={(e) =>
                  setFormData({ ...formData, credit_limit: e.target.value })
                }
                fullWidth
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <AttachMoney />
                    </InputAdornment>
                  ),
                }}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                label="Open Date"
                type="date"
                value={formData.open_date}
                onChange={(e) =>
                  setFormData({ ...formData, open_date: e.target.value })
                }
                fullWidth
                required
                InputLabelProps={{ shrink: true }}
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <CalendarToday sx={{ color: 'text.secondary' }} />
                    </InputAdornment>
                  ),
                }}
              />
            </Grid>
            <Grid item xs={12}>
              <Button
                type="submit"
                variant="contained"
                fullWidth
                size="large"
                disabled={loading}
                sx={{ py: 1.5, mt: 2 }}
              >
                {loading ? 'Submitting...' : 'Submit Credit Data'}
              </Button>
            </Grid>
          </Grid>
        </form>
      </Paper>
    </Container>
  )
}

