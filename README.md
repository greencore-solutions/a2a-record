# A2A Passport — one GTIN, one call, everything GSC knows, signed

The hubs are the records; A2A-Passport.ai issues the passport.

> The hubs are the records; A2A-Passport.ai issues the passport. A passport is a signed document for a product or a retail banner: where its record lives, where it is cleared, who lists it, where the money door is. Issued live from the GSC hubs, stamped every week. A2A Passport is operated by GreenCore Solutions Corp.: one signed document per product (a Global Trade Item Number, GTIN) or retail banner, composed live from the GSC hubs — A2A Grocery, A2A Cosmetics, A2A Peptides, A2A Retailmedia and the compliance records — and signed (EdDSA). Three tools: get_passport, list_passports, verify_passport. Every field is a hub's answer, word for word, with the door and the time it was read, or it is absent with a note: the passport never infers. A product no hub holds gets no passport. Reads are open; a verified, countersigned copy settles by x402. Artificial intelligence makes mistakes. A2A Passport is an agentic information source, not a recommendation. No ads, ever. No rank for sale. Trade only.

A2A Passport is built and run by GreenCore Solutions Corp. (github.com/greencore-solutions). This is the public connect kit, MIT.

## The door

streamable-HTTP, stateless, server name `a2a-passport`, door version 1.0.1, 3 tools (read from the wire)

- Endpoint: `https://mcp.a2a-passport.ai/mcp` — any client that speaks streamable-HTTP: `{ "url": "https://mcp.a2a-passport.ai/mcp", "transport": "streamable-http" }`
- Agent Card (signed): `https://a2a-passport.ai/.well-known/agent-card.json`
- Key: `https://a2a-passport.ai/.well-known/jwks.json` (EdDSA, key id `a2apass-2026-10`)
- No registration and no token: every read is open.

## The tools

- `get_passport` — The signed passport of a product (a Global Trade Item Number, GTIN) or a retail banner (market/banner, e.g. FR/Carrefour): which hub holds its record, where it is cleared, its compliance records, who lists it, where the payment door is. Read live from the GSC hubs on every call; the first call issues version 1. subject = a GTIN (8 to 14 digits) or market/banner; kind = gtin or banner (optional).
- `list_passports` — The passports on the register: ids, kinds, markets, versions and issue times, newest first. No bodies. Filter by kind (gtin or banner), market, or issued since a time; paginated.
- `verify_passport` — Check a passport: is the signature valid, is the chain of versions intact, how old is the stamp, was any section not read. Verifies from the published key at /.well-known/jwks.json.

## The document

One envelope for both kinds (a product by its GTIN, or a retail banner as `market/banner`): `passport_id`, `kind`, `subject`, `issued_at`, `version`, `previous_version_hash`, `issuer`, `signature`, `delta`, and the `body`.
Every field in the body is a hub's answer, word for word, with the door, the tool and the time it was read — or it is absent with a note. The passport never infers.

- Current version: `https://a2a-passport.ai/passport/{id}.json`
- One version: `https://a2a-passport.ai/passport/{id}/v{n}.json`
- Passport #1: `https://a2a-passport.ai/passport/gtin-03284230006408.json`
- The register (live counts): `https://a2a-passport.ai/passports/register.json`

A product that no hub holds on its record gets no passport.

## Verify a passport yourself

The signature is a detached JSON Web Signature (EdDSA) over the passport without its `signature` field, keys sorted, compact JSON, UTF-8. `examples/verify_passport.py` does it with the published key and nothing else.

## The countersigned copy

Reading a passport is free. A verified, countersigned copy settles at `https://a2a-passport.ai/api` (x402, two accept entries). A passport that is not on the register answers HTTP 403 and is not charged.

## Examples

- `examples/generic_mcp_client.py` — a stock client: lists the tools, reads passport #1, verifies it on the door.
- `examples/verify_passport.py` — fetches a passport and the key over plain HTTP and verifies the signature offline.

Artificial intelligence makes mistakes. A2A Passport is an agentic information source, not a recommendation. No ads, ever. No rank for sale. Trade only.
