import asyncio
import pygame
from game import Game

async def main():
    game = Game()
    await game.main()

if __name__ == "__main__":
    asyncio.run(main())