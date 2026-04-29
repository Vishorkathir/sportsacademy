import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import {
    Box,
    Button,
    Checkbox,
    Container,
    FormControlLabel,
    Link,
    Paper,
    Typography,
} from '@mui/material'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

function InputRow({ icon, placeholder, type = 'text', value, onChange }) {
    return (
        <Box
            sx={{
                height: 42,
                display: 'flex',
                alignItems: 'center',
                bgcolor: '#f1f4f8',
                borderRadius: '2px',
                border: '1px solid #eef1f5',
                px: 1.5,
                gap: 1,
            }}
        >
            <Box sx={{ width: 18, textAlign: 'center', color: '#8f96a3', fontSize: 13, lineHeight: 1 }}>
                {icon}
            </Box>
            <Box
                component="input"
                type={type}
                placeholder={placeholder}
                value={value}
                onChange={onChange}
                sx={{
                    border: 'none',
                    outline: 'none',
                    bgcolor: 'transparent',
                    width: '100%',
                    fontSize: 13,
                    color: '#8b93a3',
                    '&::placeholder': { color: '#b8bec8', opacity: 1 },
                }}
            />
        </Box>
    )
}

export default function Home() {
    const navigate = useNavigate()
    const [userId, setUserId] = useState('SA001')
    const [password, setPassword] = useState('')
    const [remember, setRemember] = useState(false)
    const [loading, setLoading] = useState(false)
    const [errorMessage, setErrorMessage] = useState('')
    const [successMessage, setSuccessMessage] = useState('')

    const handleSubmit = async (event) => {
        event.preventDefault()
        setLoading(true)
        setErrorMessage('')
        setSuccessMessage('')

        try {
            const response = await fetch(`${API_BASE_URL}/auth/admin/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email: 'admin@kings11sportsacademy.com',
                    password,
                }),
            })

            const data = await response.json()

            if (!response.ok) {
                throw new Error(data?.detail || 'Unable to sign in')
            }

            localStorage.setItem('kings11_admin_token', data.access_token)
            setSuccessMessage(`Signed in successfully as ${data.email}`)
            // navigate to dashboard on successful login
            navigate('/dashboard')
        } catch (error) {
            setErrorMessage(error.message || 'Login failed')
        } finally {
            setLoading(false)
        }
    }

    return (
        <Box
            sx={{
                minHeight: '100vh',
                bgcolor: '#f3f6fb',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                px: 2,
                py: 4,
            }}
        >
            <Container maxWidth={false} sx={{ maxWidth: 1230, width: '100%' }}>
                <Paper
                    elevation={0}
                    sx={{
                        borderRadius: '18px',
                        minHeight: 400,
                        bgcolor: '#fff',
                        boxShadow: '0 16px 40px rgba(66, 91, 118, 0.12)',
                        overflow: 'hidden',
                    }}
                >
                    <Box
                        sx={{
                            display: 'grid',
                            gridTemplateColumns: { xs: '1fr', md: '1.05fr 0.95fr' },
                            minHeight: 400,
                        }}
                    >
                        <Box
                            sx={{
                                position: 'relative',
                                minHeight: { xs: 300, md: 400 },
                                bgcolor: '#0b5aa0',
                                backgroundImage:
                                    'linear-gradient(180deg, rgba(6,48,98,0.18), rgba(6,48,98,0.42)), url(https://images.unsplash.com/photo-1518091043644-c1d4457512c6?auto=format&fit=crop&w=1200&q=80)',
                                backgroundSize: 'cover',
                                backgroundPosition: 'center bottom',
                                display: 'flex',
                                alignItems: 'flex-end',
                                color: 'white',
                            }}
                        >
                            <Box
                                sx={{
                                    position: 'absolute',
                                    inset: 0,
                                    background:
                                        'linear-gradient(180deg, rgba(10,74,135,0.82) 0%, rgba(10,74,135,0.75) 55%, rgba(10,74,135,0.92) 100%)',
                                }}
                            />
                            <Box
                                sx={{
                                    position: 'relative',
                                    zIndex: 1,
                                    width: '100%',
                                    p: { xs: 3, md: 4.3 },
                                    display: 'flex',
                                    flexDirection: 'column',
                                    justifyContent: 'space-between',
                                    minHeight: { xs: 300, md: 400 },
                                }}
                            >
                                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.2, mb: 10 }}>
                                    <Box
                                        sx={{
                                            width: 34,
                                            height: 34,
                                            borderRadius: '7px',
                                            bgcolor: 'rgba(9,15,21,0.72)',
                                            border: '1px solid rgba(255,255,255,0.08)',
                                            display: 'grid',
                                            placeItems: 'center',
                                            boxShadow: '0 4px 10px rgba(0,0,0,0.24)',
                                            fontSize: 18,
                                        }}
                                    >
                                        🏆
                                    </Box>
                                    <Typography sx={{ fontSize: 12.2, fontWeight: 700, letterSpacing: 0.1 }}>
                                        Kings11SportsAcademy
                                    </Typography>
                                </Box>

                                <Box sx={{ maxWidth: 490 }}>
                                    <Typography sx={{ fontSize: 14.5, fontWeight: 500, mb: 1.1, color: 'rgba(255,255,255,0.95)' }}>
                                        The Pursuit of Excellence Starts Here.
                                    </Typography>
                                    <Typography sx={{ fontSize: 13.3, lineHeight: 1.65, color: 'rgba(255,255,255,0.9)', maxWidth: 320 }}>
                                        Access your personalized training dashboard, match statistics, and academy resources.
                                    </Typography>

                                    <Box
                                        sx={{
                                            mt: 3.6,
                                            display: 'grid',
                                            gridTemplateColumns: 'repeat(3, 1fr)',
                                            gap: 0,
                                            maxWidth: 290,
                                            borderTop: '1px solid rgba(255,255,255,0.18)',
                                            borderBottom: '1px solid rgba(255,255,255,0.18)',
                                        }}
                                    >
                                        {[
                                            ['50+', 'STUDENTS'],
                                            ['10', 'PRO COACHES'],
                                            ['24/7', 'FACILITY ACCESS'],
                                        ].map(([value, label], index) => (
                                            <Box
                                                key={label}
                                                sx={{
                                                    py: 1.25,
                                                    px: 1.1,
                                                    borderRight: index < 2 ? '1px solid rgba(255,255,255,0.16)' : 'none',
                                                }}
                                            >
                                                <Typography sx={{ fontSize: 12.5, color: '#f6b21a', fontWeight: 700, lineHeight: 1.1 }}>
                                                    {value}
                                                </Typography>
                                                <Typography sx={{ fontSize: 11, color: 'rgba(255,255,255,0.85)', letterSpacing: 0.4, mt: 0.5 }}>
                                                    {label}
                                                </Typography>
                                            </Box>
                                        ))}
                                    </Box>
                                </Box>
                            </Box>
                        </Box>

                        <Box
                            sx={{
                                px: { xs: 3, md: 5.8 },
                                py: { xs: 4, md: 5 },
                                display: 'flex',
                                flexDirection: 'column',
                                justifyContent: 'center',
                                bgcolor: '#fff',
                            }}
                        >
                            <Box sx={{ maxWidth: 320, width: '100%', mx: 'auto' }}>
                                <form onSubmit={handleSubmit}>
                                    <Typography sx={{ fontSize: 16, fontWeight: 400, color: '#1d2733', mb: 0.8 }}>
                                        Welcome Back
                                    </Typography>
                                    <Typography sx={{ fontSize: 12.5, lineHeight: 1.55, color: '#6f7683', mb: 4.2 }}>
                                        Please enter your credentials to access the academy portal.
                                    </Typography>

                                    <Typography sx={{ fontSize: 11.2, letterSpacing: 0.35, color: '#969cab', mb: 1 }}>
                                        USER-ID
                                    </Typography>
                                    <InputRow
                                        icon="✉"
                                        placeholder="SA001"
                                        value={userId}
                                        onChange={(event) => setUserId(event.target.value)}
                                    />

                                    <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mt: 3.2, mb: 1 }}>
                                        <Typography sx={{ fontSize: 11.2, letterSpacing: 0.35, color: '#969cab' }}>
                                            PASSWORD
                                        </Typography>
                                        <Link href="#" underline="none" sx={{ fontSize: 11.5, color: '#2c5fd6', fontWeight: 500 }}>
                                            Forgot?
                                        </Link>
                                    </Box>
                                    <InputRow
                                        icon="🔒"
                                        placeholder="••••••••"
                                        type="password"
                                        value={password}
                                        onChange={(event) => setPassword(event.target.value)}
                                    />

                                    <FormControlLabel
                                        sx={{ mt: 1.6, ml: -0.5 }}
                                        control={
                                            <Checkbox
                                                size="small"
                                                checked={remember}
                                                onChange={(event) => setRemember(event.target.checked)}
                                                sx={{ color: '#c5cad4', p: 0.8, mr: 0.6 }}
                                            />
                                        }
                                        label={
                                            <Typography sx={{ fontSize: 11.8, color: '#67707f' }}>
                                                Keep me logged in on this device
                                            </Typography>
                                        }
                                    />

                                    {errorMessage ? (
                                        <Typography sx={{ mt: 1.2, fontSize: 12, color: '#c2410c' }}>
                                            {errorMessage}
                                        </Typography>
                                    ) : null}

                                    {successMessage ? (
                                        <Typography sx={{ mt: 1.2, fontSize: 12, color: '#15803d' }}>
                                            {successMessage}
                                        </Typography>
                                    ) : null}

                                    <Button
                                        fullWidth
                                        type="submit"
                                        variant="contained"
                                        disabled={loading}
                                        sx={{
                                            mt: 1.3,
                                            height: 37,
                                            borderRadius: '4px',
                                            textTransform: 'none',
                                            fontSize: 12.8,
                                            fontWeight: 500,
                                            color: '#7b4e00',
                                            bgcolor: '#f9b90e',
                                            boxShadow: 'none',
                                            '&:hover': { bgcolor: '#f1b000', boxShadow: 'none' },
                                        }}
                                    >
                                        {loading ? 'Signing In...' : 'Sign In to Dashboard →'}
                                    </Button>

                                    <Box sx={{ display: 'flex', alignItems: 'center', mt: 4.8, mb: 2.7 }}>
                                        <Box sx={{ flex: 1, height: 1, bgcolor: '#edf0f4' }} />
                                    </Box>

                                    <Typography sx={{ textAlign: 'center', fontSize: 12.4, color: '#6f7683', mb: 2.2 }}>
                                        Not an academy member yet?
                                    </Typography>

                                    <Button
                                        fullWidth
                                        variant="outlined"
                                        sx={{
                                            height: 36,
                                            borderRadius: '4px',
                                            textTransform: 'none',
                                            fontSize: 12.5,
                                            fontWeight: 500,
                                            color: '#2f64d4',
                                            borderColor: '#d8e2f4',
                                            bgcolor: '#fff',
                                            '&:hover': {
                                                borderColor: '#bfcfeb',
                                                bgcolor: '#fbfcff',
                                            },
                                        }}
                                    >
                                        Inquire about Registration
                                    </Button>
                                </form>
                            </Box>
                        </Box>
                    </Box>
                </Paper>

                <Box sx={{ textAlign: 'center', mt: 4.5, color: '#8d96a4' }}>
                    <Typography sx={{ fontSize: 11.8, mb: 0.9 }}>
                        © 2024 Kings11SportsAcademy. All rights reserved.
                    </Typography>
                    <Box sx={{ display: 'flex', justifyContent: 'center', gap: 3, fontSize: 11.7 }}>
                        <Link href="#" underline="none" sx={{ color: '#8d96a4' }}>
                            Privacy Policy
                        </Link>
                        <Link href="#" underline="none" sx={{ color: '#8d96a4' }}>
                            Technical Support
                        </Link>
                    </Box>
                </Box>
            </Container>
        </Box>
    )
}
