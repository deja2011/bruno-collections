# Hyperliquid API — Bruno collection

Native Bruno requests for the Hyperliquid API. The collection contains 89
requests converted from the sibling `hyperliquid-bruno` OpenCollection source.

- **Info** — 30 general public Info requests
- **Perpetuals** — 17 perpetuals-specific public Info requests
- **Spot** — 7 spot-specific public Info requests
- **Exchange** — 31 signed action templates
- **Websocket Payloads** — 4 WebSocket payload examples represented as the
  source collection's HTTP templates

## Environments

Select an environment before sending requests:

| Environment | Base URL |
| --- | --- |
| `production` | `https://api.hyperliquid.xyz` |
| `testnet` | `https://api.hyperliquid-testnet.xyz` |

Info requests are public. Requests containing a user address use the zero
address as an inert placeholder; replace it with the master or sub-account
address you intend to query.

Exchange requests contain deliberately invalid zero signatures and fixed sample
nonces. Replace the action fields, nonce, and signature with correctly signed
values before sending them. No private key or credential is stored in this
collection.

The Websocket Payloads folder preserves the source payload examples. Copy their
JSON bodies into Bruno's WebSocket client connected to
`wss://api.hyperliquid.xyz/ws`; they are not normal `/info` REST payloads.

## References

- https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint
- https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/exchange-endpoint
- https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/websocket

## Regenerating

From the repository root, with the source collection checked out alongside this
repository:

```sh
python3 scripts/import-hyperliquid.py ../hyperliquid-bruno hyperliquid
```
