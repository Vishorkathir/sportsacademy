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
import AdminLayout from './AdminLayout'

const metrics = [
  { icon: '👥', label: 'Total Students', value: '1,284', delta: '+15%', color: '#3b82f6' },
  { icon: '🏏', label: 'Matches Today', value: '8', delta: '', color: '#22c55e' },
  { icon: '✅', label: 'Active Status', value: '85', badge: 'Active', color: '#f59e0b' },
  { icon: '💰', label: 'Total Payment', value: '12', delta: '', color: '#ef4444' },
]

const studentData = [
  { initials: 'SK', name: 'Sonia Khan', skill: 'Bowling Analysis', status: 'Excellent', time: '4h ago' },
  { initials: 'SK', name: 'Sonia Khan', skill: 'Bowling Analysis', status: 'Excellent', time: '4h ago' },
  { initials: 'SK', name: 'Sonia Khan', skill: 'Bowling Analysis', status: 'Good', time: '4h ago' },
]

function MetricCard({ icon, label, value, delta, badge, color }) {
  return (
    <Paper
      elevation={0}
      sx={{
        p: 2,
        borderRadius: 2,
        border: '1px solid #e8edf5',
        bgcolor: '#fff',
      }}
    >
      <Stack direction="row" justifyContent="space-between" alignItems="flex-start" sx={{ mb: 1.2 }}>
        <Box
          sx={{
            width: 40,
            height: 40,
            borderRadius: 2,
            bgcolor: `${color}18`,
            display: 'grid',
            placeItems: 'center',
            fontSize: 20,
          }}
        >
          {icon}
        </Box>
        {delta && (
          <Chip
            label={delta}
            size="small"
            sx={{
              bgcolor: '#d1fae5',
              color: '#059669',
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
              bgcolor: '#d1fae5',
              color: '#059669',
              fontWeight: 700,
              fontSize: 11,
            }}
          />
        )}
      </Stack>
      <Typography sx={{ fontSize: 12, color: '#64748b', mb: 0.4 }}>
        {label}
      </Typography>
      <Typography sx={{ fontSize: 28, fontWeight: 700, color: '#0f172a' }}>
        {value}
      </Typography>
    </Paper>
  )
}

export default function Dashboard() {
  return (
    <AdminLayout>
      <Box>
        {/* Top Bar */}
        <Box
          sx={{
            height: 74,
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
                width: 350,
                px: 2,
                py: 1,
                borderRadius: 2,
                border: '1px solid #e8edf5',
                fontSize: 13,
                color: '#64748b',
                '&::placeholder': { color: '#cbd5e1' },
              }}
            />

            <Stack direction="row" alignItems="center" gap={2}>
              <IconButton sx={{ border: '1px solid #e8edf5', borderRadius: 1.5 }}>
                🔔
              </IconButton>
              <Avatar sx={{ width: 36, height: 36, bgcolor: '#1d4ed8' }}>A</Avatar>
            </Stack>
          </Stack>
        </Box>

        {/* Main Content */}
        <Box sx={{ p: 3 }}>
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
              sx={{
                bgcolor: '#1d4ed8',
                color: '#fff',
                textTransform: 'none',
                fontSize: 13,
                fontWeight: 600,
                py: 1,
                px: 2,
                borderRadius: 1.5,
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
          <Paper elevation={0} sx={{ p: 2.5, borderRadius: 2, border: '1px solid #e8edf5', bgcolor: '#fff' }}>
            <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 2 }}>
              <Typography sx={{ fontSize: 16, fontWeight: 700, color: '#0f172a' }}>
                Recent Student Activities
              </Typography>
              <Box sx={{ display: 'flex', gap: 1, alignItems: 'center' }}>
                <Box
                  component="input"
                  type="text"
                  placeholder="Search results..."
                  sx={{
                    px: 2,
                    py: 0.8,
                    borderRadius: 1.5,
                    border: '1px solid #e8edf5',
                    fontSize: 12,
                    color: '#64748b',
                    width: 180,
                  }}
                />
                <Chip
                  label="+ Register"
                  sx={{
                    bgcolor: '#f9b90e',
                    color: '#7b4e00',
                    fontWeight: 700,
                    cursor: 'pointer',
                  }}
                />
              </Box>
            </Stack>

            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow sx={{ borderBottom: '2px solid #e8edf5' }}>
                    <TableCell sx={{ fontSize: 11, fontWeight: 700, color: '#64748b', textTransform: 'uppercase' }}>
                      Student Name
                    </TableCell>
                    <TableCell sx={{ fontSize: 11, fontWeight: 700, color: '#64748b', textTransform: 'uppercase' }}>
                      Skill
                    </TableCell>
                    <TableCell sx={{ fontSize: 11, fontWeight: 700, color: '#64748b', textTransform: 'uppercase' }}>
                      Place
                    </TableCell>
                    <TableCell sx={{ fontSize: 11, fontWeight: 700, color: '#64748b', textTransform: 'uppercase' }}>
                      Payment Status
                    </TableCell>
                    <TableCell sx={{ fontSize: 11, fontWeight: 700, color: '#64748b', textTransform: 'uppercase' }}>
                      Time
                    </TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {studentData.map((row, idx) => (
                    <TableRow key={idx} sx={{ borderBottom: '1px solid #e8edf5' }}>
                      <TableCell>
                        <Stack direction="row" alignItems="center" gap={1.2}>
                          <Avatar
                            sx={{
                              width: 28,
                              height: 28,
                              bgcolor: '#1d4ed8',
                              fontSize: 11,
                              fontWeight: 700,
                            }}
                          >
                            {row.initials}
                          </Avatar>
                          <Typography sx={{ fontSize: 12.5, color: '#0f172a', fontWeight: 500 }}>
                            {row.name}
                          </Typography>
                        </Stack>
                      </TableCell>
                      <TableCell sx={{ fontSize: 12.5, color: '#0f172a' }}>
                        {row.skill}
                      </TableCell>
                      <TableCell>
                        <Chip
                          label={row.status}
                          size="small"
                          sx={{
                            bgcolor: row.status === 'Excellent' ? '#dbeafe' : '#fef3c7',
                            color: row.status === 'Excellent' ? '#1d4ed8' : '#92400e',
                            fontWeight: 600,
                            fontSize: 11,
                          }}
                        />
                      </TableCell>
                      <TableCell sx={{ fontSize: 12.5, color: '#0f172a', fontWeight: 600 }}>
                        {row.status}
                      </TableCell>
                      <TableCell sx={{ fontSize: 12.5, color: '#64748b' }}>
                        {row.time}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>

            <Stack direction="row" justifyContent="center" sx={{ mt: 2 }}>
              <Typography
                sx={{ fontSize: 12.5, color: '#2563eb', cursor: 'pointer', fontWeight: 600 }}
              >
                View All
              </Typography>
            </Stack>
          </Paper>
        </Box>
      </Box>
    </AdminLayout>
  )
}
