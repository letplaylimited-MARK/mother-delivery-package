import test from 'node:test'
import assert from 'node:assert/strict'
import { GhostChannelClient } from '../src/index.ts'

test('client constructs', () => {
  const client = new GhostChannelClient({
    compressionLevel: 9,
    semanticThreshold: 0.7,
    auditEnabled: true,
    maxRetry: 3,
    completionMode: 'apply',
  })
  assert.ok(client)
})

test('syncMemoryDelta returns SyncResult shape', async () => {
  const client = new GhostChannelClient({
    compressionLevel: 9,
    semanticThreshold: 0.7,
    auditEnabled: true,
    maxRetry: 3,
    completionMode: 'apply',
  })

  const result = await client.syncMemoryDelta(
    'secretary_v1',
    'researcher_v1',
    { __version__: 'v1', x: 1 },
    { __version__: 'v2', x: 2 },
    'protocol scope',
  )

  assert.equal(result.success, true)
  assert.ok(typeof result.bandwidthReduction === 'number')
  assert.ok(typeof result.latencyMs === 'number')
  assert.ok(Array.isArray(result.errors))
})

test('syncWorkflowState blocks when dependency missing', async () => {
  const client = new GhostChannelClient({
    compressionLevel: 9,
    semanticThreshold: 0.7,
    auditEnabled: true,
    maxRetry: 3,
    completionMode: 'apply',
  })

  const result = await client.syncWorkflowState(
    'wf_001',
    'step_02',
    { status: 'completed' },
    ['step_01'],
  )

  assert.equal(result.success, false)
  assert.ok(result.errors.length > 0)
  assert.equal(result.errors[0].errorCode, 'GC-SYNC-DEP-BLOCKED')
})

test('receiveAck accepts monotonic progression', async () => {
  const client = new GhostChannelClient({
    compressionLevel: 9,
    semanticThreshold: 0.7,
    auditEnabled: true,
    maxRetry: 3,
    completionMode: 'apply',
  })

  await client.receiveAck({
    streamId: 'stream_001',
    sequenceNumber: 1,
    ackType: 'RECEIVED',
    status: 'ok',
    receiverId: 'role_b',
    merkleRootVerified: false,
    applied: false,
    timestampNs: 1712345678123456789,
  })

  await client.receiveAck({
    streamId: 'stream_001',
    sequenceNumber: 1,
    ackType: 'APPLIED',
    status: 'ok',
    receiverId: 'role_b',
    merkleRootVerified: true,
    applied: true,
    timestampNs: 1712345678123456799,
  })

  const stats = client.getStats()
  assert.equal(stats.lastAckType, 'APPLIED')
})

test('completionMode verify treats VERIFIED as terminal', () => {
  const client = new GhostChannelClient({
    compressionLevel: 9,
    semanticThreshold: 0.7,
    auditEnabled: true,
    maxRetry: 3,
    completionMode: 'verify',
  })

  assert.equal(client.isTerminalAck('VERIFIED'), true)
  assert.equal(client.isTerminalAck('RECEIVED'), false)
})

test('completionMode apply requires APPLIED/FAILED/ROLLED_BACK', () => {
  const client = new GhostChannelClient({
    compressionLevel: 9,
    semanticThreshold: 0.7,
    auditEnabled: true,
    maxRetry: 3,
    completionMode: 'apply',
  })

  assert.equal(client.isTerminalAck('VERIFIED'), false)
  assert.equal(client.isTerminalAck('APPLIED'), true)
  assert.equal(client.isTerminalAck('FAILED'), true)
  assert.equal(client.isTerminalAck('ROLLED_BACK'), true)
})

test('recoverFromFailure prefers latest snapshot', async () => {
  const client = new GhostChannelClient({
    compressionLevel: 9,
    semanticThreshold: 0.7,
    auditEnabled: true,
    maxRetry: 3,
    completionMode: 'apply',
  })

  await client.syncWorkflowState('wf_demo', 'step_01', { status: 'completed', payload: { x: 1 } }, [])
  await client.syncWorkflowState('wf_demo', 'step_01', { status: 'completed', payload: { x: 2 } }, [])

  const recovered = await client.recoverFromFailure('step_01', { status: 'fallback', payload: { x: -1 } })
  assert.equal(recovered.payload.x, 2)
})

test('validateAssets reports current assets valid', async () => {
  const client = new GhostChannelClient({
    compressionLevel: 9,
    semanticThreshold: 0.7,
    auditEnabled: true,
    maxRetry: 3,
    completionMode: 'apply',
  })

  const report = await client.validateAssets()
  assert.equal(report.valid, true)
  assert.ok(report.schemas)
  assert.ok(report.examples)
  assert.ok(report.mapping)
})

