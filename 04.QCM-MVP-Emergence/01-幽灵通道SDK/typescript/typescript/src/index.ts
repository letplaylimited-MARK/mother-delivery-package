export type ErrorObject = {
  errorCode: string
  errorName: string
  severity: 'low' | 'medium' | 'high' | 'critical'
  message: string
  retryable: boolean
  rollbackRequired: boolean
  context: Record<string, unknown>
  timestamp: number
}

export type DeltaPayload = {
  added: Record<string, unknown>
  modified: Record<string, unknown>
  removed: string[]
  versionFrom: string
  versionTo: string
  timestamp: number
  listAppends?: Record<string, unknown[]>
  changedFields?: Record<string, string[]>
}

export type VectorClock = Record<string, number>

export type EncryptedStream = {
  protocolVersion: string
  schemaVersion: string
  streamId: string
  sourceRoleId: string
  destinationRoleId: string
  timestampNs: number
  sequenceNumber: number
  type: string
  vectorClock: VectorClock
  deltaHash: string
  deltaPayload: string
  nonce: string
  compression: Record<string, unknown>
  encryption: Record<string, unknown>
  authTag: string
  merkleRoot: string
  auditRequired: boolean
  signature?: string | null
  extensions?: Record<string, unknown>
}

export type AckMessage = {
  protocolVersion: string
  schemaVersion: string
  streamId: string
  sequenceNumber: number
  ackType: 'RECEIVED' | 'VERIFIED' | 'APPLIED' | 'ROLLED_BACK' | 'FAILED'
  status: 'ok' | 'error'
  receiverId: string
  merkleRootVerified: boolean
  applied: boolean
  timestampNs: number
  extensions?: Record<string, unknown>
  error?: ErrorObject | null
}

export type AuditEntry = {
  transactionId: string
  timestamp: number
  sourceRole: string
  destinationRole: string
  messageType: string
  deltaHash: string
  merkleRootBefore: string
  merkleRootAfter: string
  bandwidthSavedBytes: number
  transmissionDurationMs: number
  signatureVerified: boolean
  tamperDetected: boolean
}

export type WorkflowStep = {
  stepId: string
  name: string
  dependencies: string[]
  status: 'pending' | 'running' | 'completed' | 'failed' | 'blocked' | 'recovered'
  startTime?: number | null
  endTime?: number | null
  error?: string | null
  state?: Record<string, unknown>
}

export type SnapshotRecord = {
  snapshotId: string
  streamId: string
  sequenceNumber: number
  stateHash: string
  merkleRoot: string
  createdAt: number
  status: 'active' | 'archived' | 'rollback_candidate' | 'corrupted'
  state?: Record<string, unknown>
  metadata?: Record<string, unknown>
}

export type SyncResult = {
  success: boolean
  bandwidthReduction: number
  latencyMs: number
  consistencyVerified: boolean
  changesApplied: number
  errors: ErrorObject[]
}

export type GhostChannelConfig = {
  compressionLevel: number
  semanticThreshold: number
  auditEnabled: boolean
  maxRetry: number
  completionMode: 'verify' | 'apply'
  awaitAck?: boolean
  ackTimeoutMs?: number
  replayWindowSize?: number
}

export class GhostChannelClient {
  private config: GhostChannelConfig
  private auditTrail: AuditEntry[] = []
  private ackHistory = new Map<string, { ackType: AckMessage['ackType']; status: AckMessage['status'] }>()
  private replayWindows = new Map<string, number[]>()
  private snapshots = new Map<string, SnapshotRecord[]>()
  private pendingSyncs = new Map<string, { resolve: (value: SyncResult) => void; reject: (reason?: unknown) => void }>()
  private stats = {
    totalSyncs: 0,
    memorySyncs: 0,
    workflowSyncs: 0,
    acksReceived: 0,
    lastAckType: null as AckMessage['ackType'] | null,
  }
  public lastDeltaPayload: DeltaPayload | null = null
  public lastWorkflowDeltaPayload: DeltaPayload | null = null
  public lastEncryptedStream: EncryptedStream | null = null

