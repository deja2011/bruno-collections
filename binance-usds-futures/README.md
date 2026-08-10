# Binance USDS-M Futures REST API — public market data

Public market-data endpoints of the Binance USDS-Margined Futures REST API. 34 requests, generated from the official Binance Postman
collection (`binance/binance-api-postman`) and validated against the live API.

- **Market Data** — 34 requests

## Usage

Open this folder as a collection in Bruno (or run `bru run -r . --env production`
with the Bruno CLI). Select an environment first:

- `production`: https://fapi.binance.com
- `testnet`: https://testnet.binancefuture.com
- `demo`: https://demo-fapi.binance.com

All endpoints are public. The few marked `(MARKET_DATA)` need an API key (but
no signature): put it in the `apiKey` secret variable of the active environment
and the collection pre-request script sends the `X-MBX-APIKEY` header for you.

Private (signed) endpoints are intentionally not included.

## References

- https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data
- Changelog: https://developers.binance.com/en/docs/products/spot/CHANGELOG
