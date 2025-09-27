# Authentication Service

Un servicio de autenticación basado en **FastAPI** y **GraphQL** que utiliza
Firebase como backend de autenticación. Este servicio implementa una
arquitectura hexagonal (Clean Architecture) para separar las capas de dominio,
aplicación e infraestructura.

## 📋 Descripción

El Authentication Service proporciona funcionalidades completas de gestión de
usuarios y autenticación:

- **Gestión de usuarios**: Crear, obtener, actualizar, eliminar y listar
  usuarios
- **Autenticación**: Login de usuarios con tokens JWT
- **Verificación de tokens**: Validación y decodificación de tokens de
  autenticación
- **Recuperación de contraseña**: Envío de emails para restablecer contraseña
- **Backend Firebase**: Integración completa con Firebase Authentication y
  Firestore

### Arquitectura

```
src/
├── domain/           # Entidades de dominio, repositorios e interfaces
├── application/      # Casos de uso y lógica de aplicación
└── infrastructure/   # Implementaciones concretas (Firebase, GraphQL, etc.)
```

## 🚀 Instalación y Configuración

### Requisitos Previos

- Python 3.11 o superior
- Docker y Docker Compose (para ejecución con contenedores)
- Cuenta de Firebase con proyecto configurado

### Configuración de Firebase

1. Crea un proyecto en [Firebase Console](https://console.firebase.google.com/)
   o acceder a uno ya existente.
2. Habilita Authentication y Firestore Database
3. Genera una clave de servicio y descarga el archivo JSON
4. Configura las variables de entorno en `configs/.env`:

```env
FIREBASE_CREDENTIALS_JSON='{"type": "service_account", ...}'
API_KEY='tu_api_key_de_firebase'
```

## 🏃‍♂️ Ejecución Local

### Opción 1: Con uvicorn (Desarrollo)

1. **Instalar dependencias**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Ejecutar el servidor**:

   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Acceder al servicio**:
   - API: http://localhost:8000
   - GraphQL Playground: http://localhost:8000/graphql

### Opción 2: Con Docker

1. **Construir y ejecutar con Docker Compose**:

   ```bash
   docker-compose up --build
   ```

2. **Acceder al servicio**:
   - API: http://localhost:8000
   - GraphQL Playground: http://localhost:8000/graphql

### Opción 3: Solo Docker

```bash
# Construir la imagen
docker build -t authentication-service .

# Ejecutar el contenedor
docker run -p 8000:8000 authentication-service
```

## 📊 API GraphQL

El servicio expone una API GraphQL con las siguientes operaciones:

### Queries (Consultas)

#### 1. Obtener un usuario específico

```graphql
query GetUser {
  getUser(userId: "user_id_aqui") {
    id
    email
    alias
    photoUrl
  }
}
```

#### 2. Listar todos los usuarios

```graphql
query ListUsers {
  listUsers {
    id
    email
    alias
    photoUrl
  }
}
```

### Mutations (Mutaciones)

#### 1. Crear un nuevo usuario

```graphql
mutation CreateUser {
  createUser(
    userInput: {
      email: "usuario@ejemplo.com"
      password: "password123"
      alias: "UsuarioEjemplo"
    }
  ) {
    id
    email
    alias
    photoUrl
  }
}
```

#### 2. Iniciar sesión

```graphql
mutation LoginUser {
  loginUser(email: "usuario@ejemplo.com", password: "password123") {
    localId
    email
    alias
    idToken
    registered
    refreshToken
    expiresIn
  }
}
```

#### 3. Actualizar usuario

```graphql
mutation UpdateUser {
  updateUser(
    userId: "user_id_aqui"
    userInput: {
      email: "nuevo@ejemplo.com"
      password: "newpassword123"
      alias: "NuevoAlias"
    }
  ) {
    id
    email
    alias
    photoUrl
  }
}
```

#### 4. Enviar email de recuperación de contraseña

```graphql
mutation SendPasswordReset {
  sendPasswordResetEmail(email: "usuario@ejemplo.com") {
    success
    response
  }
}
```

#### 5. Eliminar usuario

```graphql
mutation DeleteUser {
  deleteUser(userId: "user_id_aqui")
}
```

#### 6. Verificar token

```graphql
mutation VerifyToken {
  verifyToken(idToken: "token_jwt_aqui") {
    uid
    email
    emailVerified
    userInfo {
      name
      userId
    }
  }
}
```

## 🌐 Endpoints REST

### Endpoint principal

- `GET /` - Mensaje de bienvenida al servicio

### GraphQL

- `POST /graphql` - Endpoint principal de GraphQL
- `GET /graphql` - GraphQL Playground (interfaz web)

## 📝 Ejemplos de Uso

### Crear un usuario y hacer login

1. **Crear usuario**:

```bash
curl -X POST http://localhost:8000/graphql \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation { createUser(userInput: { email: \"test@example.com\", password: \"password123\", alias: \"TestUser\" }) { id email alias } }"
  }'
```

2. **Hacer login**:

```bash
curl -X POST http://localhost:8000/graphql \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation { loginUser(email: \"test@example.com\", password: \"password123\") { idToken localId email } }"
  }'
```

### Usar GraphQL Playground

1. Navega a http://localhost:8000/graphql
2. Usa la interfaz web para escribir y ejecutar consultas
3. Explora el schema usando la documentación integrada

## 🏗️ Arquitectura del Proyecto

### Capas de la Arquitectura Hexagonal

- **Dominio** (`src/domain/`): Entidades y reglas de negocio
- **Aplicación** (`src/application/`): Casos de uso y coordinación
- **Infraestructura** (`src/infrastructure/`): Implementaciones concretas

### Tecnologías Utilizadas

- **FastAPI**: Framework web moderno para Python
- **Strawberry GraphQL**: Librería GraphQL para Python
- **Firebase**: Backend de autenticación y base de datos
- **Uvicorn**: Servidor ASGI
- **Docker**: Containerización
- **Pytest**: Framework de testing

## 📂 Estructura de Archivos

```
authentication-service/
├── src/
│   ├── domain/
│   │   ├── entities/          # User, Token
│   │   ├── repositories/      # Interfaces de repositorios
│   │   └── services/          # Servicios de dominio
│   ├── application/
│   │   ├── user_use_cases.py  # Casos de uso de usuarios
│   │   └── token_use_cases.py # Casos de uso de tokens
│   └── infrastructure/
│       ├── db/                # Configuración Firebase
│       ├── graphql/           # Schema y tipos GraphQL
│       ├── repositories/      # Implementaciones de repositorios
│       └── rest/              # APIs REST adicionales
├── tests/                     # Tests unitarios e integración
├── configs/                   # Configuración (.env)
├── main.py                    # Punto de entrada
├── requirements.txt           # Dependencias
├── Dockerfile                 # Configuración Docker
└── docker-compose.yml         # Orquestación Docker
```

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más
detalles.

## 👥 Equipo

**ArquiSoft - Grupo 2B**

---

Para más información o soporte, contacta al equipo de desarrollo.