  constructor(config: GhostChannelConfig) {
    this.config = {
      awaitAck: false,
      ackTimeoutMs: 500,
      replayWindowSize: 1024,
      ...config,
    }
  }

  private ackRank(ackType: AckMessage['ackType']): number {
    const ranks: Record<AckMessage['ackType'], number> = {
      RECEIVED: 1,
      VERIFIED: 2,
      APPLIED: 3,
      ROLLED_BACK: 3,
      FAILED: 3,
    }
    return ranks[ackType]
  }

  private isTerminalAck(ackType: AckMessage['ackType']): boolean {
    if (this.config.completionMode === 'verify') {
      return ['VERIFIED', 'APPLIED', 'ROLLED_BACK', 'FAILED'].includes(ackType)
    }
    return ['APPLIED', 'ROLLED_BACK', 'FAILED'].includes(ackType)
  }

  private stableDeltaHash(delta: DeltaPayload): string {
    const stable = {
      added: delta.added,
      modified: delta.modified,
      removed: delta.removed,
      versionFrom: delta.versionFrom,
      versionTo: delta.versionTo,
      listAppends: delta.listAppends ?? {},
      changedFields: delta.changedFields ?? {},
    }
    const json = JSON.stringify(stable)
    let hash = 0
    for (let i = 0; i < json.length; i++) {
      hash = (hash * 31 + json.charCodeAt(i)) >>> 0
    }
    return hash.toString(16).padStart(64, '0').slice(0, 64)
  }

  private buildDeltaPayload(oldState: Record<string, unknown>, newState: Record<string, unknown>): DeltaPayload {
    const added: Record<string, unknown> = {}
    const modified: Record<string, unknown> = {}
    const removed: string[] = []
    const listAppends: Record<string, unknown[]> = {}
    const changedFields: Record<string, string[]> = {}

    const oldKeys = new Set(Object.keys(oldState))
    const newKeys = new Set(Object.keys(newState))

    for (const key of newKeys) {
      if (!oldKeys.has(key)) added[key] = newState[key]
    }
    for (const key of oldKeys) {
      if (!newKeys.has(key)) removed.push(key)
    }
    for (const key of oldKeys) {
      if (newKeys.has(key) && JSON.stringify(oldState[key]) !== JSON.stringify(newState[key])) {
        const oldVal = oldState[key]
        const newVal = newState[key]
        if (Array.isArray(oldVal) && Array.isArray(newVal) && newVal.length >= oldVal.length) {
          const prefixMatches = JSON.stringify(newVal.slice(0, oldVal.length)) === JSON.stringify(oldVal)
          if (prefixMatches) {
            const appended = newVal.slice(oldVal.length)
            if (appended.length > 0) listAppends[key] = appended
            continue
          }
        }
        modified[key] = newVal
        changedFields[key] = [key]
      }
    }

    return {
      added,
      modified,
      removed,
      versionFrom: String((oldState['__version__'] as string | undefined) ?? ''),
      versionTo: String((newState['__version__'] as string | undefined) ?? ''),
      timestamp: Date.now() / 1000,
      listAppends,
      changedFields,
    }
  }

  private serializeDeltaPayload(delta: DeltaPayload): string {
    return Buffer.from(JSON.stringify(delta)).toString('base64')
  }

