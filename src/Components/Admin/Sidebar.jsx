import { Box, Button, Stack, Typography } from '@mui/material'

const menuItems = [
  { label: 'Student Activities', icon: '👥' },
  { label: 'Match Information', icon: '🏏' },
  { label: 'Media Upload', icon: '📤' },
  { label: 'Shop Information', icon: '🛒' },
  { label: 'Settings', icon: '⚙️' },
]

export default function Sidebar() {
  return (
    <Box
      sx={{
        width: 280,
        bgcolor: '#f8f9fb',
        borderRight: '1px solid #e8edf5',
        display: 'flex',
        flexDirection: 'column',
        height: '100vh',
        position: 'fixed',
        left: 0,
        top: 0,
      }}
    >
      {/* Logo */}
      <Box sx={{ p: 2.5, borderBottom: '1px solid #e8edf5' }}>
        <Stack direction="row" alignItems="center" gap={1}>
          <Box
            sx={{
              width: 32,
              height: 32,
              borderRadius: 1.5,
              bgcolor: '#0b5aa0',
              color: '#fff',
              display: 'grid',
              placeItems: 'center',
              fontSize: 16,
            }}
          >
            🏆
          </Box>
          <Typography sx={{ fontSize: 14, fontWeight: 700, color: '#0f172a' }}>
            Kings11Sports<br/>Academy
          </Typography>
        </Stack>
      </Box>

      {/* Menu Section */}
      <Box sx={{ p: 2, flex: 1 }}>
        <Typography sx={{ fontSize: 12, fontWeight: 700, color: '#64748b', mb: 1 }}>
          Adminer's
        </Typography>
        <Typography sx={{ fontSize: 11.5, color: '#94a3b8', mb: 2.2 }}>
          Excellence in Performance
        </Typography>

        <Stack gap={0.5}>
          {menuItems.map((item) => (
            <Box
              key={item.label}
              sx={{
                p: 1.5,
                borderRadius: 2,
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: 1.2,
                color: '#64748b',
                transition: 'all 0.2s',
                '&:hover': {
                  bgcolor: '#e8edf5',
                  color: '#0b5aa0',
                },
              }}
            >
              <Box sx={{ fontSize: 16 }}>{item.icon}</Box>
              <Typography sx={{ fontSize: 12.5, fontWeight: 500 }}>
                {item.label}
              </Typography>
            </Box>
          ))}
        </Stack>
      </Box>

      {/* Buttons */}
      <Box sx={{ p: 2, borderTop: '1px solid #e8edf5' }}>
        <Button
          fullWidth
          variant="contained"
          sx={{
            bgcolor: '#1d4ed8',
            color: '#fff',
            textTransform: 'none',
            fontSize: 12.5,
            fontWeight: 600,
            py: 1.2,
            borderRadius: 2,
            mb: 1,
            '&:hover': { bgcolor: '#1e40af' },
          }}
        >
          Upgrade to Pro
        </Button>
        <Button
          fullWidth
          variant="contained"
          sx={{
            bgcolor: '#f9b90e',
            color: '#7b4e00',
            textTransform: 'none',
            fontSize: 12.5,
            fontWeight: 600,
            py: 1.2,
            borderRadius: 2,
            '&:hover': { bgcolor: '#f1b000' },
          }}
        >
          View Benefits
        </Button>
      </Box>
    </Box>
  )
}
