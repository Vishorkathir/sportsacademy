import {
  Avatar,
  Box,
  Button,
  Chip,
  Grid,
  IconButton,
  Paper,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
} from '@mui/material'
import { useNavigate } from 'react-router-dom'
import AdminLayout from './AdminLayout'
import Boardcast from '../AdminPage/boardcast'

const metrics = [
  { icon: '👥', label: 'Total Students', value: '1,284', delta: '+12%', color: '#3b82f6' },
  { icon: '🏏', label: 'Matches Today', value: '8', delta: '', color: '#22c55e' },
  { icon: '✅', label: 'Active Status', value: '83', badge: 'Active', color: '#f59e0b' },
  { icon: '💰', label: 'Total Payment', value: '12', delta: '', color: '#ef4444' },
]

const studentData = [
  { initials: 'SK', name: 'Sonia Khan', skill: 'Bowling Analysis', place: 'Excellent', payment: '4h ago', time: '4h ago' },
  { initials: 'SK', name: 'Sonia Khan', skill: 'Bowling Analysis', place: 'Excellent', payment: '4h ago', time: '4h ago' },
  { initials: 'SK', name: 'Sonia Khan', skill: 'Bowling Analysis', place: 'Good', payment: '4h ago', time: '4h ago' },
]

function MetricCard({ icon, label, value, delta, badge, color }) {
  return (
    <Paper
      elevation={0}
      sx={{
        p: 1.8,
        borderRadius: 2.5,
        border: '1px solid #e8edf5',
        bgcolor: '#fff',
        minHeight: 110,
        boxShadow: '0 10px 20px rgba(15, 23, 42, 0.05)',
      }}
    >
      <Stack direction="row" justifyContent="space-between" alignItems="flex-start" sx={{ mb: 1.2 }}>
        <Box
          sx={{
            width: 38,
            height: 38,
            borderRadius: 2,
            bgcolor: '#f8fafc',
            border: '1px solid #e8edf5',
            display: 'grid',
            placeItems: 'center',
            fontSize: 18,
            color,
          }}
        >
          {icon}
        </Box>
        {delta && (
          <Chip
            label={delta}
            size="small"
            sx={{
              bgcolor: '#dcfce7',
              color: '#16a34a',
              fontWeight: 700,
              fontSize: 11,
            }}
          />
        )}
        {badge && (
          <Chip
            label={badge}
            size="small"
            sx={{
              bgcolor: '#dcfce7',
              color: '#16a34a',
              fontWeight: 700,
              fontSize: 11,
            }}
          />
        )}
      </Stack>
      <Typography sx={{ fontSize: 12, color: '#94a3b8', mb: 0.4 }}>
        {label}
      </Typography>
      <Typography sx={{ fontSize: 26, fontWeight: 700, color: '#0f172a' }}>
        {value}
      </Typography>
    </Paper>
  )
}