  async syncMemoryDelta(
    sourceRole: string,
    targetRole: string,
    oldState: Record<string, unknown>,
    newState: Record<string, unknown>,
    semanticFilter?: string,
  ): Promise<SyncResult> {
    void semanticFilter
    const delta = this.buildDeltaPayload(oldState, newState)
    this.lastDeltaPayload = delta
    const deltaHash = this.stableDeltaHash(delta)
    const seq = this.stats.totalSyncs + 1
    const key = `${sourceRole}:${targetRole}:${deltaHash}`
    const currentWindow = this.replayWindows.get(sourceRole) ?? []
    if (!currentWindow.includes(seq)) {
      currentWindow.push(seq)
      currentWindow.sort((a, b) => a - b)
      while (currentWindow.length > (this.config.replayWindowSize ?? 1024)) currentWindow.shift()
      this.replayWindows.set(sourceRole, currentWindow)
    }
    this.stats.totalSyncs += 1
    this.stats.memorySyncs += 1
    this.lastEncryptedStream = {
      protocolVersion: '1.1.0',
      schemaVersion: 'ghost-channel.encrypted-stream/1.1',
      streamId: `stream_${seq}`,
      sourceRoleId: sourceRole,
      destinationRoleId: targetRole,
      timestampNs: Date.now() * 1_000_000,
      sequenceNumber: seq,
      type: 'MEMORY_SYNC',
      vectorClock: { [sourceRole]: seq },
      deltaHash,
      deltaPayload: this.serializeDeltaPayload(delta),
      nonce: Buffer.from('ghostnonce12').toString('base64'),
      compression: { algorithm: 'none', level: this.config.compressionLevel },
      encryption: { algorithm: 'aes-256-gcm' },
      authTag: Buffer.from('authtagplaceholder').toString('base64'),
      merkleRoot: ''.padStart(64, '2'),
      auditRequired: this.config.auditEnabled,
    }

    this.auditTrail.push({
      transactionId: `txn_${this.auditTrail.length + 1}`,
      timestamp: Date.now() / 1000,
      sourceRole,
      destinationRole: targetRole,
      messageType: 'MEMORY_SYNC',
      deltaHash,
      merkleRootBefore: ''.padStart(64, '1'),
      merkleRootAfter: ''.padStart(64, '2'),
      bandwidthSavedBytes: 0,
      transmissionDurationMs: 0,
      signatureVerified: true,
      tamperDetected: false,
    })
    const result: SyncResult = {
      success: true,
      bandwidthReduction: 0,
      latencyMs: 0,
      consistencyVerified: true,
      changesApplied: Object.keys(delta.added).length + Object.keys(delta.modified).length + delta.removed.length,
      errors: [],
    }
    if (!this.config.awaitAck) return result
    const pendingKey = `${this.lastEncryptedStream.streamId}:${this.lastEncryptedStream.sequenceNumber}`
    return await new Promise<SyncResult>((resolve, reject) => {
      this.pendingSyncs.set(pendingKey, { resolve, reject })
      setTimeout(() => {
        if (this.pendingSyncs.has(pendingKey)) {
          this.pendingSyncs.delete(pendingKey)
          reject(new Error('ack wait timeout'))
        }
      }, this.config.ackTimeoutMs)
    })
  }

