# em DSL Reference & Cheatsheet

The `em` tool (`@milehimikey/em`) is a slice-first text DSL rendered to a strict Graphviz
swimlane grid. Use this reference so the models you generate are valid and render cleanly.
Keep `.em` files focused on structure; put deep design in markdown linked via `note`.

## CLI

```bash
em init [file]
em render <file> -o out.svg
em render <file> --emit-dot
em render <file> --keep-empty-lanes
em watch <file> -o out.svg
em validate <file>
```

Install if missing: `npm i -g @milehimikey/em`. PNG works with no system deps; PDF needs
`rsvg-convert`.

## Grammar

```text
model "Name"

persona Name
context Name

slice "Name" {
  ui   Free Text @Persona
  command Free Text
  view Free Text from "Event A", "Event B"
  event Free Text @Context
  processor Free Text from "View"
}

arrow From Element -> To Element
```

## Element kinds

| Keyword | Band | Meaning |
|---|---|---|
| `ui` | persona | screen / interface |
| `command` | API | state-changing request |
| `view` | API | read model / projection |
| `event` | context | recorded fact (past tense) |
| `processor` / `automation` / `saga` / `translation` | automation | system reaction / adapter |

## Pattern mapping

```em
slice "Place Order" {
  ui Checkout @Customer
  command Place Order
  event Order Placed @Order
}

slice "Open Orders" {
  view Open Orders from "Order Placed"
  ui Order List @Customer
}

slice "Orders To Fulfill" {
  view Orders To Fulfill from "Order Placed"
  processor Fulfillment Service
}
slice "Ship Order" {
  command Ship Order
  event Order Shipped @Shipping
}

slice "Carrier Webhook" {
  translation Carrier Adapter
}
slice "Confirm Delivery" {
  command Confirm Delivery
  event Delivery Confirmed @Shipping
}
```

## Validator rules

- One element per band per slice.
- Every command should record at least one event.
- Every view should have a source.
- Automations and translations are always two slices.
- A reaction slice never contains an event.

