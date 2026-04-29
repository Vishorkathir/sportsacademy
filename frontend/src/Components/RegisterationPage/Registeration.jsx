import {
	Avatar,
	Box,
	Checkbox,
	Grid,
	LinearProgress,
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
import AdminLayout from '../Admin/AdminLayout'

const detailRows = [
	{ label: 'USER ID', value: 'ECA-2024-089', placeholder: 'Enter user id' },
	{ label: 'AGE', value: '16 Years', placeholder: 'Enter age' },
	{ label: 'DATE OF BIRTH', value: '12/05/2008', placeholder: 'DD/MM/YYYY' },
	{ label: 'GENDER', value: 'Male', placeholder: 'Enter gender' },
	{ label: 'ADDRESS', value: '', placeholder: 'Enter address' },
	{ label: 'PIN CODE', value: '560001', placeholder: 'Enter pin code' },
	{ label: 'PARENT NAME', value: 'Robert Smith', placeholder: 'Enter parent name' },
	{ label: 'PARENT OCCUPATION', value: 'Senior Engineer', placeholder: 'Enter occupation' },
	{ label: 'PARENT MOBILE', value: '+91 98765 43210', placeholder: 'Enter mobile number' },
	{ label: 'ENROLLMENT STATUS', value: 'ACTIVE', placeholder: 'ACTIVE', readOnly: true },
	{ label: 'PROCESS STATUS', value: 'COMPLETED', placeholder: 'COMPLETED', readOnly: true },
	{ label: 'ACADEMY NAME', value: 'Elite Cricket Main Hub', placeholder: 'Enter academy name' },
	{ label: 'COURSE NAME', value: 'Advanced Performance Pro', placeholder: 'Enter course name' },
	{ label: 'GROUP NAME', value: 'U-19 Elite Batsmen', placeholder: 'Enter group name' },
]

const profileDetails = [
	{ label: 'Registered Name', value: 'Jason Statham', placeholder: 'Enter name' },
	{ label: 'Registered Mobile', value: '+91 77234 55671', placeholder: 'Enter mobile number' },
	{ label: 'Registered Date', value: 'Jan 14, 2024', placeholder: 'Enter date' },
]

const skillItems = [
	{ label: 'Batting', active: true },
	{ label: 'Bowling', active: false },
	{ label: 'Wicket Keeping', active: true },
]

const invoiceRows = [
	{ amount: '₹12,500.00', description: 'Advanced Coaching Fee', transactionId: '#TXN_0988712', status: 'Success' },
	{ amount: '₹12,500.00', description: 'Advanced Coaching Fee', transactionId: '#TXN_0977215', status: 'Success' },
	{ amount: '₹5,000.00', description: 'Cricket Kit & Apparel', transactionId: '#TXN_0961201', status: 'Success' },
]

function DetailField({ label, value, placeholder, highlight, readOnly }) {
	return (
		<Box>
			<Typography sx={{ fontSize: 10, fontWeight: 700, color: '#94a3b8', letterSpacing: 0.8, mb: 0.6 }}>
				{label}
			</Typography>
			<Box
				component="input"
				defaultValue={value}
				placeholder={placeholder}
				readOnly={readOnly}
				sx={{
					width: '100%',
					height: 34,
					px: 1.2,
					borderRadius: 1.4,
					border: '1px solid #eef2f7',
					bgcolor: '#f8fafc',
					fontSize: 12,
					color: highlight ? '#16a34a' : '#0f172a',
					fontWeight: highlight ? 700 : 500,
					outline: 'none',
				}}
			/>
		</Box>
	)
}

export default function Registeration() {
	return (
		<AdminLayout>
			<Box sx={{ p: 3, maxWidth: 960 }}>
				<Paper
					elevation={0}
					sx={{
						p: 2.2,
						borderRadius: 2.5,
						border: '1px solid #e8edf5',
						bgcolor: '#fff',
						mb: 3,
					}}
				>
					<Stack direction="row" alignItems="center" justifyContent="space-between" gap={2}>
						<Stack direction="row" alignItems="center" gap={1.2}>
							<Avatar sx={{ width: 38, height: 38, bgcolor: '#eff6ff', color: '#1d4ed8' }}>🛡️</Avatar>
							<Box>
								<Typography sx={{ fontSize: 14, fontWeight: 700, color: '#0f172a' }}>
									Registration Dashboard
								</Typography>
								<Typography sx={{ fontSize: 11.5, color: '#94a3b8' }}>
									Student Profile Completion
								</Typography>
							</Box>
						</Stack>

						<Box sx={{ flex: 1, maxWidth: 260 }}>
							<Stack direction="row" justifyContent="space-between" sx={{ mb: 0.6 }}>
								<Typography sx={{ fontSize: 10.5, color: '#94a3b8', fontWeight: 700 }}>
									PROFILE PROGRESS
								</Typography>
								<Typography sx={{ fontSize: 11.5, fontWeight: 700, color: '#0f172a' }}>
									100% Complete
								</Typography>
							</Stack>
							<LinearProgress
								variant="determinate"
								value={100}
								sx={{ height: 6, borderRadius: 999, bgcolor: '#e5e7eb', '& .MuiLinearProgress-bar': { bgcolor: '#1d4ed8' } }}
							/>
						</Box>
					</Stack>
				</Paper>

				<Paper elevation={0} sx={{ p: 2.5, borderRadius: 2.5, border: '1px solid #e8edf5', bgcolor: '#fff', mb: 3 }}>
					<Stack direction="row" alignItems="center" gap={1} sx={{ mb: 2 }}>
						<Box sx={{ width: 26, height: 26, borderRadius: 1.4, bgcolor: '#eff6ff', color: '#1d4ed8', display: 'grid', placeItems: 'center' }}>
							🪪
						</Box>
						<Typography sx={{ fontSize: 13.5, fontWeight: 700, color: '#0f172a' }}>
							Personal Details
						</Typography>
					</Stack>

					<Grid container spacing={2}>
						{detailRows.map((row) => (
							<Grid item xs={12} sm={6} md={4} key={row.label}>
								<DetailField
									label={row.label}
									value={row.value}
									placeholder={row.placeholder}
									readOnly={row.readOnly}
									highlight={row.value === 'ACTIVE' || row.value === 'COMPLETED'}
								/>
							</Grid>
						))}
					</Grid>
				</Paper>

				<Grid container spacing={2}>
					<Grid item xs={12} md={6}>
						<Paper elevation={0} sx={{ p: 2.5, borderRadius: 2.5, border: '1px solid #e8edf5', bgcolor: '#fff' }}>
							<Stack direction="row" alignItems="center" gap={1} sx={{ mb: 2 }}>
								<Box sx={{ width: 26, height: 26, borderRadius: 1.4, bgcolor: '#eff6ff', color: '#1d4ed8', display: 'grid', placeItems: 'center' }}>
									🧾
								</Box>
								<Typography sx={{ fontSize: 13.5, fontWeight: 700, color: '#0f172a' }}>
									Profile Details
								</Typography>
							</Stack>
								<Stack gap={1.3}>
									{profileDetails.map((item) => (
										<Box key={item.label}>
											<Typography sx={{ fontSize: 10.5, fontWeight: 700, color: '#94a3b8', letterSpacing: 0.6, mb: 0.6 }}>
												{item.label}
											</Typography>
											<Box
												component="input"
												defaultValue={item.value}
												placeholder={item.placeholder}
												sx={{
													width: '100%',
													height: 34,
													px: 1.2,
													borderRadius: 1.4,
													border: '1px solid #eef2f7',
													bgcolor: '#f8fafc',
													fontSize: 12,
													color: '#0f172a',
													outline: 'none',
												}}
											/>
										</Box>
									))}
								</Stack>
						</Paper>
					</Grid>

					<Grid item xs={12} md={6}>
						<Paper elevation={0} sx={{ p: 2.5, borderRadius: 2.5, border: '1px solid #e8edf5', bgcolor: '#fff' }}>
							<Stack direction="row" alignItems="center" gap={1} sx={{ mb: 2 }}>
								<Box sx={{ width: 26, height: 26, borderRadius: 1.4, bgcolor: '#eff6ff', color: '#1d4ed8', display: 'grid', placeItems: 'center' }}>
									🧠
								</Box>
								<Typography sx={{ fontSize: 13.5, fontWeight: 700, color: '#0f172a' }}>
									Skills
								</Typography>
							</Stack>
							<Stack gap={1.2}>
								{skillItems.map((item) => (
									<Paper
										key={item.label}
										elevation={0}
										sx={{
											px: 1.4,
											py: 0.9,
											borderRadius: 1.6,
											border: '1px solid #e8edf5',
											bgcolor: '#f8fafc',
											display: 'flex',
											alignItems: 'center',
											gap: 1.2,
										}}
									>
										<Checkbox
											checked={item.active}
											size="small"
											sx={{
												color: '#cbd5e1',
												'&.Mui-checked': { color: '#1d4ed8' },
												p: 0.4,
											}}
										/>
										<Typography sx={{ fontSize: 12.5, fontWeight: 600, color: '#0f172a' }}>
											{item.label}
										</Typography>
									</Paper>
								))}
							</Stack>
						</Paper>
					</Grid>
				</Grid>

				<Paper elevation={0} sx={{ p: 2.5, borderRadius: 2.5, border: '1px solid #e8edf5', bgcolor: '#fff', mt: 3 }}>
					<Stack direction="row" alignItems="center" justifyContent="space-between" sx={{ mb: 2 }}>
						<Stack direction="row" alignItems="center" gap={1}>
							<Box sx={{ width: 26, height: 26, borderRadius: 1.4, bgcolor: '#eff6ff', color: '#1d4ed8', display: 'grid', placeItems: 'center' }}>
								🧾
							</Box>
							<Typography sx={{ fontSize: 13.5, fontWeight: 700, color: '#0f172a' }}>
								Student Invoices
							</Typography>
						</Stack>
						<Typography sx={{ fontSize: 12.5, color: '#2563eb', fontWeight: 600, cursor: 'pointer' }}>
							View All History →
						</Typography>
					</Stack>

					<TableContainer>
						<Table>
							<TableHead>
								<TableRow sx={{ borderBottom: '1px solid #eef2f7', bgcolor: '#f8fafc' }}>
									<TableCell sx={{ fontSize: 10.5, fontWeight: 700, color: '#94a3b8', textTransform: 'uppercase' }}>
										Amount
									</TableCell>
									<TableCell sx={{ fontSize: 10.5, fontWeight: 700, color: '#94a3b8', textTransform: 'uppercase' }}>
										Description
									</TableCell>
									<TableCell sx={{ fontSize: 10.5, fontWeight: 700, color: '#94a3b8', textTransform: 'uppercase' }}>
										Transaction ID
									</TableCell>
									<TableCell sx={{ fontSize: 10.5, fontWeight: 700, color: '#94a3b8', textTransform: 'uppercase' }}>
										Status
									</TableCell>
								</TableRow>
							</TableHead>
							<TableBody>
								{invoiceRows.map((row) => (
									<TableRow key={row.transactionId} sx={{ borderBottom: '1px solid #f1f5f9' }}>
										<TableCell sx={{ fontSize: 12.5, fontWeight: 700, color: '#0f172a' }}>
											{row.amount}
										</TableCell>
										<TableCell sx={{ fontSize: 12.5, color: '#334155' }}>
											{row.description}
										</TableCell>
										<TableCell sx={{ fontSize: 12.5, color: '#94a3b8' }}>
											{row.transactionId}
										</TableCell>
										<TableCell>
											<Box
												sx={{
													display: 'inline-flex',
													alignItems: 'center',
													px: 1.2,
													py: 0.4,
													borderRadius: 999,
													bgcolor: '#dcfce7',
													color: '#16a34a',
													fontSize: 11,
													fontWeight: 700,
												}}
											>
												{row.status.toUpperCase()}
											</Box>
										</TableCell>
									</TableRow>
								))}
							</TableBody>
						</Table>
					</TableContainer>
				</Paper>
			</Box>
		</AdminLayout>
	)
}
