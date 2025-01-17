import asyncio

async def start_client(host='127.0.0.1', port=65432):
    reader, writer = await asyncio.open_connection(host, port)
    print(f"Соединение с сервером {host}:{port} установлено.")

    try:
        while True:
            message = input("Введите сообщение (или 'exit' для выхода): ")
            writer.write(message.encode('utf-8'))
            await writer.drain()
            print(f"Отправлено серверу: {message}")

            if message.lower() == 'exit':
                print("Разрыв соединения с сервером...")
                break

            data = await reader.read(1024)
            print(f"Ответ от сервера: {data.decode('utf-8')}")
    except KeyboardInterrupt:
        print("\nПринудительный разрыв соединения.")
    finally:
        writer.close()
        await writer.wait_closed()
        print("Клиент завершил работу.")

if __name__ == "__main__":
    asyncio.run(start_client())
