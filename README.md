# RabbitMQ Amusement Park Ticketing System

This repository contains my implementation of an asynchronous messaging system for an amusement park ticketing application, using RabbitMQ. This project is part of an assignment I completed for the Cloud Software and Systems course offered by the Department of Computer Science at Aalto University. It focuses on building distributed systems with asynchronous messaging principles.

## Project Overview

The application simulates an amusement park ticketing system, comprising of three main components:

- **Ticket Machine (TicketEventProducer)**: Simulates customers tapping their phone to issue ticket events.
- **Ticket Worker (TicketWorker)**: Processes ticket events by verifying customer details and ride prices, and then notifying the customers.
- **Customer App (CustomerEventConsumer)**: Receives notifications about ticket processing for individual customers.

## Message Flow Diagram

```mermaid
flowchart TD
    A(Ticket Machine) -->|Direct Exchange| B[Worker Queue]
    B --> |Invalid|Z[Dead Letter Exchange]
    B --> |Valid| C{ }
    C --> Y[Worker 1]
    C --> X[Worker 2]
    X --> D[Topic Exchange]
    Y --> D[Topic Exchange]
    D --> E(Customer App)
```

## System Architecture

```mermaid
sequenceDiagram
    participant TM as Ticket Machine
    participant TW as Ticket Worker
    participant CA as Customer App
    participant RMQ as RabbitMQ Broker

    TM->>RMQ: TicketEvent
    RMQ->>TW: Forward TicketEvent
    TW->>TW: Process Event
    TW->>RMQ: CustomerEvent
    RMQ->>CA: Forward CustomerEvent to relevant Customer