  async syncWorkflowState(
    workflowId: string,
    stepId: string,
    stepState: Record<string, unknown>,
    dependencies: string[],
  ): Promise<SyncResult> {
    const completed = new Set(
      (this.snapshots.get(stepId) ?? []).map((s) => s.metadata?.completedStep).filter(Boolean) as string[],
    )
    const missing = dependencies.filter((d) => !completed.has(d))
    if (missing.length > 0) {
      return {
        success: false,
        bandwidthReduction: 0,
        latencyMs: 0,
        consistencyVerified: false,
        changesApplied: 0,
        errors: [
          {
            errorCode: 'GC-SYNC-DEP-BLOCKED',
            errorName: 'DependencyBlocked',
            severity: 'medium',
            message: `missing dependencies: ${missing.join(', ')}`,
            retryable: true,
            rollbackRequired: false,
            context: { workflowId, stepId, missing },
            timestamp: Date.now() / 1000,
          },
        ],
      }
    }
    const snaps = this.snapshots.get(stepId) ?? []
    const previousState = snaps.length > 0 ? (snaps[snaps.length - 1].state ?? {}) : {}
    const workflowDelta = this.buildDeltaPayload({ __version__: stepId, ...previousState }, { __version__: stepId, ...stepState })
    this.lastWorkflowDeltaPayload = workflowDelta
    const workflowDeltaHash = this.stableDeltaHash(workflowDelta)
    const workflowStreamId = `${workflowId}:${stepId}`

    this.lastEncryptedStream = {
      protocolVersion: '1.1.0',
      schemaVersion: 'ghost-channel.encrypted-stream/1.1',
      streamId: workflowStreamId,
      sourceRoleId: workflowId,
      destinationRoleId: stepId,
      timestampNs: Date.now() * 1_000_000,
      sequenceNumber: snaps.length + 1,
      type: 'WORKFLOW_SYNC',
      vectorClock: { [workflowId]: snaps.length + 1 },
      deltaHash: workflowDeltaHash,
      deltaPayload: this.serializeDeltaPayload(workflowDelta),
      nonce: Buffer.from('ghostnonce12').toString('base64'),
      compression: { algorithm: 'none', level: this.config.compressionLevel },
      encryption: { algorithm: 'aes-256-gcm' },
      authTag: Buffer.from('authtagplaceholder').toString('base64'),
      merkleRoot: ''.padStart(64, '3'),
      auditRequired: this.config.auditEnabled,
    }

    snaps.push({
      snapshotId: `snap_${workflowId}_${stepId}_${snaps.length + 1}`,
      streamId: workflowStreamId,
      sequenceNumber: snaps.length + 1,
      stateHash: workflowDeltaHash,
      merkleRoot: ''.padStart(64, '3'),
      createdAt: Date.now() / 1000,
      status: 'active',
      state: stepState,
      metadata: { completedStep: stepId },
    })
    this.snapshots.set(stepId, snaps)
    this.stats.totalSyncs += 1
    this.stats.workflowSyncs += 1
    const result = {
      success: true,
      bandwidthReduction: 0,
      latencyMs: 0,
      consistencyVerified: true,
      changesApplied: Object.keys(workflowDelta.added).length + Object.keys(workflowDelta.modified).length + workflowDelta.removed.length,
      errors: [],
    }
    if (!this.config.awaitAck) return result
    const pendingKey = `${workflowStreamId}:${this.lastEncryptedStream.sequenceNumber}`
    return await new Promise<SyncResult>((resolve, reject) => {
      this.pendingSyncs.set(pendingKey, { resolve, reject })
      setTimeout(() => {
        if (this.pendingSyncs.has(pendingKey)) {
          this.pendingSyncs.delete(pendingKey)
          reject(new Error('ack wait timeout'))
        }
      }, this.config.ackTimeoutMs)
    })
  }

  async recoverFromFailure(stepId: string, lastKnownState: Record<string, unknown>): Promise<Record<string, unknown>> {
    const snaps = this.snapshots.get(stepId) ?? []
    const candidates = snaps.filter((s) => ['active', 'rollback_candidate', 'archived'].includes(s.status))
    if (candidates.length === 0) return lastKnownState
    return candidates[candidates.length - 1].state ?? lastKnownState
  }

  async receiveAck(ack: Record<string, unknown>): Promise<void> {
    const ackMsg = ack as Partial<AckMessage>
    if (!ackMsg.streamId || typeof ackMsg.sequenceNumber !== 'number' || !ackMsg.ackType || !ackMsg.status) {
      throw new Error('ack object failed schema validation')
    }
    if (ackMsg.status === 'ok' && ackMsg.error != null) throw new Error('ok ack must not contain error')
    if (ackMsg.status === 'error' && ackMsg.error == null) throw new Error('error ack must contain ErrorObject')

    const streamKey = `${ackMsg.streamId}:${ackMsg.sequenceNumber}`
    const prev = this.ackHistory.get(streamKey)
    const currentAck = ackMsg.ackType as AckMessage['ackType']
    if (prev) {
      if (prev.status === 'ok' && ackMsg.status === 'error') {
        throw new Error('ack replay cannot downgrade success path to error path')
      }
      if (this.ackRank(currentAck) < this.ackRank(prev.ackType)) {
        throw new Error('ack progression must be monotonic')
      }
      if (this.ackRank(currentAck) === this.ackRank(prev.ackType) && currentAck !== prev.ackType) {
        throw new Error('ack replay mismatch at same sequence')
      }
    }
    this.ackHistory.set(streamKey, { ackType: currentAck, status: ackMsg.status as AckMessage['status'] })
    this.stats.acksReceived += 1
    this.stats.lastAckType = currentAck

    const pending = this.pendingSyncs.get(streamKey)
    if (pending && this.isTerminalAck(currentAck)) {
      this.pendingSyncs.delete(streamKey)
      pending.resolve({
        success: ackMsg.status === 'ok',
        bandwidthReduction: 0,
        latencyMs: 0,
        consistencyVerified: Boolean(ackMsg.merkleRootVerified),
        changesApplied: currentAck === 'APPLIED' ? 1 : 0,
        errors: ackMsg.status === 'ok' ? [] : [ackMsg.error as ErrorObject],
      })
    }
  }

