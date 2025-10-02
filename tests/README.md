# Tests - Authentication Service

Este directorio contiene las pruebas unitarias para el servicio de autenticación,
enfocándose exclusivamente en el dominio del sistema.

## Estructura de Pruebas

```
tests/
├── domain/
│   ├── entities/          # Pruebas unitarias de entidades del dominio
│   └── services/          # Pruebas unitarias de servicios del dominio
└── conftest.py           # Configuración compartida de pytest
```

## Tipos de Pruebas

### 🔧 Pruebas Unitarias del Dominio

- **Entidades**: Validación de reglas de negocio en las entidades del dominio (User)
- **Servicios**: Lógica de negocio en servicios del dominio (UserService) usando mocks para repositorios

## Cómo Ejecutar las Pruebas

### Todas las pruebas unitarias

```bash
python -m pytest tests/ -v
```

### Con reporte de cobertura

```bash
python -m pytest tests/ --cov=src/domain --cov-report=term-missing
```

### Solo pruebas de entidades

```bash
python -m pytest tests/domain/entities/ -v
```

### Solo pruebas de servicios

```bash
python -m pytest tests/domain/services/ -v
```

### Generar reporte HTML de cobertura

```bash
python -m pytest tests/ --cov=src/domain --cov-report=html:htmlcov
```

```

## Herramientas Utilizadas

- **pytest**: Framework de pruebas
- **pytest-cov**: Reporte de cobertura de código
- **unittest.mock**: Mocking para aislar unidades de código bajo prueba

## Cobertura Actual

- **Entidades**: 100% de cobertura
- **Servicios**: 100% de cobertura del dominio

Las pruebas se enfocan exclusivamente en el dominio del sistema, evitando
dependencias externas y manteniendo la pureza arquitectónica.
