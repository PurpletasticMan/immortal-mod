# Immortal & Godly (Fabric, Minecraft 26.3)

Tiers (weakest to strongest): Galaxy (blue starfield) < Purple Hero armour < Immortal (purple galaxy) < Godly (white/heavenly).

Build: push this folder to a GitHub repo. The included workflow builds it, and the jar appears under
Actions > latest run > Artifacts. Use the jar that does NOT end in `-sources`. Needs Fabric API.

## Recipes
- Golden food: 8 gold nuggets around the cooked item (steak, porkchop, chicken, mutton, rabbit, cod, salmon, baked potato, bread)
- Galaxy Ingot: diamond centre, lapis blocks N/S/E/W, amethyst blocks in the corners. Galaxy tools/armour use vanilla shapes with sticks
- Immortal Ingot: nether star centre, galaxy ingots N/S/E/W, netherite ingots in the corners
- Godly Ingot: nether star centre, enchanted golden apples N/S/E/W, immortal ingots in the corners
- Immortal/Godly tools + armour: normal vanilla shapes using the ingot (stick = blaze rod / end rod)
- Spears: ingot at the tip, two rods on the diagonal
- Bedrock Pickaxe: netherite pickaxe centre, netherite ingots N/S/E/W, obsidian corners
- Immortal Ender Pearl: 8 ender pearls around an immortal ingot. Godly: 8 ender eyes around a godly ingot
- Immortal Totem: totem of undying centre, immortal ingots N/S/E/W, gold blocks in the corners
- Godly Totem: immortal totem centre, godly ingots N/S/E/W, emerald blocks in the corners
- Heart: golden apple centre, redstone blocks N/S/E/W, diamonds in the corners
- Immortal Heart: immortal ingot centre, 4 hearts, 4 gold blocks. Godly Heart: godly ingot centre, 4 immortal hearts, 4 emerald blocks
- Immortal Apple: enchanted golden apple + immortal ingot. Godly Apple: immortal apple + godly ingot
- Purple Hero armour: amethyst shards in the vanilla armour shapes
- Sword blocks (stonecutter): iron/diamond/netherite block, immortal ingot, godly ingot -> matching sword block

Everything is also in the "Immortal & Godly" creative tab.

## Using it in the Modrinth App
1. Create an instance: Fabric, Minecraft 26.3.
2. In the instance, Add content > search Fabric API > install.
3. Drag the built jar (build/libs/immortal-1.0.0.jar, not the -sources one) onto the instance, or Add content > Add from file.
