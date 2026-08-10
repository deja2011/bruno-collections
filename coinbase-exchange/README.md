# Coinbase Exchange REST API — Bruno collection

A [Bruno](https://www.usebruno.com/) collection covering the **full Coinbase
Exchange (Institutional) REST API** — 87 requests across 16 folders — generated
from the official OpenAPI specification.

> This is the Coinbase **Exchange** API (`api.exchange.coinbase.com`), the
> institutional trading API — not the Coinbase International Exchange API
> (`api.international.coinbase.com`), which is a separate product.

Reference docs: https://docs.cdp.coinbase.com/exchange/rest-api

## Environments

Two environments are provided; pick one before sending requests:

| Environment  | Base URL                                             |
| ------------ | ---------------------------------------------------- |
| `production` | `https://api.exchange.coinbase.com`                  |
| `sandbox`    | `https://api-public.sandbox.exchange.coinbase.com`   |

## Authentication

Private endpoints require an API key generated at
<https://exchange.coinbase.com/profile/api> (or the sandbox equivalent — sandbox
keys are separate). Set these variables on the active environment:

- `apiKey`
- `apiSecret`
- `apiPassphrase`

**Signing is automatic.** The collection-level pre-request script
(`collection.bru`) builds the `CB-ACCESS-KEY / SIGN / TIMESTAMP / PASSPHRASE`
headers for every request:

```
prehash   = timestamp + method + requestPath + body
signature = base64( HMAC-SHA256( base64-decode(apiSecret), prehash ) )
```

If the credentials are blank the signing step is skipped, so **public endpoints
work out of the box** with no setup.

### Public (no credentials needed)

Most of **Products**, **Currencies**, and a few **Wrapped assets** endpoints are
public. These return `200 OK` immediately after selecting an environment.

## Folder layout

`Accounts`, `Address book`, `Coinbase accounts`, `Conversions`, `Currencies`,
`Fees`, `Futures`, `Loans`, `Orders`, `Products`, `Profiles`, `Reports`,
`Transfers`, `Travel Rules`, `Users`, `Wrapped assets`.

Path parameters use placeholder values (e.g. `ACCOUNT_ID`, `BTC-USD`); optional
query parameters are included but disabled (prefixed with `~`) so you can toggle
them on as needed. POST/PUT requests ship with example JSON bodies.

## Running from the CLI

```bash
npm install -g @usebruno/cli
cd coinbase-exchange
bru run Products -r --env production          # all public product endpoints
bru run . -r --env production                 # entire collection
```
