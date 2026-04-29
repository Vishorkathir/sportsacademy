import { Box, Button, Paper, Stack, Typography } from '@mui/material'

export default function Boardcast() {
	return (
		<Paper
			elevation={0}
			sx={{
				borderRadius: 2.5,
				border: '1px solid #eef2f7',
				bgcolor: '#fff',
				overflow: 'hidden',
			}}
		>
			<Box sx={{ p: 2.5, borderBottom: '1px solid #f1f5f9' }}>
				<Stack direction="row" alignItems="center" gap={1}>
					<Box
						sx={{
							width: 28,
							height: 28,
							borderRadius: 1.5,
							bgcolor: '#e0f2fe',
							color: '#0284c7',
							display: 'grid',
							placeItems: 'center',
							fontSize: 16,
						}}
					>
						📣
					</Box>
					<Typography sx={{ fontSize: 16, fontWeight: 700, color: '#0f172a' }}>
						Broadcast
					</Typography>
				</Stack>
				<Typography sx={{ fontSize: 12.2, color: '#94a3b8', mt: 0.4 }}>
					Send a message to all active groups
				</Typography>
			</Box>

			<Box sx={{ p: 2.5 }}>
				<Typography sx={{ fontSize: 10.5, fontWeight: 700, color: '#94a3b8', letterSpacing: 1, mb: 0.8 }}>
					RECIPIENTS
				</Typography>
				<Box
					sx={{
						height: 40,
						borderRadius: 1.5,
						bgcolor: '#f8fafc',
						border: '1px solid #eef2f7',
						px: 1.5,
						display: 'flex',
						alignItems: 'center',
						justifyContent: 'space-between',
						color: '#0f172a',
						fontSize: 12.5,
						mb: 2.2,
					}}
				>
					<span>All Students (248)</span>
					<span style={{ color: '#94a3b8' }}>▾</span>
				</Box>

				<Typography sx={{ fontSize: 10.5, fontWeight: 700, color: '#94a3b8', letterSpacing: 1, mb: 0.8 }}>
					SUBJECT
				</Typography>
				<Box
					component="input"
					placeholder="e.g. Schedule Update"
					sx={{
						width: '100%',
						height: 40,
						borderRadius: 1.5,
						bgcolor: '#f8fafc',
						border: '1px solid #eef2f7',
						px: 1.5,
						fontSize: 12.5,
						color: '#64748b',
						mb: 2.2,
						outline: 'none',
					}}
				/>

				<Typography sx={{ fontSize: 10.5, fontWeight: 700, color: '#94a3b8', letterSpacing: 1, mb: 0.8 }}>
					MESSAGE BODY
				</Typography>
				<Box
					component="textarea"
					placeholder="Write your announcement here..."
					sx={{
						width: '100%',
						minHeight: 120,
						borderRadius: 1.5,
						bgcolor: '#f8fafc',
						border: '1px solid #eef2f7',
						px: 1.5,
						py: 1.2,
						fontSize: 12.5,
						color: '#64748b',
						outline: 'none',
						resize: 'none',
						mb: 1.6,
					}}
				/>

				<Stack direction="row" alignItems="center" gap={0.8} sx={{ color: '#94a3b8', fontSize: 11.5, mb: 2.2 }}>
					<span>📎</span>
					<span>Attach training schedule or PDF</span>
				</Stack>
			</Box>

			<Box sx={{ p: 2.5, borderTop: '1px solid #f1f5f9' }}>
				<Button
					fullWidth
					variant="contained"
					sx={{
						bgcolor: '#0b5aa0',
						color: '#fff',
						textTransform: 'none',
						fontSize: 12.8,
						fontWeight: 600,
						py: 1.1,
						borderRadius: 1.5,
						'&:hover': { bgcolor: '#094a83' },
					}}
				>
					➤ Send Announcement
				</Button>
			</Box>
		</Paper>
	)
}
