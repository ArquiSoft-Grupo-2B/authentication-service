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
- **Autenticación**: Login de usuarios con tokens JWT y autorización mediante
  headers
- **Verificación de tokens**: Validación y decodificación de tokens de
  autenticación
- **Recuperación de contraseña**: Envío de emails para restablecer contraseña
- **Backend Firebase**: Integración completa con Firebase Authentication y
  Firestore
- **Autorización por Header**: Sistema de autenticación mediante header
  `Authorization` con tokens Bearer

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

### 🔐 Autenticación

El servicio utiliza autenticación basada en tokens JWT mediante el header
`Authorization`. Para las operaciones que requieren autenticación, incluye el
token en el header de la siguiente manera:

```
Authorization: Bearer <tu_token_jwt>
```

**Operaciones que requieren autenticación:**

- `updateUser` - Actualizar usuario (usa el ID del token, no requiere parámetro
  userId)
- `deleteUser` - Eliminar usuario (usa el ID del token, no requiere parámetro
  userId)

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

#### 3. Actualizar usuario 🔐

**Requiere autenticación**: Esta operación requiere el header `Authorization`
con un token Bearer válido. El ID del usuario se obtiene automáticamente del
token, por lo que no es necesario enviarlo como parámetro.

```graphql
mutation UpdateUser {
  updateUser(
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

#### 5. Eliminar usuario 🔐

**Requiere autenticación**: Esta operación requiere el header `Authorization`
con un token Bearer válido. El ID del usuario se obtiene automáticamente del
token, por lo que no es necesario enviarlo como parámetro.

```graphql
mutation DeleteUser {
  deleteUser
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

3. **Actualizar usuario (requiere token de autorización)**:

```bash
curl -X POST http://localhost:8000/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <tu_token_jwt>" \
  -d '{
    "query": "mutation { updateUser(userInput: { email: \"updated@example.com\", alias: \"UpdatedUser\" }) { id email alias } }"
  }'
```

4. **Eliminar usuario (requiere token de autorización)**:

```bash
curl -X POST http://localhost:8000/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <tu_token_jwt>" \
  -d '{
    "query": "mutation { deleteUser }"
  }'
```

### Usar GraphQL Playground

1. Navega a http://localhost:8000/graphql
2. Para operaciones que requieren autenticación, configura el header en la
   sección "HTTP Headers":
   ```json
   {
     "Authorization": "Bearer <tu_token_jwt>"
   }
   ```
3. Usa la interfaz web para escribir y ejecutar consultas
4. Explora el schema usando la documentación integrada

### Flujo completo de autenticación

1. **Crear usuario** → Obtener datos del usuario
2. **Login** → Obtener `idToken`
3. **Usar token** → Incluir en header `Authorization: Bearer <idToken>` para
   operaciones protegidas
4. **Operaciones protegidas** → Actualizar perfil, eliminar cuenta

## 🏗️ Arquitectura del Proyecto

### Capas de la Arquitectura Hexagonal

- **Dominio** (`src/domain/`): Entidades y reglas de negocio
- **Aplicación** (`src/application/`): Casos de uso y coordinación
- **Infraestructura** (`src/infraestructure/`): Implementaciones concretas

### Sistema de Autenticación

El servicio implementa un sistema de autenticación basado en headers que
incluye:

#### Context Management (`context.py`)

- **Función**: Extrae el header `Authorization` de las peticiones HTTP
- **Formato esperado**: `Authorization: Bearer <token>`
- **Procesamiento**: Separa el tipo de autorización ("Bearer") del token JWT

#### Decorador de Autorización (`decorators.py`)

- **`@login_required`**: Decorador que protege endpoints GraphQL
- **Validación**: Verifica que el header sea válido y el token esté presente
- **Verificación**: Valida el token JWT con Firebase
- **Context**: Añade el token verificado al contexto de GraphQL para uso
  posterior

#### Flujo de Autenticación

1. **Cliente** → Envía petición con header `Authorization: Bearer <token>`
2. **Context** → Extrae y procesa el header
3. **Decorador** → Valida formato y verifica token con Firebase
4. **Endpoint** → Accede al usuario autenticado desde el contexto
5. **Respuesta** → Retorna datos sin exponer información de otros usuarios

### Endpoints Protegidos

- **`updateUser`**: Actualiza el usuario autenticado (ID extraído del token)
- **`deleteUser`**: Elimina el usuario autenticado (ID extraído del token)

### Tecnologías Utilizadas

- **FastAPI**: Framework web moderno para Python
- **Strawberry GraphQL**: Librería GraphQL para Python
- **Firebase**: Backend de autenticación y base de datos
- **JWT**: Tokens de autenticación
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
│   └── infraestructure/
│       ├── db/                # Configuración Firebase
│       ├── graphql/           # Schema y tipos GraphQL
│       │   ├── context.py     # Manejo del contexto y headers de autenticación
│       │   ├── decorators.py  # Decorador @login_required para endpoints protegidos
│       │   ├── schema.py      # Definición de queries y mutations
│       │   └── types.py       # Tipos GraphQL
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
