
```mermaid
erDiagram
          USER ||--o{ ITEM : has
          ITEM ||--o{ ITEM_IMAGE: has
          ITEM }|--|| CITY : is_published_in
```
