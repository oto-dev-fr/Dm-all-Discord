import discord
import sys
import logging
from colorama import Fore, Style, init
import asyncio

# Initialisation de colorama
init(autoreset=True)

# Classe pour les couleurs
class color:
    RED = Fore.RED + Style.BRIGHT
    GREEN = Fore.GREEN
    WHITE = Fore.WHITE + Style.BRIGHT
    RESET = Style.RESET_ALL

# Configuration du logging
logging.basicConfig(level=logging.CRITICAL, format='%(asctime)s - %(levelname)s - %(message)s')

# Désactiver le logging de discord.py
discord.utils.setup_logging(level=logging.CRITICAL)

# Définition des intentions du bot
intents = discord.Intents.default()
intents.members = True

# Classe pour le client du bot Discord
class BotClient(discord.Client):
    def __init__(self, token, server_id=None, message=None, *args, **kwargs):
        super().__init__(intents=intents, *args, **kwargs)
        self.token = token
        self.server_id = server_id
        self.message = message
        self.sent_count = 0  # Compteur de messages envoyés

    async def on_ready(self):
        print(f'[{self.user.name}] est connecté avec succès.')

        if self.server_id:
            guild = discord.utils.get(self.guilds, id=self.server_id)
            if guild:
                for member in guild.members:
                    if member.id != self.user.id:
                        try:
                            dm_channel = await member.create_dm()
                            await dm_channel.send(self.message)
                            self.sent_count += 1
                            print(f'Message envoyé à {member.display_name}.')
                        except Exception:
                            # Ignorer les erreurs pour garder le terminal propre
                            continue
                print(f"Total de messages envoyés : {self.sent_count}")
            else:
                print(f'Impossible de trouver le serveur avec l\'ID {self.server_id}.')
        else:
            print("Server ID non fourni pour l'option 1.")

        await self.close()

# Fonction principale pour exécuter le bot
async def main():
    while True:
        token = input(f"{color.GREEN}[!] {color.WHITE}Entrez le token de votre bot Discord : {color.RESET}").strip()
        if not token:
            print(f"{color.RED}[!] {color.WHITE}Réponse invalide. Le token ne peut pas être vide.{color.RESET}")
            continue
        
        server_id_input = input(f"{color.GREEN}[!] {color.WHITE}Entrez l'ID du serveur : {color.RESET}").strip()
        if not server_id_input.isdigit():
            print(f"{color.RED}[!] {color.WHITE}Réponse invalide. L'ID du serveur doit être un nombre entier.{color.RESET}")
            continue
        server_id = int(server_id_input)

        message = input(f"{color.GREEN}[!] {color.WHITE}Entrez le message à envoyer : {color.RESET}").strip()
        if not message:
            print(f"{color.RED}[!] {color.WHITE}Réponse invalide. Le message ne peut pas être vide.{color.RESET}")
            continue

        # Vérifier la validité du token en essayant de se connecter
        client = BotClient(token=token, server_id=server_id, message=message)
        try:
            # Tentative de connexion pour vérifier le token
            await client.start(token)
            break  # Quitte la boucle si tout est valide
        except discord.LoginFailure:
            print(f"{color.RED}[!] {color.WHITE}Le token n'est pas valide.{color.RESET}")
        except discord.HTTPException:
            print(f"{color.RED}[!] {color.WHITE}L'ID du serveur est invalide ou le bot ne peut pas accéder au serveur.{color.RESET}")
        except Exception:
            print(f"{color.RED}[!] {color.WHITE}Une erreur est survenue.{color.RESET}")
        finally:
            await client.close()

    # Attendre que l'utilisateur appuie sur Entrée pour fermer le terminal
    input(f"{color.GREEN}[!] {color.WHITE}Appuyez sur ENTER pour quitter...{color.RESET}")

# Affichage du titre
title = color.RED + '''
▓█████▄  ███▄ ▄███▓    ▄▄▄       ██▓     ██▓    
▒██▀ ██▌▓██▒▀█▀ ██▒   ▒████▄    ▓██▒    ▓██▒    
░██   █▌▓██    ▓██░   ▒██  ▀█▄  ▒██░    ▒██░    
░▓█▄   ▌▒██    ▒██    ░██▄▄▄▄██ ▒██░    ▒██░    
░▒████▓ ▒██▒   ░██▒    ▓█   ▓██▒░██████▒░██████▒
 ▒▒▓  ▒ ░ ▒░   ░  ░    ▒▒   ▓▒█░░ ▒░▓  ░░ ▒░▓  ░
 ░ ▒  ▒ ░  ░      ░     ▒   ▒▒ ░░ ░ ▒  ░░ ░ ▒  ░
 ░ ░  ░ ░      ░        ░   ▒     ░ ░     ░ ░   
   ░           ░            ░  ░    ░  ░    ░  ░
 ░                                              
''' + color.WHITE + "fully coded by oto.dev" + color.RESET  
print (title)  

if __name__ == '__main__':
    asyncio.run(main())