test('syncMemoryDelta produces object-flow state', async () => {
  const client = new GhostChannelClient({
    compressionLevel: 9,
    semanticThreshold: 0.7,
    auditEnabled: true,
    maxRetry: 3,
    completionMode: 'apply',
  })

  const result = await client.syncMemoryDelta(
    'a',
    'b',
    { __version__: 'v1', x: 1 },
    { __version__: 'v2', x: 2, y: 3 },
  )

  assert.equal(result.success, true)
  assert.ok(client.lastDeltaPayload)
  assert.equal(client.lastDeltaPayload.versionFrom, 'v1')
  assert.equal(client.lastDeltaPayload.versionTo, 'v2')
  assert.ok(client.lastEncryptedStream)
  assert.equal(client.lastEncryptedStream.type, 'MEMORY_SYNC')
})

test('syncMemoryDelta uses listAppends when list is only appended', async () => {
  const client = new GhostChannelClient({
    compressionLevel: 9,
    semanticThreshold: 0.7,
    auditEnabled: true,
    maxRetry: 3,
    completionMode: 'apply',
  })

  await client.syncMemoryDelta(
    'a',
    'b',
    { __version__: 'v1', log: [{ id: 1, content: 'hello' }] },
    { __version__: 'v2', log: [{ id: 1, content: 'hello' }, { id: 2, content: 'world' }] },
  )

  assert.ok(client.lastDeltaPayload.listAppends)
  assert.equal(client.lastDeltaPayload.listAppends.log.length, 1)
})

test('syncWorkflowState records snapshot chain', async () => {
  const client = new GhostChannelClient({
    compressionLevel: 9,
    semanticThreshold: 0.7,
    auditEnabled: true,
    maxRetry: 3,
    completionMode: 'apply',
  })

  await client.syncWorkflowState('wf_demo', 'step_chain', { status: 'completed', payload: { x: 1 } }, [])
  await client.syncWorkflowState('wf_demo', 'step_chain', { status: 'completed', payload: { x: 2 } }, [])

  assert.equal(client.snapshots.get('step_chain').length, 2)
  const recovered = await client.recoverFromFailure('step_chain', { status: 'fallback', payload: { x: -1 } })
  assert.equal(recovered.payload.x, 2)
})

test('syncWorkflowState produces workflow object-flow state', async () => {
  const client = new GhostChannelClient({
    compressionLevel: 9,
    semanticThreshold: 0.7,
    auditEnabled: true,
    maxRetry: 3,
    completionMode: 'apply',
  })

  const result = await client.syncWorkflowState('wf_x', 'step_01', { status: 'completed', payload: { x: 1 } }, [])
  assert.equal(result.success, true)
  assert.ok(client.lastWorkflowDeltaPayload)
  assert.ok(client.lastEncryptedStream)
  assert.equal(client.lastEncryptedStream.type, 'WORKFLOW_SYNC')
  assert.equal(client.lastEncryptedStream.sourceRoleId, 'wf_x')
  assert.equal(client.lastEncryptedStream.destinationRoleId, 'step_01')
})

test('syncWorkflowState waits for terminal ACK when awaitAck is enabled', async () => {
  const client = new GhostChannelClient({
    compressionLevel: 9,
    semanticThreshold: 0.7,
    auditEnabled: true,
    maxRetry: 3,
    completionMode: 'apply',
    awaitAck: true,
  })

  const pending = client.syncWorkflowState('wf_ack', 'step_01', { status: 'completed', payload: { x: 1 } }, [])
  await new Promise((r) => setTimeout(r, 10))

  await client.receiveAck({
    streamId: 'wf_ack:step_01',
    sequenceNumber: 1,
    ackType: 'VERIFIED',
    status: 'ok',
    receiverId: 'step_01',
    merkleRootVerified: true,
    applied: false,
    timestampNs: 1712345678123456789,
  })

  let settled = false
  pending.then(() => { settled = true }).catch(() => {})
  await new Promise((r) => setTimeout(r, 10))
  assert.equal(settled, false)

  await client.receiveAck({
    streamId: 'wf_ack:step_01',
    sequenceNumber: 1,
    ackType: 'APPLIED',
    status: 'ok',
    receiverId: 'step_01',
    merkleRootVerified: true,
    applied: true,
    timestampNs: 1712345678123456799,
  })

  const result = await pending
  assert.equal(result.success, true)
})

test('syncMemoryDelta waits for terminal ACK when awaitAck is enabled', async () => {
  const client = new GhostChannelClient({
    compressionLevel: 9,
    semanticThreshold: 0.7,
    auditEnabled: true,
    maxRetry: 3,
    completionMode: 'verify',
    awaitAck: true,
  })

  const pending = client.syncMemoryDelta('a', 'b', { __version__: 'v1' }, { __version__: 'v2', x: 1 })
  await new Promise((r) => setTimeout(r, 10))

  await client.receiveAck({
    streamId: client.lastEncryptedStream.streamId,
    sequenceNumber: client.lastEncryptedStream.sequenceNumber,
    ackType: 'VERIFIED',
    status: 'ok',
    receiverId: 'b',
    merkleRootVerified: true,
    applied: false,
    timestampNs: 1712345678123456789,
  })

  const result = await pending
  assert.equal(result.success, true)
})

