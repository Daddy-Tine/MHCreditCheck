import { useState, useEffect } from 'react'
import {
  Container,
  Typography,
  Box,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  IconButton,
  Chip,
  Alert,
  Tooltip,
} from '@mui/material'
import { CheckCircle, Cancel } from '@mui/icons-material'
import { useAuth } from '../../context/AuthContext'
import api from '../../services/api'
import SkeletonTable from '../../components/Loading/SkeletonTable'

interface Bank {
  id: number
  name: string
  license_number: string
  contact_email: string
  is_active: boolean
  is_approved: boolean
  created_at: string
}

export default function Banks() {
  const { user } = useAuth()
  const [banks, setBanks] = useState<Bank[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchBanks()
  }, [])

  const fetchBanks = async () => {
    try {
      const response = await api.get('/api/v1/banks/', {
        params: { skip: 0, limit: 100 },
      })
      setBanks(response.data.data || [])
    } catch (err: any) {
      setError(err.response?.data?.error?.detail || 'Failed to fetch banks')
    } finally {
      setLoading(false)
    }
  }

  const handleApprove = async (bankId: number, approve: boolean) => {
    try {
      await api.post(`/api/v1/banks/${bankId}/approve`, {
        is_approved: approve,
      })
      fetchBanks()
    } catch (err: any) {
      setError(err.response?.data?.error?.detail || 'Failed to update bank')
    }
  }

  return (
    <Container maxWidth="lg">
      <Box sx={{ mb: 3 }}>
        <Typography variant="h4" component="h1" fontWeight={600} gutterBottom>
          Bank Management
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Approve and manage registered banks
        </Typography>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError('')}>
          {error}
        </Alert>
      )}

      {loading ? (
        <SkeletonTable rows={5} columns={6} />
      ) : (
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell><strong>ID</strong></TableCell>
                <TableCell><strong>Name</strong></TableCell>
                <TableCell><strong>License Number</strong></TableCell>
                <TableCell><strong>Contact Email</strong></TableCell>
                <TableCell><strong>Status</strong></TableCell>
                <TableCell><strong>Actions</strong></TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {banks.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={6} align="center" sx={{ py: 4 }}>
                    <Typography color="text.secondary">No banks registered</Typography>
                  </TableCell>
                </TableRow>
              ) : (
                banks.map((bank) => (
                  <TableRow key={bank.id} hover>
                    <TableCell>{bank.id}</TableCell>
                    <TableCell>
                      <Typography fontWeight={500}>{bank.name}</Typography>
                    </TableCell>
                    <TableCell>{bank.license_number}</TableCell>
                    <TableCell>{bank.contact_email}</TableCell>
                    <TableCell>
                      <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                        <Chip
                          label={bank.is_active ? 'Active' : 'Inactive'}
                          color={bank.is_active ? 'success' : 'default'}
                          size="small"
                        />
                        <Chip
                          label={bank.is_approved ? 'Approved' : 'Pending'}
                          color={bank.is_approved ? 'success' : 'warning'}
                          size="small"
                        />
                      </Box>
                    </TableCell>
                    <TableCell>
                      {!bank.is_approved && (
                        <Box sx={{ display: 'flex', gap: 1 }}>
                          <Tooltip title="Approve Bank">
                            <IconButton
                              size="small"
                              color="success"
                              onClick={() => handleApprove(bank.id, true)}
                            >
                              <CheckCircle />
                            </IconButton>
                          </Tooltip>
                          <Tooltip title="Reject Bank">
                            <IconButton
                              size="small"
                              color="error"
                              onClick={() => handleApprove(bank.id, false)}
                            >
                              <Cancel />
                            </IconButton>
                          </Tooltip>
                        </Box>
                      )}
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </TableContainer>
      )}
    </Container>
  )
}

