
### 📄 1. Definición de requisitos

| ID     | REQUISITO                            | CASO DE USO   | PRIORIZACIÓN   | NOTA                                                                                            |
|--------|--------------------------------------|---------------|----------------|--------------------------------------------------------------------------------------------------|
| RF-01  | Registro inicial del usuario         | CU01          | MUST           | Es la primera acción necesaria para usar el sistema. Asegurarse que solo se permita una cuenta. |
| RF-02  | Inicio de sesión                     | CU03          | MUST           | Fundamental para el control de acceso seguro. Implementar junto con bloqueo por intentos.       |
| RF-03  | Carga de archivos                    | CU08          | MUST           | El sistema gira en torno a esta función. Validar tipos de archivo y tamaños permitidos.         |
| RF-04  | Cifrado de archivos                  | CU09          | MUST           | Debe ejecutarse automáticamente. Usar librería segura                                           |
| RF-05  | Visualización de archivos            | CU10          | MUST           | Mostrar lista ordenada y clara, permitir ordenamiento por nombre o fecha.                       |
| RF-06  | Descarga de archivos                 | CU11          | MUST           | Incluir proceso de descifrado tras autenticación activa.                                        |
| RF-07  | Eliminación de archivos              | CU12          | MUST           | Garantizar eliminación segura del archivo.                                                      |
| RF-08  | Cambio de contraseña                 | CU06          | MUST           | Validar contraseña anterior antes de permitir el cambio.                                        |
| RF-09  | Cierre de sesión                     | CU05          | MUST           | Implementar cierre automático tras inactividad como configuración opcional.                     |
| RF-10  | Eliminación de cuenta                | CU07          | SHOULD         | Confirmar con la contraseña y mostrar advertencia clara antes de borrar permanentemente.        |
| RF-11  | Registro de eventos                  | CU13          | SHOULD         | Útil para auditoría y depuración. Guardar localmente y de forma segura.                         |
| RF-12  | Prevención de múltiples registros    | CU01          | MUST           | Validar en el primer inicio del sistema si ya existe un usuario para bloquear nuevo registro.   |
| RF-13  | Reinicio del sistema                 | CU07          | COULD          | Útil para reinstalación o limpieza manual. Dejar bien documentado qué datos elimina.            |
| RNF-01 | Cifrado de archivos                  | CU09          | MUST           | Usar algoritmos robustos como AES-256 y una librería bien mantenida                             |
| RNF-02 | Almacenamiento seguro de contraseñas | CU07          | MUST           | Implementar hash con bcrypt + SHA-256. No almacenar contraseñas en texto plano.                 |
| RNF-03 | Control de acceso local              | CU01          | MUST           | El sistema debe validar siempre que el usuario esté autenticado antes de mostrar contenido.     |
| RNF-04 | Bloqueo por intentos fallidos        | CU04          | MUST           | Aplicar bloqueo temporal después de 5 intentos fallidos consecutivos.                           |
| RNF-05 | Tiempo de respuesta general          |               | SHOULD         | Asegurar que operaciones normales no excedan 5 segundos en equipos promedio.                    |
| RNF-06 | Tiempo de inicio de sesión           |               | SHOULD         | Optimizar autenticación y carga inicial para no superar los 3 segundos.                         |
| RNF-07 | Interfaz intuitiva                   |               | MUST           | Diseñar una interfaz simple usando Tkinter, sin sobrecargar de opciones técnicas.               |
| RNF-08 | Retroalimentación visual             | CU14          | SHOULD         | Cada acción debe mostrar mensajes claros de éxito, error o advertencia.                         |
| RNF-09 | Multiplataforma                      |               | COULD          | Probar funcionalidad completa en Windows, Linux y macOS con Python 3.9+.                        |
| RNF-10 | Uso de SQLite                        |               | MUST           | Base de datos local y embebida. No requerir instalación adicional.                              |
| RNF-11 | Estilo de código PEP8                |               | SHOULD         | Usar herramientas como flake8 o black para mantener el estándar.                                |
| RNF-12 | Principios de Clean Code             |               | SHOULD         | Mantener funciones cortas, nombres descriptivos y separación clara de responsabilidades.        |
| RNF-13 | Patrones de diseño                   |               | SHOULD         | Aplicar patrones Singleton (gestión de usuario) y Factory (módulos de archivos).                |
| RNF-14 | Pruebas automatizadas                |               | SHOULD         | Usar pytest o unittest para asegurar estabilidad y regresión.                                   |

