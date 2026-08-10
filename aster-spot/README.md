# Aster spot REST API — public wallet endpoints

Public (unauthenticated) wallet endpoints of the Aster spot API. 3 requests,
validated against the live API.

- **Wallet** — 3 requests

## Usage

Open this folder as a collection in Bruno (or run `bru run -r . --env production`
with the Bruno CLI). Select an environment first:

- `production`: https://www.asterdex.com

All endpoints are public — no credentials required.

Private (signed) endpoints are intentionally not included.

## Why this is not a Binance environment

These requests live under Aster's proprietary `/bapi/futures/v1/public/future/aster`
namespace, which has no Binance counterpart — the Binance collections are all
`/api/v3`, `/fapi/v1`, `/dapi/v1`, `/eapi/v1`. Swapping only `baseUrl` would break
requests in both directions, so `aster-spot` stays a standalone collection that
follows the same conventions as the Binance ones.

## References

- https://docs.asterdex.com/
