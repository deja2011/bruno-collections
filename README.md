# bruno-collections

[Bruno](https://www.usebruno.com/) API collections for the exchanges we work
with. Each top-level directory is a self-contained Bruno collection — open it
directly in the Bruno app, or run it with the CLI:

```sh
cd <collection> && bru run -r . --env production
```

## Collections

| Collection | API | Requests | Auth |
| --- | --- | --- | --- |
| [`binance-spot`](binance-spot) | Binance Spot and Wallet (`api.binance.com`) | 21 | public; `apiKey` for MARKET_DATA; HMAC for selected USER_DATA |
| [`binance-usds-futures`](binance-usds-futures) | Binance USDⓈ-M Futures (`fapi.binance.com`) | 34 | public; `apiKey` for MARKET_DATA endpoints |
| [`binance-coin-futures`](binance-coin-futures) | Binance COIN-M Futures (`dapi.binance.com`) | 26 | public; `apiKey` for MARKET_DATA endpoints |
| [`binance-options`](binance-options) | Binance European Options (`eapi.binance.com`) | 12 | public |
| [`aster-spot`](aster-spot) | Aster spot wallet (`asterdex.com`) | 3 | public |
| [`coinbase-exchange`](coinbase-exchange) | Coinbase Exchange (`api.exchange.coinbase.com`) | 87 | HMAC-signed (collection pre-request script) |
| [`hyperliquid`](hyperliquid) | Hyperliquid (`api.hyperliquid.xyz`) | 89 | public Info requests; signed Exchange templates |

Credentials are never committed: environment files declare secrets via
`vars:secret`, and Bruno stores their values outside the collection.

## Conventions

Collections follow one shared layout so they are readable side by side:

- `bruno.json` — collection manifest, `name` matching the directory name.
- `collection.bru` — collection-level auth, shared headers, any pre-request
  signing script, and a `docs` block covering setup and base URLs.
- `environments/*.bru` — one file per environment, each defining `baseUrl`
  (plus `vars:secret` for credentials where the API needs them).
- Request folders in Title Case with a `folder.bru` (`name` + `seq`).
- Request files in `kebab-case.bru`; the `meta.name` inside is sentence case.
- Every request has a `docs` block: title, `METHOD /path` with its auth tier,
  annotated query/path parameters, and a link to the upstream reference.
- Requests use `{{baseUrl}}`; optional parameters are present but disabled
  (`~` prefix) so they document the full surface.
- Only public / read-only endpoints are included unless noted otherwise.

## Regenerating the Binance collections

The four Binance collections were generated from the official Postman
collections at https://github.com/binance/binance-api-postman, pinned at commit
`03a10b5` (2026-07-22). That repo is not vendored here — clone it separately if
you need to regenerate.

Upstream metadata has known errors that were corrected during generation and
must be re-applied on any regeneration:

- COIN-M `topLongShortAccountRatio` takes `pair`, not `symbol`.
- COIN-M contract symbols must be explicit (`BTCUSD_PERP`), not pair names.
- Options contract symbols expire and need periodic refresh.
- Invalid values on COIN-M statistics endpoints return a WAF `403`, not a JSON
  error — so bad parameters look like auth failures.

## Regenerating the Hyperliquid collection

The native Bruno collection is converted from the OpenCollection/YAML source in
the sibling `hyperliquid-bruno` directory:

```sh
python3 scripts/import-hyperliquid.py ../hyperliquid-bruno hyperliquid
```
