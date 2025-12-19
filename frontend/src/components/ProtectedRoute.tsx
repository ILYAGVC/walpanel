import { useEffect, useState } from 'react'
import { Navigate } from 'react-router-dom'
import { isTokenValid, getUserRole } from '@/lib/auth'

interface ProtectedRouteProps {
    children: React.ReactNode
    allowedRoles?: ('admin' | 'superadmin')[]
}

export function ProtectedRoute({ children, allowedRoles }: ProtectedRouteProps) {
    const [isValid, setIsValid] = useState<boolean | null>(null)
    const [hasAccess, setHasAccess] = useState<boolean>(true)

    useEffect(() => {
        const checkToken = async () => {
            const valid = isTokenValid()
            setIsValid(valid)

            if (valid && allowedRoles && allowedRoles.length > 0) {
                const userRole = getUserRole()
                setHasAccess(userRole !== null && allowedRoles.includes(userRole))
            }
        }

        checkToken()
    }, [allowedRoles])

    if (isValid === null) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
            </div>
        )
    }

    if (!isValid) {
        return <Navigate to="/login" replace />
    }

    if (!hasAccess) {
        return <Navigate to="/" replace />
    }

    return <>{children}</>
}
