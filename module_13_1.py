import asyncio


async def start_strongman(name: str, power: int):
    print(f'Силач {name} начал соревнования')
    for i in range(5):
        await asyncio.sleep(10 - power)
        print(f'Силач {name} поднял {i+1} шар')
    print(f'Силач {name} окончил соревнования')


async def start_tournament():
    # для более быстрого прохода циклов можно Антохе силу до 3-4 поднять
    strongman1 = asyncio.create_task(start_strongman('Антоха aka Кирпич', 2))
    strongman2 = asyncio.create_task(start_strongman('Михаил Кокляев', 5))
    strongman3 = asyncio.create_task(start_strongman('Цирковой Слон', 7))
    await strongman1
    await strongman2
    await strongman3


if __name__ == "__main__":
    asyncio.run(start_tournament())
