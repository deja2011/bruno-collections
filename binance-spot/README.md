# Binance Spot and Wallet REST APIs

Market data and general endpoints of the Binance Spot REST API, plus selected
Wallet endpoints. The 19 Spot requests were generated from the official Binance
Postman collection (`binance/binance-api-postman`) and validated against the live
API.

- **General** — 4 requests
- **Market** — 15 requests
- **Wallet** — 2 requests

## Usage

Open this folder as a collection in Bruno (or run `bru run -r . --env production`
with the Bruno CLI). Select an environment first:

- `production`: https://api.binance.com
- `testnet`: https://testnet.binance.vision
- `demo`: https://demo-api.binance.com

Public Spot endpoints need no credentials. Requests marked `(MARKET_DATA)` need
an API key (but no signature): put it in the `apiKey` secret variable of the
active environment. The All Coins Information Wallet request is signed; also set
the `apiSecret` secret and its pre-request script generates the timestamp and
HMAC-SHA256 signature automatically. Never commit either credential.

## References

- https://developers.binance.com/docs/binance-spot-api-docs/rest-api/general-endpoints
- https://developers.binance.com/docs/binance-spot-api-docs/rest-api/market-data-endpoints
- https://developers.binance.com/en/docs/catalog/core-trading-wallet/api/rest-api
- Changelog: https://developers.binance.com/en/docs/products/spot/CHANGELOG
