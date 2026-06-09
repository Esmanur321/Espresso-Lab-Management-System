/**
 * Decode JWT payload (middle segment) without verifying the signature.
 * Used only after our own backend issued the token via OAuth redirect.
 */
export function parseJwtPayload(token: string): Record<string, unknown> | null {
  const parts = token.split('.');
  if (parts.length !== 3) return null;
  const payload = parts[1];
  if (!payload) return null;
  try {
    const base64 = payload.replace(/-/g, '+').replace(/_/g, '/');
    const pad = base64.length % 4;
    const padded = pad ? base64 + '='.repeat(4 - pad) : base64;
    let json: string;
    if (typeof globalThis.atob === 'function') {
      json = globalThis.atob(padded);
    } else {
      json = Buffer.from(padded, 'base64').toString('utf8');
    }
    return JSON.parse(json) as Record<string, unknown>;
  } catch {
    return null;
  }
}
