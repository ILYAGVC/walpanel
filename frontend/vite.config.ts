import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'
import fs from 'fs'

// Read URLPATH from root .env file
function getRootEnvUrlPath(): string {
    const rootEnvPath = path.resolve(__dirname, '../.env')
    try {
        const envContent = fs.readFileSync(rootEnvPath, 'utf-8')
        const match = envContent.match(/^URLPATH=(.*)$/m)
        return match ? match[1].trim() : 'dashboard'
    } catch {
        return 'dashboard'
    }
}

const urlPath = getRootEnvUrlPath()

export default defineConfig({
    plugins: [react()],
    base: `/${urlPath}/`,
    resolve: {
        alias: {
            '@': path.resolve(__dirname, './src'),
        },
    },
    server: {
        port: 5173,
        open: true,
    },
    define: {
        'import.meta.env.VITE_URL_PREFIX': JSON.stringify(urlPath),
    },
})