---

### 📄 2. Planeación data

| REQUISITO                  | TAREA                                            |   ESTIMACION (DIAS) | INICIO              | FIN                 | RESPONSABLE                                                           | ESTADO    |
|---------------------------|--------------------------------------------------|----------------------|---------------------|---------------------|------------------------------------------------------------------------|-----------|
| Diseño de interfaz RNF-07  | Diseñar interfaz de usuario (Tkinter)            | 3                    | 2025-06-14          | 2025-06-16          | Daniel Jossa, Michel Mauricio Castañeda                               | Pendiente |
| Diseño gráfico RNF-08      | Crear íconos, paleta y estilo visual             | 2                    | 2025-06-17          | 2025-06-18          | Daniel Jossa, Michel Mauricio Castañeda                               | Pendiente |
| Base de datos RNF-10       | Diseñar y configurar SQLite                      | 3                    | 2025-06-18          | 2025-06-20          | Andres Alarcon                                                        | Pendiente |
| Arquitectura RNF-13        | Definir estructura y arquitectura base           | 3                    | 2025-06-20          | 2025-06-22          | Andres Alarcon                                                        | Pendiente |
| Backend RF-01,02,09,12     | Registro e inicio/cierre de sesión               | 4                    | 2025-06-22          | 2025-06-25          | Jaime Angulo, Andres Alarcon                                          | Pendiente |
| Backend RNF-02,03,04       | Control de sesión, bloqueo y hash de contraseñas | 3                    | 2025-06-26          | 2025-06-28          | Jaime Angulo                                                          | Pendiente |
| Frontend RF-03             | Carga de archivos y validación                   | 2                    | 2025-06-29          | 2025-06-30          | Daniel Jossa, Michel Mauricio Castañeda                               | Pendiente |
| Backend RF-04, RFN-01      | Cifrado automático de archivos                   | 2                    | 2025-07-01          | 2025-07-02          | Andres Alarcon                                                        | Pendiente |
| Frontend RF-05             | Visualización de archivos                        | 2                    | 2025-07-03          | 2025-07-04          | Daniel Jossa, Michel Mauricio Castañeda                               | Pendiente |
| Backend RF-11              | Registro de eventos del sistema                  | 1                    | 2025-07-05          | 2025-07-05          | Jaime Angulo                                                          | Pendiente |
| Frontend RF-06             | Descarga y descifrado de archivos                | 3                    | 2025-07-06          | 2025-07-07          | Daniel Jossa, Michel Mauricio Castañeda                               | Pendiente |
| Frontend RF-07             | Eliminación de archivos                          | 1                    | 2025-07-08          | 2025-07-08          | Daniel Jossa, Michel Mauricio Castañeda                               | Pendiente |
| Backend RF-08              | Cambio de contraseña                             | 1                    | 2025-07-09          | 2025-07-09          | Jaime Angulo, Andres Alarcon                                          | Pendiente |
| Backend RF-10,13           | Eliminar Cuenta y reiniciar sistema              | 2                    | 2025-07-10          | 2025-07-11          | Andres Alarcon, Jaime Angulo                                          | Pendiente |
| Integración                | Integrar Frontend, Backend y base de datos       | 2                    | 2025-07-11          | 2025-07-12          | Todo el equipo                                                        | Pendiente |
| Testing RNF-14             | Pruebas Unitarias y automatizadas                | 2                    | 2025-07-13          | 2025-07-14          | Todo el equipo                                                        | Pendiente |
| Revisión QA RNF-09         | Revisión final de calidad y multiplataforma      | 2                    | 2025-07-15          | 2025-07-16          | Todo el equipo                                                        | Pendiente |
| Documentación              | Redactar manual técnico y de usuario             | 2                    | 2025-07-17          | 2025-07-18          | Andres Alarcon                                                        | Pendiente |
| Código limpio RNF-11,12,13 | Aplicar PEP8, Clean Code, patrones               | 2                    | 2025-07-19          | 2025-07-20          | Todo el equipo                                                        | Pendiente |
