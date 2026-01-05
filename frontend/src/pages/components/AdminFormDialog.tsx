import { useEffect, useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { adminSchema, AdminFormData, AdminOutput } from '@/types'
import { adminAPI, dashboardAPI } from '@/lib/api'
import { bytesToGB } from '@/lib/traffic-converter'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from '@/components/ui/select'
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
} from '@/components/ui/dialog'
import { AlertCircle, Loader2 } from 'lucide-react'

interface AdminFormDialogProps {
    isOpen: boolean
    onClose: () => void
    onSuccess: () => void
    admin?: AdminOutput | null
}

export function AdminFormDialog({
    isOpen,
    onClose,
    onSuccess,
    admin,
}: AdminFormDialogProps) {
    const [serverError, setServerError] = useState<string | null>(null)
    const [panels, setPanels] = useState<{ name: string; panel_type: string }[]>([])
    const [loadingPanels, setLoadingPanels] = useState(false)

    const {
        register,
        handleSubmit,
        formState: { errors, isSubmitting },
        reset,
        setValue,
        watch,
    } = useForm<AdminFormData>({
        resolver: zodResolver(adminSchema),
        defaultValues: {
            username: '',
            password: '',
            panel: '',
            inbound_id: null,
            traffic: 0,
            return_traffic: false,
            is_active: true,
            expiry_date: null,
        },
    })

    useEffect(() => {
        if (isOpen) {
            loadPanels()
        }
    }, [isOpen])

    useEffect(() => {
        if (admin) {
            setValue('username', admin.username)
            setValue('password', '') // Don't pre-fill password
            setValue('panel', admin.panel)
            setValue('inbound_id', admin.inbound_id)
            setValue('traffic', bytesToGB(admin.traffic))
            setValue('return_traffic', admin.return_traffic)
            setValue('is_active', admin.is_active)
            setValue('expiry_date', admin.expiry_date)
        } else {
            reset()
        }
    }, [admin, isOpen, setValue, reset])

    const loadPanels = async () => {
        try {
            setLoadingPanels(true)
            const data = await dashboardAPI.getDashboardData()
            if (data.panels) {
                setPanels(data.panels.map((p) => ({ name: p.name, panel_type: p.panel_type })))
            }
        } catch (err) {
            console.error('Failed to load panels:', err)
        } finally {
            setLoadingPanels(false)
        }
    }

    const onSubmit = async (data: AdminFormData) => {
        setServerError(null)

        try {
            if (admin?.id) {
                // Update
                await adminAPI.updateAdmin(admin.id, data)
            } else {
                // Create
                await adminAPI.createAdmin(data)
            }

            onSuccess()
        } catch (error: any) {
            console.error('Form submission error:', error)
            setServerError(error?.message || 'Operation failed')
        }
    }

    return (
        <Dialog open={isOpen} onOpenChange={onClose}>
            <DialogContent className="max-h-[90vh] overflow-y-auto">
                <DialogHeader>
                    <DialogTitle>{admin ? 'Edit Admin' : 'Create New Admin'}</DialogTitle>
                    <DialogDescription>
                        {admin ? 'Update admin information' : 'Add a new admin account'}
                    </DialogDescription>
                </DialogHeader>

                <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
                    {serverError && (
                        <div className="flex items-gap-2 rounded-md bg-destructive/10 p-3 text-sm text-destructive border border-destructive/20">
                            <AlertCircle className="h-4 w-4 mr-2 flex-shrink-0 mt-0.5" />
                            <p>{serverError}</p>
                        </div>
                    )}

                    {/* Username */}
                    <div className="space-y-2">
                        <Label htmlFor="username">Username *</Label>
                        <Input
                            id="username"
                            placeholder="admin_name"
                            disabled={isSubmitting || !!admin}
                            {...register('username')}
                        />
                        {errors.username && (
                            <p className="text-sm text-destructive">{errors.username.message}</p>
                        )}
                    </div>

                    {/* Password */}
                    <div className="space-y-2">
                        <Label htmlFor="password">Password *</Label>
                        <Input
                            id="password"
                            type="password"
                            placeholder={admin ? 'Leave empty to keep current' : 'Enter password'}
                            disabled={isSubmitting}
                            {...register('password')}
                        />
                        {errors.password && (
                            <p className="text-sm text-destructive">{errors.password.message}</p>
                        )}
                    </div>

                    {/* Panel Selection */}
                    <div className="space-y-2">
                        <Label htmlFor="panel">Panel *</Label>
                        <Select
                            value={watch('panel')}
                            onValueChange={(value) => setValue('panel', value)}
                            disabled={isSubmitting || loadingPanels}
                        >
                            <SelectTrigger>
                                <SelectValue placeholder="Select a panel" />
                            </SelectTrigger>
                            <SelectContent>
                                {panels.map((panel) => (
                                    <SelectItem key={panel.name} value={panel.name}>
                                        {panel.name}
                                    </SelectItem>
                                ))}
                            </SelectContent>
                        </Select>
                        {errors.panel && (
                            <p className="text-sm text-destructive">{errors.panel.message}</p>
                        )}
                    </div>

                    {/* Inbound ID - Only for 3x-ui panels */}
                    {watch('panel') && panels.find(p => p.name === watch('panel'))?.panel_type === '3x-ui' && (
                        <div className="space-y-2">
                            <Label htmlFor="inbound_id">Inbound ID</Label>
                            <Input
                                id="inbound_id"
                                type="number"
                                placeholder="Optional"
                                disabled={isSubmitting}
                                {...register('inbound_id', { valueAsNumber: true })}
                            />
                            {errors.inbound_id && (
                                <p className="text-sm text-destructive">{errors.inbound_id.message}</p>
                            )}
                        </div>
                    )}

                    {/* Traffic */}
                    <div className="space-y-2">
                        <Label htmlFor="traffic">Traffic (GB)</Label>
                        <Input
                            id="traffic"
                            type="number"
                            step="0.1"
                            min="0"
                            placeholder="0"
                            disabled={isSubmitting}
                            {...register('traffic', { valueAsNumber: true })}
                        />
                        {errors.traffic && (
                            <p className="text-sm text-destructive">{errors.traffic.message}</p>
                        )}
                    </div>

                    {/* Expiry Date */}
                    <div className="space-y-2">
                        <Label htmlFor="expiry_date">Expiry Date</Label>
                        <Input
                            id="expiry_date"
                            type="date"
                            disabled={isSubmitting}
                            {...register('expiry_date')}
                        />
                        {errors.expiry_date && (
                            <p className="text-sm text-destructive">{errors.expiry_date.message}</p>
                        )}
                    </div>

                    {/* Checkboxes */}
                    <div className="space-y-3">
                        <label className="flex items-center gap-2 cursor-pointer">
                            <input
                                type="checkbox"
                                disabled={isSubmitting}
                                {...register('return_traffic')}
                                className="rounded border border-input"
                            />
                            <span className="text-sm">Return Traffic</span>
                        </label>

                        <label className="flex items-center gap-2 cursor-pointer">
                            <input
                                type="checkbox"
                                disabled={isSubmitting}
                                defaultChecked
                                {...register('is_active')}
                                className="rounded border border-input"
                            />
                            <span className="text-sm">Active</span>
                        </label>
                    </div>
                </form>

                <DialogFooter className="gap-2 sm:gap-0">
                    <Button variant="outline" onClick={onClose} disabled={isSubmitting}>
                        Cancel
                    </Button>
                    <Button onClick={handleSubmit(onSubmit)} disabled={isSubmitting}>
                        {isSubmitting && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                        {isSubmitting ? 'Saving...' : admin ? 'Update Admin' : 'Create Admin'}
                    </Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    )
}
