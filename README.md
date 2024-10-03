# Install dependencies using
```bash
  poetry install
```

# Run application using command
```bash
  python -m app
```

# ENV variables to define
```bash
RABBITMQ_HOST
RABBITMQ_PORT 
RABBITMQ_USER
RABBITMQ_PASSWORD
EXCHANGE_NAME
```

# RUN CONSUMERS 
```bash
python -m app.user_migration.consumer.TransferCitizenConsumer
```
```bash
python -m python -m app.user_migration.consumer.TransferCitizenConfirmConsumer
```