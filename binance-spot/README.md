# Binance Spot REST API — public endpoints

Market data and general endpoints of the Binance Spot REST API. 19 requests, generated from the official Binance Postman
collection (`binance/binance-api-postman`) and validated against the live API.

- **General** — 4 requests
- **Market** — 15 requests

## Usage

Open this folder as a collection in Bruno (or run `bru run -r . --env production`
with the Bruno CLI). Select an environment first:

- `production`: https://api.binance.com
- `testnet`: https://testnet.binance.vision
- `demo`: https://demo-api.binance.com

All endpoints are public. The few marked `(MARKET_DATA)` need an API key (but
no signature): put it in the `apiKey` secret variable of the active environment
and the collection pre-request script sends the `X-MBX-APIKEY` header for you.

Private (signed) endpoints are intentionally not included.

## References

- https://developers.binance.com/docs/binance-spot-api-docs/rest-api/general-endpoints
- https://developers.binance.com/docs/binance-spot-api-docs/rest-api/market-data-endpoints
- Changelog: https://developers.binance.com/en/docs/products/spot/CHANGELOG
