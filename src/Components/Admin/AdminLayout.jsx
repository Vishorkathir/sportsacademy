import { Box } from '@mui/material'
import Sidebar from './Sidebar'

export default function AdminLayout({ children }) {
  return (
    <Box sx={{ display: 'flex' }}>
      <Sidebar />
      <Box sx={{ marginLeft: 280, width: '100%', minHeight: '100vh', bgcolor: '#f8f9fb' }}>
        {children}
      </Box>
    </Box>
  )
}
