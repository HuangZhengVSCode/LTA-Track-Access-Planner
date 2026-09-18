import { copyFile, mkdir } from 'node:fs/promises'
import { dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const scriptDirectory = dirname(fileURLToPath(import.meta.url))
const frontendDirectory = resolve(scriptDirectory, '..')
const source = resolve(frontendDirectory, '..', 'scheduler.py')
const destinationDirectory = resolve(frontendDirectory, 'public')
const destination = resolve(destinationDirectory, 'scheduler.py')

await mkdir(destinationDirectory, { recursive: true })
await copyFile(source, destination)
console.log('Prepared the Python scheduling engine for the browser build.')
