import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs))
}

export function calculateRemainingDays(expiryDate: string | null | undefined): number | null {
    if (!expiryDate) return null

    const today = new Date()
    today.setHours(0, 0, 0, 0)

    const expiry = new Date(expiryDate)
    expiry.setHours(0, 0, 0, 0)

    const diffTime = expiry.getTime() - today.getTime()
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

    return diffDays
}

export function formatBytes(bytes: number, decimals = 2): string {
    if (bytes === 0) return '0 Bytes'

    const k = 1024
    const dm = decimals < 0 ? 0 : decimals
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))

    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i]
}

export function formatDate(dateString: string | number): string {
    const date = typeof dateString === 'string' ? new Date(dateString) : new Date(dateString)
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
    })
}

export function formatExpiryWithDays(expiryTimestamp: number): { text: string; isExpired: boolean; daysLeft: number } {
    const now = new Date()
    const expiry = new Date(expiryTimestamp)

    const diffTime = expiry.getTime() - now.getTime()
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

    if (diffDays < 0) {
        return {
            text: `Expired ${Math.abs(diffDays)} days ago`,
            isExpired: true,
            daysLeft: diffDays,
        }
    } else if (diffDays === 0) {
        return {
            text: 'Expires today',
            isExpired: false,
            daysLeft: 0,
        }
    } else if (diffDays === 1) {
        return {
            text: '1 day left',
            isExpired: false,
            daysLeft: 1,
        }
    } else {
        return {
            text: `${diffDays} days left`,
            isExpired: false,
            daysLeft: diffDays,
        }
    }
}

export function formatDateTime(dateString: string | number): string {
    const date = typeof dateString === 'string' ? new Date(dateString) : new Date(dateString * 1000)
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
    })
}
