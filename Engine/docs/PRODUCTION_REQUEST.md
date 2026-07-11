# Production Request

A Production Request describes **what** the operator wants to generate.

Example:

```python
ProductionRequestModel(

    request_id="REQ_001",

    subject="Physics",

    unit="P1",

    chapter="CH1",

    subtopic="ST4",

    set_no="S1",

    total_questions=250,

    batch_size=100

)
```

The request **does not** contain:

- question_start
- batch_no
- ProductionOrderModel

Those values are automatically determined by the Queue Builder.

The Queue Builder converts one Production Request into one or more Production Orders.
