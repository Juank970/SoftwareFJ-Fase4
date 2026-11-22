"""
Sistema Integral de Gestión de Clientes, Servicios y Reservas
Empresa: Software FJ
Curso: Programación 213023 - Fase 4
Estudiante: Juan Camilo Alzate Díaz
Grupo: 141
Tutor: Johnny Alirio Blanquicett Cardona

Incluye:
- Abstracción, herencia, polimorfismo y encapsulación
- Manejo avanzado de excepciones (personalizadas, try/except/else/finally, chaining)
- Sin bases de datos (listas + archivo de logs)
- Simulación de más de 10 operaciones válidas e inválidas
"""

from abc import ABC, abstractmethod
from datetime import datetime
import os

# ==================== EXCEPCIONES PERSONALIZADAS ====================
class FalloSistema(Exception):
    """Excepción base del sistema."""
    pass

class FalloValidacion(FalloSistema):
    pass

class FalloCliente(FalloValidacion):
    pass

class FalloServicio(FalloValidacion):
    pass

class FalloReserva(FalloValidacion):
    pass


# ==================== CLASE ABSTRACTA ====================
class EntidadSistema(ABC):
    """Clase abstracta que representa entidades generales."""

    @abstractmethod
    def comprobar(self):
        pass

    @abstractmethod
    def resumen(self):
        pass


# ==================== CLASE CLIENTE ====================
class Cliente(EntidadSistema):
    def __init__(self, nombre, numero_documento, celular="", correo_electronico=""):
        self._nombre = ""
        self._numero_documento = ""
        self._celular = ""
        self._correo_electronico = ""
        self.nombre = nombre
        self.numero_documento = numero_documento
        self.celular = celular
        self.correo_electronico = correo_electronico
        self.comprobar()

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or len(str(valor).strip()) < 3:
            raise FalloCliente("El nombre debe contener al menos 3 caracteres.")
        self._nombre = str(valor).strip().title()

    @property
    def numero_documento(self):
        return self._numero_documento

    @numero_documento.setter
    def numero_documento(self, valor):
        valor = str(valor).strip()
        if not valor.isdigit() or len(valor) < 6:
            raise FalloCliente("El número de documento debe ser numérico y de mínimo 6 dígitos.")
        self._numero_documento = valor

    @property
    def celular(self):
        return self._celular

    @celular.setter
    def celular(self, valor):
        if valor and (not str(valor).isdigit() or len(str(valor)) < 7):
            raise FalloCliente("El celular debe ser numérico y tener al menos 7 dígitos.")
        self._celular = str(valor).strip() if valor else ""

    @property
    def correo_electronico(self):
        return self._correo_electronico

    @correo_electronico.setter
    def correo_electronico(self, valor):
        if valor and ("@" not in valor or "." not in valor):
            raise FalloCliente("El correo electrónico tiene un formato incorrecto.")
        self._correo_electronico = str(valor).strip().lower() if valor else ""

    def comprobar(self):
        if not self.nombre or not self.numero_documento:
            raise FalloCliente("Nombre y número de documento son obligatorios.")

    def resumen(self):
        return f"{self.nombre} - Documento: {self.numero_documento}"


# ==================== CLASE ABSTRACTA SERVICIO ====================
class Servicio(EntidadSistema, ABC):
    def __init__(self, nombre_servicio, valor_base, habilitado=True):
        self.nombre_servicio = nombre_servicio
        self.valor_base = float(valor_base)
        self.habilitado = habilitado

    @abstractmethod
    def obtener_costo(self, cantidad=1, iva=0.19, porcentaje_descuento=0.0):
        """Cálculo de costo con parámetros opcionales."""
        pass

    @abstractmethod
    def detalle(self):
        pass

    def comprobar(self):
        if self.valor_base <= 0:
            raise FalloServicio(f"El valor base de '{self.nombre_servicio}' debe ser positivo.")
        if not self.habilitado:
            raise FalloServicio(f"El servicio '{self.nombre_servicio}' no está habilitado.")

    def resumen(self):
        return self.detalle()


# ==================== SERVICIOS CONCRETOS ====================
class ReservaSala(Servicio):
    def obtener_costo(self, cantidad=1, iva=0.19, porcentaje_descuento=0.0):
        self.comprobar()
        if cantidad <= 0:
            raise FalloReserva("La cantidad debe ser mayor que cero.")
        subtotal = self.valor_base * cantidad
        con_descuento = subtotal * (1 - porcentaje_descuento / 100)
        return round(con_descuento * (1 + iva), 2)

    def detalle(self):
        return f"Reserva de Sala | Valor/hora: ${self.valor_base:.2f} | Habilitado: {self.habilitado}"


