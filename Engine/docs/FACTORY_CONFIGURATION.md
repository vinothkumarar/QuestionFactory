# Question Factory OS

## Factory Configuration

The factory reads all production settings from:

```
config/factory_config.py
```

## Example

```python
PRODUCTION_ORDERS = [

    {

        "order_id": "ORDER_001",

        "subject": "Physics",

        "unit": "P1",

        "chapter": "CH1",

        "subtopic": "ST4",

        "set_no": "S1",

        "batch_no": 6,

        "question_start": 501,

        "question_count": 100

    }

]
```

To generate another batch, simply add another production order to the list.

Future versions of the factory will automatically process every order in sequence.
