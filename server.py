import asyncio

async def handle_client(reader, writer):
    address = writer.get_extra_info('peername')
    print(f"Клиент подключился: {address}")

    try:
        while True:
            data = await reader.read(1024)
            if not data:
                print(f"Клиент отключился: {address}")
                break

            message = data.decode('utf-8').strip()
            print(f"Получено от клиента: {message}")
            writer.write(data)
            await writer.drain()
            print(f"Отправлено клиенту: {message}")
    except Exception as e:
        print(f"Ошибка с клиентом {address}: {e}")
    finally:
        writer.close()
        await writer.wait_closed()

async def start_server(host='127.0.0.1', port=65432):
    server = await asyncio.start_server(handle_client, host, port)
    print(f"Сервер запущен на {host}:{port}")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    try:
        asyncio.run(start_server())
    except KeyboardInterrupt:
        print("\nСервер остановлен.")
