# Babson Bean Café — Database Project

## 1. The Scenario

**Scenario C — Babson Bean Café.** Babson Bean is a café on campus. Today its till records sales and its loyalty program lives on punch cards, and neither can answer a question. The café wants to know what sells, which add-ons (options like extra shot, oat milk, vanilla syrup) earn their keep, and who its regular customers are. This project builds a database that holds loyalty members, the menu, the options a drink can carry, orders, the lines and options on each order, and the payments that settle each order — so those questions can be answered with SQL instead of guesswork.

## 2. The ERD

```mermaid
erDiagram
  MEMBERS ||--o{ ORDERS : places
  PRODUCTS ||--o{ ORDER_LINES : "is ordered as"
  ORDERS ||--|{ ORDER_LINES : contains
  ORDER_LINES ||--o{ ORDER_LINE_OPTIONS : carries
  OPTIONS ||--o{ ORDER_LINE_OPTIONS : "is added as"
  ORDERS ||--|{ PAYMENTS : "is settled by"

  MEMBERS {
    int member_id PK
    string first_name
    string mobile_number
    string email
    date join_date
    int points_balance
  }

  PRODUCTS {
    int product_id PK
    string name
    string category
    decimal price
    decimal cost
    boolean is_available
  }

  OPTIONS {
    int option_id PK
    string name
    decimal price
    decimal cost
  }

  ORDERS {
    int order_id PK
    datetime order_datetime
    int member_id FK
    string channel
  }

  ORDER_LINES {
    int order_line_id PK
    int order_id FK
    int product_id FK
    int quantity
    decimal price_charged
  }

  ORDER_LINE_OPTIONS {
    int order_line_id PK, FK
    int option_id PK, FK
    decimal price_charged
  }

  PAYMENTS {
    int payment_id PK
    int order_id FK
    string method
    decimal amount
  }
```

## 3. What One Row Means

- One row of `members` is one loyalty member who has joined the program, with the mobile number and points balance they currently have.
- One row of `products` is one item that can appear on the menu, with the price and cost it has today and whether it is available today.
- One row of `options` is one add-on a drink can carry, such as oat milk, with the price and cost of adding it once.
- One row of `orders` is one order placed at the café, at one date and time, through one channel, by a member if one was involved.
- One row of `order_lines` is one product on one order, at the quantity ordered and the price charged that day.
- One row of `order_line_options` is one option added to one order line, at the price charged that day.
- One row of `payments` is one amount paid toward one order, by one method.

## 4. Design Choices

