import asyncio
from collections.abc import Callable


async def worker(
    name: str,
    # client: SolscanClient,
    function: Callable,
    queue: asyncio.Queue,
    results: list,
    max_retries: int = 1,
):
    """
    Worker que procesa tareas desde una cola asíncrona.
    Args:
        name (str): Nombre del worker (usado para logging).
        function (Callable): Función asíncrona a llamar con los argumentos de la tarea.
        queue (asyncio.Queue): Cola asíncrona de tareas a procesar.
        results (list): Lista donde almacenar los resultados exitosos.
        max_retries (int): Número máximo de reintentos por tarea en caso de fallo.
    Ejemplo de uso:
        ```python
        import asyncio
        from soltradepy.infrastructure.http.worker import worker
        async def sample_function(address):
            # Simula una llamada asíncrona
            await asyncio.sleep(1)
            return f"Data for {address}"
        async def main():
            queue = asyncio.Queue()
            results = []
            await queue.put(({"address": "addr1"}, 0))
            await worker("Worker1", sample_function, queue, results, max_retries=2)
            print(results)
        asyncio.run(main())
        ```
    Descripción:
    Este worker toma tareas de una cola asíncrona, llama a una función asíncrona con los argumentos de la tarea,
    maneja errores y reintentos, y almacena los resultados exitosos en una lista compartida.
    """
    while True:
        try:
            kwargs, attempts = queue.get_nowait()  # (kwargs, attempts_used)
        except asyncio.QueueEmpty:
            return  # ya no hay trabajo

        try:
            # res = await client.fake_request(address)
            await asyncio.sleep(5)
            res = await function(**kwargs)
        except Exception as e:
            # registrar error del cliente y decidir qué hacer con la address
            print(f"❌ Error en {name}: {e}")

            # si no hemos alcanzado max_retries, reencolamos con attempts+1
            if attempts < max_retries:
                await queue.put((kwargs, attempts + 1))
                print(f"  ↩ Reencolada {kwargs} (intento {attempts + 1})")
            else:
                print(f"  ⚠ Descartando {kwargs} tras {attempts} intentos")

            # terminamos el worker para "eliminar" el cliente de la rotación
            return
        else:
            # éxito -> almacenar resultado
            print(f"✅ Éxito en {name}: {res}")
            results.append((kwargs, name, res))
        finally:
            queue.task_done()


async def monitor_workers(tasks, queue):
    while True:
        await asyncio.sleep(1)
        if queue.empty() and not tasks:
            break
        # Filtrar workers activos
        tasks = [t for t in tasks if not t.done()]
        # Si NO hay workers activos pero sí hay trabajo en cola:
        if not tasks and not queue.empty():
            pending_items = []
            while not queue.empty():
                pending_items.append(await queue.get())
                queue.task_done()

            print("⚠️ Todos los workers fallaron. No queda nadie para procesar la cola.")
            print(f"❌ Quedaron {len(pending_items)} direcciones sin procesar.")
            break
    return tasks
