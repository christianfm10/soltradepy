# SolTradePy

Proyecto experimental de trading algorítmico para memecoins en Solana (Pump.Fun, BonkFun, etc.), desarrollado en Python con enfoque en **automatización**, **baja latencia** y **arquitectura modular**.

## Objetivos principales

- ✅ Detectar memecoins recién lanzadas en múltiples fuentes (PumpPortal, BonkFun, etc.)
- ✅ Notificaciones en tiempo real (Telegram)
- ✅ Persistencia estructurada (SQLite + SQLAlchemy)
- ✅ Escalable para agregar más fuentes fácilmente

## Stack inicial

- `uv` como package/env manager
- `Python 3.14`
- `SQLAlchemy + Pydantic`
- `RPCs: Helius / Moralis`
- `PumpPortal / AxiomTradeClient / BonkFun / etc.`

## Estado

🚧 Desarrollo desde cero — estructura inicial del proyecto en construcción.

## Cómo ejecutar

```bash
uv run python main.py