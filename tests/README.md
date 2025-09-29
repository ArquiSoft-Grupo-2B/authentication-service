# Tests - Authentication Service

Este directorio contiene las pruebas unitarias e integración para el servicio de
autenticación.

## Estructura de Pruebas

```
tests/
├── domain/
│   ├── entities/          # Pruebas de entidades del dominio
│   └── services/          # Pruebas de servicios del dominio
├── application/           # Pruebas de casos de uso
├── infrastructure/        # Pruebas de repositorios en memoria
├── test_integration.py    # Pruebas de integración completas
└── conftest.py           # Configuración compartida de pytest
```

## Tipos de Pruebas

### 🔧 Pruebas Unitarias

- **Entidades**: Validación de reglas de negocio en la clase `User`
- **Servicios**: Lógica de negocio en `UserService`
- **Repositorios**: Implementación en memoria de `InMemoryUserRepository`
- **Casos de Uso**: Coordinación entre capas en `UserUseCases`

### 🔄 Pruebas de Integración

- Flujo completo a través de todas las capas
- Consistencia de datos entre repositorio, servicio y casos de uso
- Propagación de errores entre capas
- Aislamiento entre instancias de repositorio

## Cómo Ejecutar las Pruebas

### Todas las pruebas

```bash
python -m pytest tests/ -v
```

### Con reporte de cobertura

```bash
python -m pytest tests/ --cov=src --cov-report=term-missing
```

### Solo pruebas unitarias

```bash
python -m pytest tests/domain/ tests/application/ tests/infrastructure/ -v
```

### Solo pruebas de integración

```bash
python -m pytest tests/test_integration.py -v
```

### Generar reporte HTML de cobertura

```bash
python -m pytest tests/ --cov=src --cov-report=html:htmlcov
```

## Herramientas Utilizadas

- **pytest**: Framework de pruebas
- **pytest-cov**: Reporte de cobertura de código
- **InMemoryUserRepository**: Repositorio en memoria para pruebas aisladas

## Cobertura Actual

- **Total**: ~95% de cobertura de código
- **Entidades**: 100%
- **Servicios**: 100%
- **Casos de Uso**: 100%
- **Repositorios**: 100%

Las líneas no cubiertas corresponden principalmente a métodos abstractos del
repositorio base.