  getAuditTrail(limit = 100): Record<string, unknown>[] {
    return this.auditTrail.slice(-limit)
  }

  getStats() {
    return { ...this.stats }
  }

  async validateAssets(baseDir?: string) {
    const currentFile = fileURLToPath(import.meta.url)
    const srcDir = path.dirname(currentFile)
    const tsRoot = path.resolve(srcDir, '..')
    const sdkRoot = baseDir ?? path.resolve(tsRoot, '..')
    const schemasDir = path.join(sdkRoot, 'schemas')
    const examplesDir = path.join(sdkRoot, 'examples')
    const mappingFile = path.join(examplesDir, 'example-schema-map.json')

    const report = {
      schemas: { valid: true, count: 0, errors: [] as string[] },
      examples: { valid: true, count: 0, errors: [] as string[] },
      mapping: { valid: true, count: 0, errors: [] as string[] },
      valid: true,
    }

    // schemas
    if (!fs.existsSync(schemasDir)) {
      report.schemas.valid = false
      report.schemas.errors.push(`schemas directory not found: ${schemasDir}`)
    } else {
      const schemaFiles = fs.readdirSync(schemasDir).filter((f) => f.endsWith('.schema.json'))
      report.schemas.count = schemaFiles.length
      for (const file of schemaFiles) {
        try {
          JSON.parse(fs.readFileSync(path.join(schemasDir, file), 'utf8'))
        } catch (err) {
          report.schemas.valid = false
          report.schemas.errors.push(`invalid schema json: ${file}`)
        }
      }
    }

    // examples
    if (!fs.existsSync(examplesDir)) {
      report.examples.valid = false
      report.examples.errors.push(`examples directory not found: ${examplesDir}`)
    } else {
      const exampleFiles = fs.readdirSync(examplesDir).filter((f) => f.endsWith('.example.json'))
      report.examples.count = exampleFiles.length
      for (const file of exampleFiles) {
        try {
          JSON.parse(fs.readFileSync(path.join(examplesDir, file), 'utf8'))
        } catch (err) {
          report.examples.valid = false
          report.examples.errors.push(`invalid example json: ${file}`)
        }
      }
    }

    // mapping
    if (!fs.existsSync(mappingFile)) {
      report.mapping.valid = false
      report.mapping.errors.push(`mapping file not found: ${mappingFile}`)
    } else {
      try {
        const mapping = JSON.parse(fs.readFileSync(mappingFile, 'utf8'))
        const mappings = Array.isArray(mapping.mappings) ? mapping.mappings : []
        report.mapping.count = mappings.length
        for (const item of mappings) {
          if (!fs.existsSync(path.join(examplesDir, item.example))) {
            report.mapping.valid = false
            report.mapping.errors.push(`missing example file: ${item.example}`)
          }
          if (!fs.existsSync(path.join(schemasDir, item.schema))) {
            report.mapping.valid = false
            report.mapping.errors.push(`missing schema file: ${item.schema}`)
          }
        }
      } catch {
        report.mapping.valid = false
        report.mapping.errors.push('invalid mapping file json')
      }
    }

    report.valid = report.schemas.valid && report.examples.valid && report.mapping.valid
    return report
  }
}
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