class AlquilerEquipo(Servicio):
    def obtener_costo(self, cantidad=1, iva=0.19, porcentaje_descuento=0.0):
        self.comprobar()
        if cantidad <= 0:
            raise FalloReserva("La cantidad debe ser mayor que cero.")
        subtotal = self.valor_base * cantidad
        con_descuento = subtotal * (1 - porcentaje_descuento / 100)
        return round(con_descuento * (1 + iva), 2)

    def detalle(self):
        return f"Alquiler de Equipo | Valor/día: ${self.valor_base:.2f} | Habilitado: {self.habilitado}"


class AsesoriaEspecializada(Servicio):
    def obtener_costo(self, cantidad=1, iva=0.19, porcentaje_descuento=0.0):
        self.comprobar()
        if cantidad <= 0:
            raise FalloReserva("La cantidad debe ser mayor que cero.")
        subtotal = self.valor_base * cantidad
        con_descuento = subtotal * (1 - porcentaje_descuento / 100)
        return round(con_descuento * (1 + iva), 2)

    def detalle(self):
        return f"Asesoría Especializada | Valor/hora: ${self.valor_base:.2f} | Habilitado: {self.habilitado}"


# ==================== CLASE RESERVA ====================
class Reserva:
    def __init__(self, cliente, servicio, cantidad, estado="Pendiente"):
        self.cliente = cliente
        self.servicio = servicio
        self.cantidad = cantidad
        self.estado = estado
        self.costo_total = 0.0
        self.fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M")

    def confirmar(self, iva=0.19, porcentaje_descuento=0.0):
        try:
            self.costo_total = self.servicio.obtener_costo(self.cantidad, iva, porcentaje_descuento)
            self.estado = "Confirmada"
            return True
        except Exception as err:
            raise FalloReserva(f"Error al confirmar la reserva: {err}") from err

    def cancelar(self):
        if self.estado in ("Cancelada", "Procesada"):
            raise FalloReserva("No es posible cancelar la reserva en el estado actual.")
        self.estado = "Cancelada"
        return True

    def procesar(self):
        if self.estado != "Confirmada":
            raise FalloReserva("Únicamente se pueden procesar reservas confirmadas.")
        self.estado = "Procesada"
        return True


# ==================== SISTEMA PRINCIPAL ====================
class PlataformaFJ:
    def __init__(self):
        self.registro_clientes = []
        self.registro_servicios = []
        self.registro_reservas = []
        self.archivo_logs = "registro_eventos.log"
        self._iniciar_archivo_log()

    def _iniciar_archivo_log(self):
        with open(self.archivo_logs, "a", encoding="utf-8") as archivo:
            archivo.write(f"\n===== NUEVA SESIÓN: {datetime.now()} =====\n")

    def escribir_log(self, mensaje, error=False):
        nivel = "ERROR" if error else "INFO"
        texto = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [{nivel}] {mensaje}"
        with open(self.archivo_logs, "a", encoding="utf-8") as archivo:
            archivo.write(texto + "\n")
        print(texto)

    def inscribir_cliente(self, nombre, documento, celular="", correo=""):
        try:
            cliente = Cliente(nombre, documento, celular, correo)
            self.registro_clientes.append(cliente)
            self.escribir_log(f"Cliente inscrito: {cliente.resumen()}")
            return cliente
        except Exception as e:
            self.escribir_log(f"Error al inscribir cliente: {e}", error=True)
            raise

    def registrar_servicio(self, tipo, nombre, valor, habilitado=True):
        try:
            tipo = tipo.lower().strip()
            if tipo == "sala":
                servicio = ReservaSala(nombre, valor, habilitado)
            elif tipo == "equipo":
                servicio = AlquilerEquipo(nombre, valor, habilitado)
            elif tipo == "asesoria":
                servicio = AsesoriaEspecializada(nombre, valor, habilitado)
            else:
                raise FalloServicio("Tipo de servicio no válido.")
            servicio.comprobar()
            self.registro_servicios.append(servicio)
            self.escribir_log(f"Servicio registrado: {servicio.detalle()}")
            return servicio
        except Exception as e:
            self.escribir_log(f"Error al registrar servicio: {e}", error=True)
            raise

    def generar_reserva(self, documento, nombre_servicio, cantidad, descuento=0.0):
        try:
            cliente = next((c for c in self.registro_clientes if c.numero_documento == str(documento)), None)
            if not cliente:
                raise FalloReserva("Cliente no encontrado.")

            servicio = next((s for s in self.registro_servicios if s.nombre_servicio.lower() == nombre_servicio.lower()), None)
            if not servicio:
                raise FalloServicio("Servicio no encontrado.")

            reserva = Reserva(cliente, servicio, cantidad)
            reserva.confirmar(porcentaje_descuento=descuento)
            self.registro_reservas.append(reserva)
            self.escribir_log(f"Reserva generada: {cliente.nombre} → {servicio.nombre_servicio} | Costo: ${reserva.costo_total}")
            return reserva
        except Exception as e:
            self.escribir_log(f"Error al generar reserva: {e}", error=True)
            raise

    def mostrar_todo(self):
        print("\n========== INFORMACIÓN DEL SISTEMA ==========")
        print("CLIENTES:")
        for c in self.registro_clientes:
            print(f"  - {c.resumen()}")
        print("\nSERVICIOS:")
        for s in self.registro_servicios:
            print(f"  - {s.detalle()}")
        print("\nRESERVAS:")
        for r in self.registro_reservas:
            print(f"  - {r.cliente.nombre} | {r.servicio.nombre_servicio} | {r.cantidad} | ${r.costo_total} | {r.estado}")


