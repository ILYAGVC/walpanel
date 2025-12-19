import Cookies from 'js-cookie'
import { jwtDecode } from 'jwt-decode'
import { DecodedToken } from '@/types'

const TOKEN_KEY = 'access_token'

export function getToken(): string | undefined {
    return Cookies.get(TOKEN_KEY)
}

export function setToken(token: string): void {
    Cookies.set(TOKEN_KEY, token, {
        httpOnly: false, // Note: httpOnly is not supported in browser cookies via JS
        secure: window.location.protocol === 'https:',
        sameSite: 'strict',
        expires: 7,
    })
}

export function removeToken(): void {
    Cookies.remove(TOKEN_KEY)
}

export function getDecodedToken(): DecodedToken | null {
    try {
        const token = getToken()
        if (!token) return null
        return jwtDecode<DecodedToken>(token)
    } catch (error) {
        console.error('Failed to decode token:', error)
        return null
    }
}

export function isTokenValid(): boolean {
    try {
        const decoded = getDecodedToken()
        if (!decoded || !decoded.exp) return false

        // Check if token is expired
        const now = Math.floor(Date.now() / 1000)
        return decoded.exp > now
    } catch {
        return false
    }
}

export function getUserRole(): 'admin' | 'superadmin' | null {
    const decoded = getDecodedToken()
    return decoded?.role || null
}

export function getUsername(): string | null {
    const decoded = getDecodedToken()
    return decoded?.sub || null
}

export function getPanel(): string | null {
    const decoded = getDecodedToken()
    return decoded?.panel || null
}

export function logout(): void {
    removeToken()
    window.location.href = import.meta.env.BASE_URL + 'login'
}
