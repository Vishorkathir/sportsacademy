import { Box } from '@mui/material'
import Sidebar from './Sidebar'

export default function AdminLayout({ children }) {
  return (
    <Box sx={{ display: 'flex', bgcolor: '#f5f7fb' }}>
      <Sidebar />
      <Box
        sx={{
          marginLeft: 32,
          width: '100%',
          minHeight: '100vh',
          bgcolor: '#f5f7fb',
        }}
      >
        {children}
      </Box>
    </Box>
  )
}
