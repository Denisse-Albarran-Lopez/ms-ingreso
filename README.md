# MS-Ingreso - Microservicio de Autenticación

Microservicio para manejo de autenticación de usuarios del sistema CaFES Check.

## Características

- Registro e inicio de sesión para usuarios UNAM y externos
- Autenticación con Google OAuth
- Validación de correos institucionales UNAM
- Almacenamiento en archivo de texto
- API REST compatible con FastAPI

## Endpoints Disponibles

### Autenticación Básica
- `POST /auth/login` - Iniciar sesión
- `POST /auth/register/unam` - Registro para comunidad UNAM
- `POST /auth/register/externo` - Registro para usuarios externos

### Autenticación con Google
- `POST /auth/google/unam` - Autenticación Google para comunidad UNAM
- `POST /auth/google/externo` - Autenticación Google para usuarios externos

## Instalación

1. Ejecutar `instalar_dependencias.bat` o:
   ```bash
   pip install -r requirements.txt
   ```

2. Ejecutar el servidor:
   ```bash
   python run.py
   ```

3. El servidor estará disponible en `http://localhost:8000`

## Configuración Google OAuth

Para habilitar la autenticación con Google:

1. Crear proyecto en Google Cloud Console
2. Habilitar Google+ API
3. Crear credenciales OAuth 2.0
4. Configurar variables de entorno:
   ```
   GOOGLE_CLIENT_ID=tu_client_id
   GOOGLE_CLIENT_SECRET=tu_client_secret
   ```

## Estructura de Datos

Los usuarios se almacenan en formato JSON en el archivo `usuarios.txt`:

```json
{
  "id": 1,
  "correo": "usuario@comunidad.unam.mx",
  "contrasena_hash": "hash_bcrypt",
  "tipo_usuario": "unam",
  "fecha_registro": "2024-01-01T00:00:00",
  "verificado": true,
  "oauth_provider": "google"
}
```
