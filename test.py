import nest_asyncio
import asyncio
from SQLite import create_table,  update_quiz_score, get_quiz_score
nest_asyncio.apply()


async def main():
    await create_table()
    await update_quiz_score(892087118, 5)
    a = await get_quiz_score(892087118)
    print(a)



if __name__ == "__main__":
    asyncio.run(main())