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
} from '@mui/material'
import { useAuth } from '../../context/AuthContext'
import api from '../../services/api'

export default function CreditInquiry() {
  // const { user } = useAuth() // Reserved for future use
  const [loading, setLoading] = useState(false)
  const [success, setSuccess] = useState('')
  const [error, setError] = useState('')
  const [formData, setFormData] = useState({
    consumer_id: '',
    purpose: 'LOAN_APPLICATION',
    purpose_description: '',
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    setSuccess('')

    try {
      await api.post('/api/v1/inquiries/', {
        consumer_id: parseInt(formData.consumer_id),
        purpose: formData.purpose,
        purpose_description: formData.purpose_description,
      })
      setSuccess('Credit inquiry submitted successfully!')
      setFormData({
        consumer_id: '',
        purpose: 'LOAN_APPLICATION',
        purpose_description: '',
      })
    } catch (err: any) {
      setError(err.response?.data?.error?.detail || 'Failed to submit inquiry')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Container maxWidth="md">
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" fontWeight={600} gutterBottom>
          Credit Inquiry
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Request a credit report for a consumer
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
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                label="Purpose"
                select
                value={formData.purpose}
                onChange={(e) =>
                  setFormData({ ...formData, purpose: e.target.value })
                }
                fullWidth
                required
              >
                <MenuItem value="LOAN_APPLICATION">Loan Application</MenuItem>
                <MenuItem value="CREDIT_CARD_APPLICATION">
                  Credit Card Application
                </MenuItem>
                <MenuItem value="EMPLOYMENT">Employment</MenuItem>
                <MenuItem value="RENTAL_APPLICATION">Rental Application</MenuItem>
                <MenuItem value="INSURANCE">Insurance</MenuItem>
                <MenuItem value="ACCOUNT_REVIEW">Account Review</MenuItem>
                <MenuItem value="OTHER">Other</MenuItem>
              </TextField>
            </Grid>
            <Grid item xs={12}>
              <TextField
                label="Purpose Description"
                multiline
                rows={4}
                value={formData.purpose_description}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    purpose_description: e.target.value,
                  })
                }
                fullWidth
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
                {loading ? 'Submitting...' : 'Submit Inquiry'}
              </Button>
            </Grid>
          </Grid>
        </form>
      </Paper>
    </Container>
  )
}

