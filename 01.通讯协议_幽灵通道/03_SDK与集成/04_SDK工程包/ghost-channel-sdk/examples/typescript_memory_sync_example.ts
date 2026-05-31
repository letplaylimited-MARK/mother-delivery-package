import { GhostChannelClient } from '../typescript/src/index.ts'

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
  { __version__: 'v1' },
  { __version__: 'v2' },
  'protocol scope',
)

console.log(result)
