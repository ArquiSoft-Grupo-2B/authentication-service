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
- **Refresh tokens**: Renovación automática de tokens de acceso sin requerir
  reautenticación
- **Recuperación de contraseña**: Envío de emails para restablecer contraseña
- **Backend Firebase**: Integración completa con Firebase Authentication y
  Firestore
- **Autorización por Header**: Sistema de autenticación mediante header
  `Authorization` con tokens Bearer

### Arquitectura

```
src/
├── domain/           # Entidades de dominio y repositorios abstractos
├── application/      # Casos de uso y lógica de aplicación
├── infrastructure/   # Implementaciones concretas (Firebase, BD, etc.)
├── interface/        # Interfaces de entrada (GraphQL)
└── adapters/         # Adaptadores externos (Firebase Auth API)
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
4. Coloca el archivo en la carpeta `creds/` de tu proyecto: (Si decides cambiar la posición, también es necesario modificar los volumenes en `docker-compose` y `k8s/auth-deployment`)
5. Configura las variables de entorno en `.env` (en la raíz del proyecto):

```env
FIREBASE_CREDENTIALS_JSON=RUTA/A/JSON
API_KEY='tu_api_key_de_firebase'
```

## 🏃‍♂️ Ejecución Local

### Opción 1: Con uvicorn (Desarrollo)

1. **Instalar dependencias**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Configurar variables de entorno**:
   
   Asegúrate de que el archivo `.env` esté en la raíz del proyecto con las variables necesarias.

3. **Ejecutar el servidor**:

   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Acceder al servicio**:
   - API: http://localhost:8000
   - GraphQL Playground: http://localhost:8000/graphql

### Opción 2: Con Docker Compose

Antes de iniciar, asegúrate de tener instalado:

- [Docker](https://docs.docker.com/get-docker/)  
- [Docker Compose](https://docs.docker.com/compose/)  
- Una red Docker compartida llamada `routes_shared_network`

Si no existe la red, créala con:

```bash
docker network create routes_shared_network
```

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

#### 7. Renovar token de acceso

```graphql
mutation RefreshToken {
  refreshToken(refreshToken: "refresh_token_aqui") {
    accessToken
    expiresIn
    tokenType
    refreshToken
    idToken
    userId
    projectId
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

5. **Renovar token de acceso**:

```bash
curl -X POST http://localhost:8000/graphql \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation { refreshToken(refreshToken: \"<tu_refresh_token>\") { idToken accessToken expiresIn refreshToken } }"
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
2. **Login** → Obtener `idToken` y `refreshToken`
3. **Usar token** → Incluir en header `Authorization: Bearer <idToken>` para
   operaciones protegidas
4. **Token expirado** → Usar `refreshToken` para obtener nuevo `idToken` sin
   reautenticación
5. **Operaciones protegidas** → Actualizar perfil, eliminar cuenta

### Gestión de tokens

- **idToken**: Token de acceso con tiempo de vida limitado (1 hora)
- **refreshToken**: Token de larga duración para renovar el `idToken`
- **Flujo de renovación**: Cuando el `idToken` expira, usa el `refreshToken`
  para obtener uno nuevo sin requerir login

## 🧪 Testing

El proyecto incluye una suite completa de pruebas unitarias e integración:

### Ejecutar todas las pruebas

```bash
python -m pytest
```

### Ejecutar pruebas con cobertura

```bash
python -m pytest --cov=src --cov-report=html
```

### Ejecutar pruebas específicas

```bash
# Pruebas de dominio
python -m pytest tests/domain/

# Pruebas de aplicación  
python -m pytest tests/application/

# Pruebas de integración
python -m pytest tests/integration/
```

### Estructura de Testing

- **`tests/domain/`**: Pruebas unitarias de entidades y validaciones
- **`tests/application/`**: Pruebas de casos de uso y lógica de aplicación
- **`tests/integration/`**: Pruebas de integración con Firebase y servicios externos

### Características de Testing

- **Mocking**: Uso de mocks para aislar unidades de código
- **Fixtures**: Configuración reutilizable de datos de prueba
- **Cobertura**: Medición de cobertura de código
- **Validaciones**: Pruebas exhaustivas de métodos de validación estáticos

## 🏗️ Arquitectura del Proyecto

### Capas de la Arquitectura Hexagonal

- **Dominio** (`src/domain/`): Entidades y reglas de negocio, repositorios abstractos
- **Aplicación** (`src/application/`): Casos de uso y coordinación entre capas
- **Infraestructura** (`src/infrastructure/`): Implementaciones concretas de repositorios y BD
- **Interface** (`src/interface/`): Interfaces de entrada (GraphQL schema, context, decorators)
- **Adaptadores** (`src/adapters/`): Adaptadores para servicios externos (Firebase Auth API)

### Sistema de Autenticación

El servicio implementa un sistema de autenticación basado en headers que
incluye:

#### Context Management (`src/interface/graphql/context.py`)

- **Función**: Extrae el header `Authorization` de las peticiones HTTP
- **Formato esperado**: `Authorization: Bearer <token>`
- **Procesamiento**: Separa el tipo de autorización ("Bearer") del token JWT

#### Decorador de Autorización (`src/interface/graphql/decorators.py`)

- **`@login_required`**: Decorador que protege endpoints GraphQL
- **Validación**: Verifica que el header sea válido y el token esté presente
- **Verificación**: Valida el token JWT con Firebase
- **Context**: Añade el token verificado al contexto de GraphQL para uso
  posterior

#### Adaptadores Externos (`src/adapters/`)

- **Firebase Adapter**: Manejo de la conexión y configuración con Firebase
- **Firebase Auth API**: Interacción directa con la API REST de Firebase Auth para operaciones como login, refresh tokens, y password reset

#### Validaciones de Dominio

Las entidades del dominio implementan métodos de validación estáticos que pueden utilizarse sin instanciar objetos:

- **`User.validate_email(email: str)`**: Valida formato de email
- **`User.validate_password(password: str)`**: Valida contraseña (mínimo 8 caracteres)  
- **`User.validate_alias(alias: str)`**: Valida alias (3-30 caracteres)

Además, la entidad User incluye métodos de validación específicos para diferentes contextos:

- **`validate_user_complete()`**: Validación completa (email, password, alias)
- **`validate_user_login()`**: Validación para login (email, password)
- **`validate_user_no_password()`**: Validación excluyendo password (email, alias)

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
│   │   ├── entities/          
│   │   └── repositories/      
│   ├── application/
│   │   ├── user_use_cases.py  
│   │   └── token_use_cases.py 
│   ├── infrastructure/
│   │   ├── db/                
│   │   ├── repositories/      
│   │   └── rest/              
│   ├── interface/
│   │   └── graphql/           
│   │       ├── context.py     
│   │       ├── decorators.py  
│   │       ├── schema.py      
│   │       └── types.py       
│   └── adapters/
│       └── firebase_adapter.py 
├── tests/                     
│   ├── domain/               
│   ├── application/          
│   └── integration/          
├── k8s/                       # Carpeta nueva para Kubernetes
│   ├── auth_deployment.yaml
│   └── auth_service.yaml
├── creds/                     # Carpeta de credenciales (preferible)
│   └── firebase_credentials.json
├── .env                      
├── main.py                   
├── requirements.txt          
├── Dockerfile               
└── docker-compose.yml        
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