test('syncMemoryDelta tracks stats correctly', async () => {
  const client = new GhostChannelClient({
    compressionLevel: 9,
    semanticThreshold: 0.7,
    auditEnabled: true,
    maxRetry: 3,
    completionMode: 'apply',
  })

  assert.equal(client.getStats().totalSyncs, 0)
  assert.equal(client.getStats().memorySyncs, 0)

  await client.syncMemoryDelta('a', 'b', { x: 1 }, { x: 2 })
  await client.syncMemoryDelta('c', 'd', { y: 1 }, { y: 2 })

  const stats = client.getStats()
  assert.equal(stats.totalSyncs, 2)
  assert.equal(stats.memorySyncs, 2)
})

test('syncWorkflowState tracks stats correctly', async () => {
  const client = new GhostChannelClient({
    compressionLevel: 9,
    semanticThreshold: 0.7,
    auditEnabled: true,
    maxRetry: 3,
    completionMode: 'apply',
  })

  await client.syncWorkflowState('wf_1', 'step_1', { status: 'done' }, [])
  await client.syncWorkflowState('wf_2', 'step_2', { status: 'done' }, [])

  const stats = client.getStats()
  assert.equal(stats.totalSyncs, 2)
  assert.equal(stats.workflowSyncs, 2)
})

test('receiveAck rejects invalid ack shape', async () => {
  const client = new GhostChannelClient({
    compressionLevel: 9,
    semanticThreshold: 0.7,
    auditEnabled: true,
    maxRetry: 3,
    completionMode: 'apply',
  })

  await assert.rejects(
    async () => client.receiveAck({ streamId: 's1' }),
    /ack object failed schema validation/
  )
})

test('receiveAck rejects ok ack with error', async () => {
  const client = new GhostChannelClient({
    compressionLevel: 9,
    semanticThreshold: 0.7,
    auditEnabled: true,
    maxRetry: 3,
    completionMode: 'apply',
  })

  await assert.rejects(
    async () => client.receiveAck({
      streamId: 's1',
      sequenceNumber: 1,
      ackType: 'APPLIED',
      status: 'ok',
      receiverId: 'r1',
      merkleRootVerified: true,
      applied: true,
      timestampNs: 1,
      error: { code: 'ERR' }
    }),
    /ok ack must not contain error/
  )
})

test('receiveAck rejects error ack without error', async () => {
  const client = new GhostChannelClient({
    compressionLevel: 9,
    semanticThreshold: 0.7,
    auditEnabled: true,
    maxRetry: 3,
    completionMode: 'apply',
  })

  await assert.rejects(
    async () => client.receiveAck({
      streamId: 's1',
      sequenceNumber: 1,
      ackType: 'FAILED',
      status: 'error',
      receiverId: 'r1',
      merkleRootVerified: false,
      applied: false,
      timestampNs: 1,
      error: null
    }),
    /error ack must contain ErrorObject/
  )
})

test('receiveAck rejects non-monotonic ack progression', async () => {
  const client = new GhostChannelClient({
    compressionLevel: 9,
    semanticThreshold: 0.7,
    auditEnabled: true,
    maxRetry: 3,
    completionMode: 'apply',
  })

  await client.receiveAck({
    streamId: 's1',
    sequenceNumber: 1,
    ackType: 'APPLIED',
    status: 'ok',
    receiverId: 'r1',
    merkleRootVerified: true,
    applied: true,
    timestampNs: 1,
  })

  await assert.rejects(
    async () => client.receiveAck({
      streamId: 's1',
      sequenceNumber: 1,
      ackType: 'RECEIVED',
      status: 'ok',
      receiverId: 'r1',
      merkleRootVerified: false,
      applied: false,
      timestampNs: 2,
    }),
    /ack progression must be monotonic/
  )
})

test('getAuditTrail returns recent entries', async () => {
  const client = new GhostChannelClient({
    compressionLevel: 9,
    semanticThreshold: 0.7,
    auditEnabled: true,
    maxRetry: 3,
    completionMode: 'apply',
  })

  await client.syncMemoryDelta('a', 'b', { x: 1 }, { x: 2 })
  await client.syncWorkflowState('wf', 'step', { status: 'done' }, [])

  const trail = client.getAuditTrail()
  assert.ok(Array.isArray(trail))
  assert.ok(trail.length >= 1)
})

test('recoverFromFailure returns fallback when no snapshots', async () => {
  const client = new GhostChannelClient({
    compressionLevel: 9,
    semanticThreshold: 0.7,
    auditEnabled: true,
    maxRetry: 3,
    completionMode: 'apply',
  })

  const fallback = { x: -1 }
  const recovered = await client.recoverFromFailure('nonexistent', fallback)
  assert.equal(recovered.x, -1)
})