# ==================== SIMULACIÓN ====================
def simular_operaciones():
    plataforma = PlataformaFJ()
    print("=== SIMULACIÓN DE OPERACIONES ===\n")

    pruebas = [
        ("Inscripción cliente válida", lambda: plataforma.inscribir_cliente("Mariana Torres", "1034567890", "3151234567", "mariana@correo.com")),
        ("Nombre muy corto", lambda: plataforma.inscribir_cliente("Jo", "123456")),
        ("Documento no numérico", lambda: plataforma.inscribir_cliente("Carlos Pérez", "ABC123")),
        ("Servicio sala válido", lambda: plataforma.registrar_servicio("sala", "Sala Conferencias", 85.0)),
        ("Servicio equipo válido", lambda: plataforma.registrar_servicio("equipo", "Laptop Profesional", 40.0)),
        ("Servicio asesoría válida", lambda: plataforma.registrar_servicio("asesoria", "Mentoría en Python", 160.0)),
        ("Valor base inválido", lambda: plataforma.registrar_servicio("sala", "Sala Pequeña", -5)),
        ("Reserva exitosa", lambda: plataforma.generar_reserva("1034567890", "Sala Conferencias", 2, descuento=8)),
        ("Cliente no existente", lambda: plataforma.generar_reserva("000000", "Laptop Profesional", 1)),
        ("Servicio no existente", lambda: plataforma.generar_reserva("1034567890", "Servicio Inexistente", 3)),
        ("Cantidad inválida", lambda: plataforma.generar_reserva("1034567890", "Mentoría en Python", 0)),
    ]

    for i, (descripcion, accion) in enumerate(pruebas, 1):
        print(f"\n--- Prueba {i}: {descripcion} ---")
        try:
            accion()
            print("✓ Correcto")
        except Exception as e:
            print(f"✗ Error controlado: {e}")
        else:
            print("→ (else) Sin errores")
        finally:
            print("→ (finally) Prueba finalizada")

    print("\n" + "="*60)
    plataforma.mostrar_todo()
    print(f"\nArchivo de logs: {os.path.abspath(plataforma.archivo_logs)}")


# ==================== MENÚ ====================
def menu():
    plataforma = PlataformaFJ()
    while True:
        print("\n" + "="*55)
        print("  PLATAFORMA SOFTWARE FJ - Gestión de Reservas")
        print("="*55)
        print("1. Inscribir cliente")
        print("2. Registrar servicio")
        print("3. Generar reserva")
        print("4. Mostrar información")
        print("5. Ejecutar simulación")
        print("0. Salir")
        op = input("\nOpción: ").strip()

        try:
            if op == "1":
                n = input("Nombre: ")
                d = input("Número de documento: ")
                c = input("Celular (opcional): ")
                e = input("Correo (opcional): ")
                plataforma.inscribir_cliente(n, d, c, e)
            elif op == "2":
                t = input("Tipo (sala/equipo/asesoria): ")
                n = input("Nombre del servicio: ")
                v = float(input("Valor base: "))
                plataforma.registrar_servicio(t, n, v)
            elif op == "3":
                d = input("Documento del cliente: ")
                n = input("Nombre del servicio: ")
                c = int(input("Cantidad: "))
                plataforma.generar_reserva(d, n, c)
            elif op == "4":
                plataforma.mostrar_todo()
            elif op == "5":
                simular_operaciones()
            elif op == "0":
                print("Saliendo del sistema...")
                break
            else:
                print("Opción no válida.")
        except Exception as e:
            print(f"Error controlado: {e}")


if __name__ == "__main__":
    menu()