export default function Dashboard() {
  const navigate = useNavigate()
  return (
    <AdminLayout>
      <Box>
        {/* Top Bar */}
        <Box
          sx={{
            height: 68,
            borderBottom: '1px solid #e8edf5',
            bgcolor: '#fff',
            display: 'flex',
            alignItems: 'center',
            px: 3,
          }}
        >
          <Stack direction="row" alignItems="center" justifyContent="space-between" sx={{ width: '100%' }}>
            <Box
              component="input"
              type="text"
              placeholder="Search students, matches, or media..."
              sx={{
                width: 420,
                px: 2.2,
                py: 0.9,
                borderRadius: 999,
                border: '1px solid #e8edf5',
                fontSize: 12.5,
                color: '#64748b',
                bgcolor: '#f8fafc',
                '&::placeholder': { color: '#cbd5e1' },
              }}
            />

            <Stack direction="row" alignItems="center" gap={1.6}>
              <IconButton sx={{ border: '1px solid #e8edf5', borderRadius: 1.5, width: 34, height: 34 }}>
                🔔
              </IconButton>
              <Avatar sx={{ width: 34, height: 34, bgcolor: '#1d4ed8' }}>A</Avatar>
            </Stack>
          </Stack>
        </Box>

        {/* Main Content */}
        <Box sx={{ p: 3, maxWidth: 1020 }}>
          <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 3 }}>
            <Box>
              <Typography sx={{ fontSize: 28, fontWeight: 700, color: '#0f172a' }}>
                Dashboard Overview
              </Typography>
              <Typography sx={{ fontSize: 13, color: '#64748b' }}>
                Welcome back, Academy Admin. Here's your performance summary for today.
              </Typography>
            </Box>
            <Button
              variant="contained"
              onClick={() => navigate('/registration')}
              sx={{
                bgcolor: '#1d4ed8',
                color: '#fff',
                textTransform: 'none',
                fontSize: 12.5,
                fontWeight: 600,
                py: 0.9,
                px: 2.2,
                borderRadius: 2,
                '&:hover': { bgcolor: '#1e40af' },
              }}
            >
              + New Registration
            </Button>
          </Stack>

          {/* Metrics Grid */}
          <Grid container spacing={2} sx={{ mb: 3 }}>
            {metrics.map((item) => (
              <Grid item xs={12} sm={6} lg={3} key={item.label}>
                <MetricCard {...item} />
              </Grid>
            ))}
          </Grid>

          {/* Recent Student Activities */}
          <Paper elevation={0} sx={{ p: 2.5, borderRadius: 2.5, border: '1px solid #e8edf5', bgcolor: '#fff' }}>
            <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 1.5 }}>
              <Typography sx={{ fontSize: 16, fontWeight: 700, color: '#0f172a' }}>
                Recent Student Activities
              </Typography>
              <Typography sx={{ fontSize: 12.5, color: '#2563eb', fontWeight: 600, cursor: 'pointer' }}>
                View All
              </Typography>
            </Stack>

            <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 2 }}>
              <Box
                component="input"
                type="text"
                placeholder="Search roster..."
                sx={{
                  px: 2,
                  py: 0.8,
                  borderRadius: 1.5,
                  border: '1px solid #e8edf5',
                  fontSize: 12,
                  color: '#64748b',
                  width: 220,
                  bgcolor: '#f8fafc',
                }}
              />
              <Chip
                label="+ Register"
                sx={{
                  bgcolor: '#f9b90e',
                  color: '#7b4e00',
                  fontWeight: 700,
                  cursor: 'pointer',
                  px: 1.2,
                }}
              />
            </Stack>

            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow sx={{ borderBottom: '1px solid #e8edf5', bgcolor: '#f8fafc' }}>
                    <TableCell sx={{ fontSize: 10.5, fontWeight: 700, color: '#94a3b8', textTransform: 'uppercase', py: 1.2 }}>
                      Student Name
                    </TableCell>
                    <TableCell sx={{ fontSize: 10.5, fontWeight: 700, color: '#94a3b8', textTransform: 'uppercase', py: 1.2 }}>
                      Skill
                    </TableCell>
                    <TableCell sx={{ fontSize: 10.5, fontWeight: 700, color: '#94a3b8', textTransform: 'uppercase', py: 1.2 }}>
                      Place
                    </TableCell>
                    <TableCell sx={{ fontSize: 10.5, fontWeight: 700, color: '#94a3b8', textTransform: 'uppercase', py: 1.2 }}>
                      Payment Status
                    </TableCell>
                    <TableCell sx={{ fontSize: 10.5, fontWeight: 700, color: '#94a3b8', textTransform: 'uppercase', py: 1.2 }}>
                      Time
                    </TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {studentData.map((row, idx) => (
                    <TableRow key={idx} sx={{ borderBottom: '1px solid #eef2f7' }}>
                      <TableCell>
                        <Stack direction="row" alignItems="center" gap={1.2}>
                          <Avatar
                            sx={{
                              width: 28,
                              height: 28,
                              bgcolor: '#facc15',
                              color: '#7c2d12',
                              fontSize: 10.5,
                              fontWeight: 700,
                            }}
                          >
                            {row.initials}
                          </Avatar>
                          <Typography sx={{ fontSize: 12.5, color: '#0f172a', fontWeight: 600 }}>
                            {row.name}
                          </Typography>
                        </Stack>
                      </TableCell>
                      <TableCell sx={{ fontSize: 12.5, color: '#334155' }}>
                        {row.skill}
                      </TableCell>
                      <TableCell>
                        <Chip
                          label={row.place}
                          size="small"
                          sx={{
                            bgcolor: row.place === 'Excellent' ? '#dbeafe' : '#e2e8f0',
                            color: row.place === 'Excellent' ? '#1d4ed8' : '#475569',
                            fontWeight: 600,
                            fontSize: 11,
                          }}
                        />
                      </TableCell>
                      <TableCell sx={{ fontSize: 12.5, color: '#64748b' }}>
                        {row.payment}
                      </TableCell>
                      <TableCell sx={{ fontSize: 12.5, color: '#64748b' }}>
                        {row.time}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Paper>

          <Box sx={{ mt: 3, maxWidth: 420 }}>
            <Boardcast />
          </Box>
        </Box>
      </Box>
    </AdminLayout>
  )
}