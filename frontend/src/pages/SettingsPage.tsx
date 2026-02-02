import { useEffect, useState } from 'react'
import {
    Download,
    Upload,
    FileText,
} from 'lucide-react'
import { superadminAPI } from '@/lib/api'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

export function SettingsPage() {
    const [logs, setLogs] = useState<string[]>([])
    const [logsLoading, setLogsLoading] = useState(false)
    const [backupLoading, setBackupLoading] = useState(false)
    const [restoreLoading, setRestoreLoading] = useState(false)

    useEffect(() => {
        fetchLogs()
    }, [])

    const fetchLogs = async () => {
        try {
            setLogsLoading(true)
            const logsData = await superadminAPI.getLogs()
            setLogs(logsData)
        } catch (err: any) {
            console.error('Failed to fetch logs:', err)
            alert(err?.message || 'Failed to fetch logs')
        } finally {
            setLogsLoading(false)
        }
    }

    const handleDownloadBackup = async () => {
        try {
            setBackupLoading(true)
            const blob = await superadminAPI.downloadBackup()
            const url = window.URL.createObjectURL(blob)
            const a = document.createElement('a')
            a.href = url
            a.download = `backup-${new Date().toISOString().split('T')[0]}.db`
            document.body.appendChild(a)
            a.click()
            window.URL.revokeObjectURL(url)
            document.body.removeChild(a)
        } catch (err: any) {
            console.error('Failed to download backup:', err)
            alert(err?.message || 'Failed to download backup')
        } finally {
            setBackupLoading(false)
        }
    }

    const handleRestoreBackup = async (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0]
        if (!file) return

        try {
            setRestoreLoading(true)
            const message = await superadminAPI.restoreBackup(file)
            alert(message)
        } catch (err: any) {
            console.error('Failed to restore backup:', err)
            alert(err?.message || 'Failed to restore backup')
        } finally {
            setRestoreLoading(false)
            event.target.value = ''
        }
    }

    return (
        <div className="space-y-6 p-4 md:p-6 max-w-full overflow-x-hidden">
            <div>
                <h1 className="text-2xl md:text-3xl font-bold tracking-tight">Settings</h1>
                <p className="text-muted-foreground">Manage database backups, restores, and view application logs.</p>
            </div>

            <div className="grid gap-6 md:grid-cols-2">
                <Card>
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <Download className="h-5 w-5" />
                            Database Backup
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <p className="text-sm text-muted-foreground mb-4">
                            Download a backup of the current database.
                        </p>
                        <Button
                            onClick={handleDownloadBackup}
                            disabled={backupLoading}
                            className="w-full"
                        >
                            {backupLoading ? 'Downloading...' : 'Download Backup'}
                        </Button>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <Upload className="h-5 w-5" />
                            Database Restore
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <p className="text-sm text-muted-foreground mb-4">
                            Restore database from a backup file.
                        </p>
                        <div className="space-y-2">
                            <Button
                                onClick={() => document.getElementById('restore-file-input')?.click()}
                                disabled={restoreLoading}
                                className="w-full bg-orange-500 hover:bg-orange-600 text-white"
                            >
                                {restoreLoading ? 'Restoring...' : 'Select Backup File'}
                            </Button>
                            <Input
                                id="restore-file-input"
                                type="file"
                                accept=".db"
                                onChange={handleRestoreBackup}
                                disabled={restoreLoading}
                                className="hidden"
                            />
                            {restoreLoading && (
                                <p className="text-sm text-muted-foreground">Restoring...</p>
                            )}
                        </div>
                    </CardContent>
                </Card>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <FileText className="h-5 w-5" />
                        Application Logs
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="space-y-2">
                        <Button
                            onClick={fetchLogs}
                            disabled={logsLoading}
                            variant="outline"
                            size="sm"
                        >
                            {logsLoading ? 'Loading...' : 'Refresh Logs'}
                        </Button>
                        <div className="bg-muted p-4 rounded-md max-h-64 overflow-y-auto">
                            {logs.length > 0 ? (
                                <pre className="text-xs whitespace-pre-wrap">
                                    {logs.join('\n')}
                                </pre>
                            ) : (
                                <p className="text-sm text-muted-foreground">No logs available</p>
                            )}
                        </div>
                    </div>
                </CardContent>
            </Card>
        </div>
    )
}