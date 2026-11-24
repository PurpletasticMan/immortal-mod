"""Writes the whole Immortal & Godly mod source tree (Java + generated textures, models, recipes, tags, lang).
Run from the repo root:  python3 generate_mod.py   (needs: pip install pillow)
The GitHub workflow runs this automatically before building."""
import os, json, random
from PIL import Image, ImageDraw

FILES = {'src/main/java/com/immortalmod/ModTab.java': 'package com.immortalmod;\n\nimport net.fabricmc.fabric.api.creativetab.v1.CreativeModeTabEvents;\nimport net.fabricmc.fabric.api.creativetab.v1.FabricCreativeModeTab;\nimport net.minecraft.core.Registry;\nimport net.minecraft.core.registries.BuiltInRegistries;\nimport net.minecraft.core.registries.Registries;\nimport net.minecraft.network.chat.Component;\nimport net.minecraft.resources.ResourceKey;\nimport net.minecraft.world.item.CreativeModeTab;\nimport net.minecraft.world.item.Item;\nimport net.minecraft.world.item.ItemStack;\n\npublic final class ModTab {\n\tpublic static final ResourceKey<CreativeModeTab> TAB = ResourceKey.create(Registries.CREATIVE_MODE_TAB, ImmortalMod.id("main"));\n\n\tprivate ModTab() {\n\t}\n\n\tpublic static void init() {\n\t\tRegistry.register(BuiltInRegistries.CREATIVE_MODE_TAB, TAB, FabricCreativeModeTab.builder()\n\t\t\t\t.icon(() -> new ItemStack(ModItems.GODLY_SWORD))\n\t\t\t\t.title(Component.translatable("itemGroup.immortal"))\n\t\t\t\t.build());\n\t\tCreativeModeTabEvents.modifyOutputEvent(TAB).register(entries -> {\n\t\t\tfor (Item item : ModItems.ALL) {\n\t\t\t\tentries.accept(item);\n\t\t\t}\n\t\t});\n\t}\n}\n', 'src/main/java/com/immortalmod/ModItems.java': 'package com.immortalmod;\n\nimport com.immortalmod.item.GoldenFoodItem;\nimport com.immortalmod.item.HeartItem;\nimport com.immortalmod.item.InfinitePearlItem;\nimport com.immortalmod.item.LungeSpearItem;\nimport com.immortalmod.item.SlashSwordItem;\nimport java.util.ArrayList;\nimport java.util.List;\nimport java.util.function.Function;\nimport net.minecraft.core.Registry;\nimport net.minecraft.core.component.DataComponents;\nimport net.minecraft.core.registries.BuiltInRegistries;\nimport net.minecraft.core.registries.Registries;\nimport net.minecraft.network.chat.Component;\nimport net.minecraft.resources.ResourceKey;\nimport net.minecraft.util.Unit;\nimport net.minecraft.world.effect.MobEffectInstance;\nimport net.minecraft.world.effect.MobEffects;\nimport net.minecraft.world.entity.EquipmentSlotGroup;\nimport net.minecraft.world.entity.ai.attributes.AttributeModifier;\nimport net.minecraft.world.entity.ai.attributes.Attributes;\nimport net.minecraft.world.food.FoodProperties;\nimport net.minecraft.world.item.BlockItem;\nimport net.minecraft.world.item.Item;\nimport net.minecraft.world.item.Rarity;\nimport net.minecraft.world.item.ToolMaterial;\nimport net.minecraft.world.item.component.ItemAttributeModifiers;\nimport net.minecraft.world.item.component.ItemLore;\nimport net.minecraft.world.item.equipment.ArmorType;\nimport net.minecraft.world.level.block.Block;\n\npublic final class ModItems {\n\t/** Everything we register, in order, for the creative tab. */\n\tpublic static final List<Item> ALL = new ArrayList<>();\n\n\t// ---- materials ----\n\tpublic static final Item IMMORTAL_INGOT = simple("immortal_ingot", p -> p.rarity(Rarity.EPIC).fireResistant().component(DataComponents.ENCHANTMENT_GLINT_OVERRIDE, true));\n\tpublic static final Item GODLY_INGOT = simple("godly_ingot", p -> p.rarity(Rarity.EPIC).fireResistant().component(DataComponents.ENCHANTMENT_GLINT_OVERRIDE, true));\n\n\t// ---- golden cooked food ----\n\tpublic static final Item GOLDEN_STEAK = food("golden_steak", 10, 1.2F);\n\tpublic static final Item GOLDEN_PORKCHOP = food("golden_porkchop", 10, 1.2F);\n\tpublic static final Item GOLDEN_CHICKEN = food("golden_chicken", 8, 1.0F);\n\tpublic static final Item GOLDEN_MUTTON = food("golden_mutton", 8, 1.0F);\n\tpublic static final Item GOLDEN_RABBIT = food("golden_rabbit", 7, 1.0F);\n\tpublic static final Item GOLDEN_COD = food("golden_cod", 7, 1.0F);\n\tpublic static final Item GOLDEN_SALMON = food("golden_salmon", 8, 1.0F);\n\tpublic static final Item GOLDEN_BAKED_POTATO = food("golden_baked_potato", 7, 1.0F);\n\tpublic static final Item GOLDEN_BREAD = food("golden_bread", 6, 1.0F);\n\n\t// ---- power apples (instant full food, big effects) ----\n\tpublic static final Item IMMORTAL_APPLE = apple("immortal_apple", Rarity.EPIC, List.of(\n\t\t\tnew MobEffectInstance(MobEffects.REGENERATION, 20 * 30, 3),\n\t\t\tnew MobEffectInstance(MobEffects.ABSORPTION, 20 * 120, 4),\n\t\t\tnew MobEffectInstance(MobEffects.RESISTANCE, 20 * 60, 2),\n\t\t\tnew MobEffectInstance(MobEffects.FIRE_RESISTANCE, 20 * 120, 0)));\n\tpublic static final Item GODLY_APPLE = apple("godly_apple", Rarity.EPIC, List.of(\n\t\t\tnew MobEffectInstance(MobEffects.REGENERATION, 20 * 60, 4),\n\t\t\tnew MobEffectInstance(MobEffects.ABSORPTION, 20 * 300, 9),\n\t\t\tnew MobEffectInstance(MobEffects.RESISTANCE, 20 * 120, 3),\n\t\t\tnew MobEffectInstance(MobEffects.FIRE_RESISTANCE, 20 * 300, 0),\n\t\t\tnew MobEffectInstance(MobEffects.STRENGTH, 20 * 120, 2),\n\t\t\tnew MobEffectInstance(MobEffects.SPEED, 20 * 120, 1)));\n\n\t// ---- galaxy gear (lowest tier, breakable) ----\n\tpublic static final Item GALAXY_INGOT = simple("galaxy_ingot", p -> p.rarity(Rarity.UNCOMMON));\n\tpublic static final Item GALAXY_PICKAXE = register("galaxy_pickaxe", Item::new,\n\t\t\tbase("galaxy_pickaxe").pickaxe(ModMaterials.GALAXY_TOOLS, 1.0F, -2.8F).rarity(Rarity.UNCOMMON));\n\tpublic static final Item GALAXY_AXE = register("galaxy_axe", Item::new,\n\t\t\tbase("galaxy_axe").axe(ModMaterials.GALAXY_TOOLS, 5.0F, -3.0F).rarity(Rarity.UNCOMMON));\n\tpublic static final Item GALAXY_SWORD = register("galaxy_sword", Item::new,\n\t\t\tbase("galaxy_sword").sword(ModMaterials.GALAXY_TOOLS, 3.0F, -2.4F).rarity(Rarity.UNCOMMON));\n\tpublic static final Item GALAXY_HELMET = armor("galaxy_helmet", ModMaterials.GALAXY_ARMOR, ArmorType.HELMET, Rarity.UNCOMMON, "Wear all 4: Speed, Night Vision");\n\tpublic static final Item GALAXY_CHESTPLATE = armor("galaxy_chestplate", ModMaterials.GALAXY_ARMOR, ArmorType.CHESTPLATE, Rarity.UNCOMMON, "Wear all 4: Speed, Night Vision");\n\tpublic static final Item GALAXY_LEGGINGS = armor("galaxy_leggings", ModMaterials.GALAXY_ARMOR, ArmorType.LEGGINGS, Rarity.UNCOMMON, "Wear all 4: Speed, Night Vision");\n\tpublic static final Item GALAXY_BOOTS = armor("galaxy_boots", ModMaterials.GALAXY_ARMOR, ArmorType.BOOTS, Rarity.UNCOMMON, "Wear all 4: Speed, Night Vision");\n\n\t// ---- bedrock pickaxe ----\n\tpublic static final Item BEDROCK_PICKAXE = register("bedrock_pickaxe", Item::new, unbreakable(\n\t\t\tbase("bedrock_pickaxe").pickaxe(ModMaterials.BEDROCK_TOOLS, 1.0F, -2.8F).rarity(Rarity.EPIC).fireResistant()\n\t\t\t\t\t.component(DataComponents.LORE, lore("Breaks bedrock in one hit", "Unbreakable"))));\n\n\t// ---- immortal gear ----\n\tpublic static final Item IMMORTAL_PICKAXE = register("immortal_pickaxe", Item::new, unbreakable(\n\t\t\tbase("immortal_pickaxe").pickaxe(ModMaterials.IMMORTAL_TOOLS, 1.0F, -2.8F).rarity(Rarity.EPIC).fireResistant()\n\t\t\t\t\t.component(DataComponents.LORE, lore("Unbreakable", "Mines bedrock in one hit"))));\n\tpublic static final Item IMMORTAL_AXE = register("immortal_axe", Item::new, unbreakable(\n\t\t\tbase("immortal_axe").axe(ModMaterials.IMMORTAL_TOOLS, 5.0F, -3.0F).rarity(Rarity.EPIC).fireResistant()\n\t\t\t\t\t.component(DataComponents.LORE, lore("Unbreakable"))));\n\tpublic static final Item IMMORTAL_SWORD = register("immortal_sword",\n\t\t\tp -> new SlashSwordItem(p, 6.0, 20.0F, 100, 1.4),\n\t\t\tunbreakable(base("immortal_sword").sword(ModMaterials.IMMORTAL_TOOLS, 3.0F, -2.4F).rarity(Rarity.EPIC).fireResistant()\n\t\t\t\t\t.component(DataComponents.LORE, lore("Unbreakable", "Right-click: Immortal Slash (shockwave, 5s cooldown)"))));\n\tpublic static final Item IMMORTAL_SPEAR = register("immortal_spear",\n\t\t\tp -> new LungeSpearItem(p, 24.0F, 2.2, 60),\n\t\t\tunbreakable(base("immortal_spear").component(DataComponents.ATTRIBUTE_MODIFIERS, spearAttributes("immortal", 13.0, 3.0)).enchantable(30).rarity(Rarity.EPIC).fireResistant()\n\t\t\t\t\t.component(DataComponents.LORE, lore("Unbreakable", "+3 reach", "Right-click: Piercing Lunge (3s cooldown)"))));\n\tpublic static final Item IMMORTAL_HELMET = armor("immortal_helmet", ModMaterials.IMMORTAL_ARMOR, ArmorType.HELMET, Rarity.EPIC, "Wear all 4: Resistance, Strength, Fire Resistance, Night Vision");\n\tpublic static final Item IMMORTAL_CHESTPLATE = armor("immortal_chestplate", ModMaterials.IMMORTAL_ARMOR, ArmorType.CHESTPLATE, Rarity.EPIC, "Wear all 4: Resistance, Strength, Fire Resistance, Night Vision");\n\tpublic static final Item IMMORTAL_LEGGINGS = armor("immortal_leggings", ModMaterials.IMMORTAL_ARMOR, ArmorType.LEGGINGS, Rarity.EPIC, "Wear all 4: Resistance, Strength, Fire Resistance, Night Vision");\n\tpublic static final Item IMMORTAL_BOOTS = armor("immortal_boots", ModMaterials.IMMORTAL_ARMOR, ArmorType.BOOTS, Rarity.EPIC, "Wear all 4: Resistance, Strength, Fire Resistance, Night Vision");\n\tpublic static final Item IMMORTAL_ENDER_PEARL = register("immortal_ender_pearl",\n\t\t\tp -> new InfinitePearlItem(p, 1.5F),\n\t\t\tbase("immortal_ender_pearl").rarity(Rarity.EPIC).fireResistant().component(DataComponents.ENCHANTMENT_GLINT_OVERRIDE, true)\n\t\t\t\t\t.component(DataComponents.LORE, lore("Unlimited uses, no cooldown")));\n\tpublic static final Item IMMORTAL_TOTEM = simple("immortal_totem", p -> p.rarity(Rarity.EPIC).fireResistant().stacksTo(1)\n\t\t\t.component(DataComponents.LORE, lore("Keep it anywhere in your inventory", "Saves you from death and is never used up")));\n\tpublic static final Item HEART = register("heart", p -> new HeartItem(p, 1),\n\t\t\tbase("heart").rarity(Rarity.RARE).component(DataComponents.LORE, lore("Right-click: +1 permanent heart")));\n\tpublic static final Item IMMORTAL_HEART = register("immortal_heart", p -> new HeartItem(p, 5),\n\t\t\tbase("immortal_heart").rarity(Rarity.EPIC).fireResistant().component(DataComponents.ENCHANTMENT_GLINT_OVERRIDE, true)\n\t\t\t\t\t.component(DataComponents.LORE, lore("Right-click: +5 permanent hearts")));\n\n\t// ---- godly gear ----\n\tpublic static final Item GODLY_PICKAXE = register("godly_pickaxe", Item::new, unbreakable(\n\t\t\tbase("godly_pickaxe").pickaxe(ModMaterials.GODLY_TOOLS, 1.0F, -2.8F).rarity(Rarity.EPIC).fireResistant()\n\t\t\t\t\t.component(DataComponents.ENCHANTMENT_GLINT_OVERRIDE, true)\n\t\t\t\t\t.component(DataComponents.LORE, lore("Unbreakable", "Near-instant mining", "Mines bedrock in one hit"))));\n\tpublic static final Item GODLY_AXE = register("godly_axe", Item::new, unbreakable(\n\t\t\tbase("godly_axe").axe(ModMaterials.GODLY_TOOLS, 5.0F, -3.0F).rarity(Rarity.EPIC).fireResistant()\n\t\t\t\t\t.component(DataComponents.ENCHANTMENT_GLINT_OVERRIDE, true)\n\t\t\t\t\t.component(DataComponents.LORE, lore("Unbreakable"))));\n\tpublic static final Item GODLY_SWORD = register("godly_sword",\n\t\t\tp -> new SlashSwordItem(p, 12.0, 60.0F, 60, 2.2),\n\t\t\tunbreakable(base("godly_sword").sword(ModMaterials.GODLY_TOOLS, 3.0F, -2.4F).rarity(Rarity.EPIC).fireResistant()\n\t\t\t\t\t.component(DataComponents.ENCHANTMENT_GLINT_OVERRIDE, true)\n\t\t\t\t\t.component(DataComponents.LORE, lore("Unbreakable", "Right-click: Godly Judgement (huge shockwave, 3s cooldown)"))));\n\tpublic static final Item GODLY_SPEAR = register("godly_spear",\n\t\t\tp -> new LungeSpearItem(p, 70.0F, 3.0, 40),\n\t\t\tunbreakable(base("godly_spear").component(DataComponents.ATTRIBUTE_MODIFIERS, spearAttributes("godly", 30.0, 5.0)).enchantable(40).rarity(Rarity.EPIC).fireResistant()\n\t\t\t\t\t.component(DataComponents.ENCHANTMENT_GLINT_OVERRIDE, true)\n\t\t\t\t\t.component(DataComponents.LORE, lore("Unbreakable", "+5 reach", "Right-click: Piercing Lunge (2s cooldown)"))));\n\tpublic static final Item GODLY_HELMET = armor("godly_helmet", ModMaterials.GODLY_ARMOR, ArmorType.HELMET, Rarity.EPIC, "Wear all 4: FLY, no fall damage, god-tier buffs");\n\tpublic static final Item GODLY_CHESTPLATE = armor("godly_chestplate", ModMaterials.GODLY_ARMOR, ArmorType.CHESTPLATE, Rarity.EPIC, "Wear all 4: FLY, no fall damage, god-tier buffs");\n\tpublic static final Item GODLY_LEGGINGS = armor("godly_leggings", ModMaterials.GODLY_ARMOR, ArmorType.LEGGINGS, Rarity.EPIC, "Wear all 4: FLY, no fall damage, god-tier buffs");\n\tpublic static final Item GODLY_BOOTS = armor("godly_boots", ModMaterials.GODLY_ARMOR, ArmorType.BOOTS, Rarity.EPIC, "Wear all 4: FLY, no fall damage, god-tier buffs");\n\tpublic static final Item GODLY_ENDER_PEARL = register("godly_ender_pearl",\n\t\t\tp -> new InfinitePearlItem(p, 3.0F),\n\t\t\tbase("godly_ender_pearl").rarity(Rarity.EPIC).fireResistant().component(DataComponents.ENCHANTMENT_GLINT_OVERRIDE, true)\n\t\t\t\t\t.component(DataComponents.LORE, lore("Unlimited uses, no cooldown, throws twice as far")));\n\tpublic static final Item GODLY_TOTEM = simple("godly_totem", p -> p.rarity(Rarity.EPIC).fireResistant().stacksTo(1)\n\t\t\t.component(DataComponents.ENCHANTMENT_GLINT_OVERRIDE, true)\n\t\t\t.component(DataComponents.LORE, lore("Keep it anywhere in your inventory", "Full heal + god buffs on death, never used up")));\n\tpublic static final Item GODLY_HEART = register("godly_heart", p -> new HeartItem(p, 10),\n\t\t\tbase("godly_heart").rarity(Rarity.EPIC).fireResistant().component(DataComponents.ENCHANTMENT_GLINT_OVERRIDE, true)\n\t\t\t\t\t.component(DataComponents.LORE, lore("Right-click: +10 permanent hearts")));\n\n\t// ---- purple superhero armour ----\n\tpublic static final Item PURPLE_HERO_HELMET = armor("purple_hero_helmet", ModMaterials.PURPLE_HERO_ARMOR, ArmorType.HELMET, Rarity.RARE, "Wear all 4: Speed, Jump Boost, Strength");\n\tpublic static final Item PURPLE_HERO_CHESTPLATE = armor("purple_hero_chestplate", ModMaterials.PURPLE_HERO_ARMOR, ArmorType.CHESTPLATE, Rarity.RARE, "Wear all 4: Speed, Jump Boost, Strength");\n\tpublic static final Item PURPLE_HERO_LEGGINGS = armor("purple_hero_leggings", ModMaterials.PURPLE_HERO_ARMOR, ArmorType.LEGGINGS, Rarity.RARE, "Wear all 4: Speed, Jump Boost, Strength");\n\tpublic static final Item PURPLE_HERO_BOOTS = armor("purple_hero_boots", ModMaterials.PURPLE_HERO_ARMOR, ArmorType.BOOTS, Rarity.RARE, "Wear all 4: Speed, Jump Boost, Strength");\n\n\t// ---- enchantable sword blocks (made in the stonecutter) ----\n\tpublic static final Item IRON_SWORD_BLOCK = swordBlock("iron_sword_block", ModBlocks.IRON_SWORD_BLOCK, net.minecraft.world.item.ToolMaterial.IRON, false);\n\tpublic static final Item DIAMOND_SWORD_BLOCK = swordBlock("diamond_sword_block", ModBlocks.DIAMOND_SWORD_BLOCK, net.minecraft.world.item.ToolMaterial.DIAMOND, false);\n\tpublic static final Item NETHERITE_SWORD_BLOCK = swordBlock("netherite_sword_block", ModBlocks.NETHERITE_SWORD_BLOCK, net.minecraft.world.item.ToolMaterial.NETHERITE, false);\n\tpublic static final Item IMMORTAL_SWORD_BLOCK = swordBlock("immortal_sword_block", ModBlocks.IMMORTAL_SWORD_BLOCK, ModMaterials.IMMORTAL_TOOLS, true);\n\tpublic static final Item GODLY_SWORD_BLOCK = swordBlock("godly_sword_block", ModBlocks.GODLY_SWORD_BLOCK, ModMaterials.GODLY_TOOLS, true);\n\n\tprivate ModItems() {\n\t}\n\n\tpublic static void init() {\n\t}\n\n\t// ------------------------------------------------------------------ helpers\n\n\tprivate static ResourceKey<Item> key(String name) {\n\t\treturn ResourceKey.create(Registries.ITEM, ImmortalMod.id(name));\n\t}\n\n\tprivate static Item.Properties base(String name) {\n\t\treturn new Item.Properties().setId(key(name));\n\t}\n\n\tprivate static Item.Properties unbreakable(Item.Properties p) {\n\t\treturn p.component(DataComponents.UNBREAKABLE, Unit.INSTANCE);\n\t}\n\n\tprivate static ItemLore lore(String... lines) {\n\t\tList<Component> list = new ArrayList<>();\n\t\tfor (String line : lines) {\n\t\t\tlist.add(Component.literal(line));\n\t\t}\n\t\treturn new ItemLore(list);\n\t}\n\n\tprivate static <T extends Item> T register(String name, Function<Item.Properties, T> factory, Item.Properties properties) {\n\t\tT item = Registry.register(BuiltInRegistries.ITEM, key(name), factory.apply(properties));\n\t\tALL.add(item);\n\t\treturn item;\n\t}\n\n\tprivate static Item simple(String name, Function<Item.Properties, Item.Properties> customiser) {\n\t\treturn register(name, Item::new, customiser.apply(base(name)));\n\t}\n\n\tprivate static Item food(String name, int nutrition, float saturation) {\n\t\tFoodProperties food = new FoodProperties.Builder().nutrition(nutrition).saturationModifier(saturation).alwaysEdible().build();\n\t\treturn register(name,\n\t\t\t\tp -> new GoldenFoodItem(p, List.of(\n\t\t\t\t\t\tnew MobEffectInstance(MobEffects.REGENERATION, 20 * 5, 1),\n\t\t\t\t\t\tnew MobEffectInstance(MobEffects.ABSORPTION, 20 * 60, 1))),\n\t\t\t\tbase(name).food(food).rarity(Rarity.RARE)\n\t\t\t\t\t\t.component(DataComponents.LORE, lore("Regeneration II + Absorption II")));\n\t}\n\n\tprivate static Item apple(String name, Rarity rarity, List<MobEffectInstance> effects) {\n\t\tFoodProperties food = new FoodProperties.Builder().nutrition(20).saturationModifier(1.0F).alwaysEdible().build();\n\t\treturn register(name, p -> new GoldenFoodItem(p, effects),\n\t\t\t\tbase(name).food(food).rarity(rarity).fireResistant().component(DataComponents.ENCHANTMENT_GLINT_OVERRIDE, true));\n\t}\n\n\tprivate static Item armor(String name, net.minecraft.world.item.equipment.ArmorMaterial material, ArmorType slot, Rarity rarity, String loreLine) {\n\t\tItem.Properties p = base(name).humanoidArmor(material, slot).rarity(rarity)\n\t\t\t\t.component(DataComponents.LORE, lore(loreLine));\n\t\tif (material != ModMaterials.PURPLE_HERO_ARMOR && material != ModMaterials.GALAXY_ARMOR) {\n\t\t\tp = unbreakable(p).fireResistant();\n\t\t}\n\t\treturn register(name, Item::new, p);\n\t}\n\n\tprivate static ItemAttributeModifiers spearAttributes(String tier, double damage, double reach) {\n\t\treturn ItemAttributeModifiers.builder()\n\t\t\t\t.add(Attributes.ATTACK_DAMAGE, new AttributeModifier(Item.BASE_ATTACK_DAMAGE_ID, damage, AttributeModifier.Operation.ADD_VALUE), EquipmentSlotGroup.MAINHAND)\n\t\t\t\t.add(Attributes.ATTACK_SPEED, new AttributeModifier(Item.BASE_ATTACK_SPEED_ID, -2.6, AttributeModifier.Operation.ADD_VALUE), EquipmentSlotGroup.MAINHAND)\n\t\t\t\t.add(Attributes.ENTITY_INTERACTION_RANGE, new AttributeModifier(ImmortalMod.id(tier + "_spear_reach"), reach, AttributeModifier.Operation.ADD_VALUE), EquipmentSlotGroup.MAINHAND)\n\t\t\t\t.build();\n\t}\n\n\tprivate static Item swordBlock(String name, Block block, ToolMaterial material, boolean indestructible) {\n\t\tItem.Properties p = base(name).useBlockDescriptionPrefix().sword(material, 3.0F, -2.4F);\n\t\tif (indestructible) {\n\t\t\tp = unbreakable(p).fireResistant().rarity(Rarity.EPIC);\n\t\t}\n\t\tBlockItem item = Registry.register(BuiltInRegistries.ITEM, key(name), new BlockItem(block, p));\n\t\tALL.add(item);\n\t\treturn item;\n\t}\n}\n', 'src/main/java/com/immortalmod/ImmortalMod.java': 'package com.immortalmod;\n\nimport net.fabricmc.api.ModInitializer;\nimport net.minecraft.resources.Identifier;\nimport org.slf4j.Logger;\nimport org.slf4j.LoggerFactory;\n\npublic class ImmortalMod implements ModInitializer {\n\tpublic static final String MOD_ID = "immortal";\n\tpublic static final Logger LOGGER = LoggerFactory.getLogger(MOD_ID);\n\n\tpublic static Identifier id(String path) {\n\t\treturn Identifier.fromNamespaceAndPath(MOD_ID, path);\n\t}\n\n\t@Override\n\tpublic void onInitialize() {\n\t\tModAttachments.init();\n\t\tModBlocks.init();   // blocks first: the sword-block items need them\n\t\tModItems.init();\n\t\tModTab.init();\n\t\tModEvents.init();\n\t\tLOGGER.info("Immortal & Godly loaded");\n\t}\n}\n', 'src/main/java/com/immortalmod/ModMaterials.java': 'package com.immortalmod;\n\nimport java.util.Map;\nimport net.minecraft.resources.ResourceKey;\nimport net.minecraft.sounds.SoundEvents;\nimport net.minecraft.tags.BlockTags;\nimport net.minecraft.tags.ItemTags;\nimport net.minecraft.world.item.ToolMaterial;\nimport net.minecraft.world.item.equipment.ArmorMaterial;\nimport net.minecraft.world.item.equipment.ArmorType;\nimport net.minecraft.world.item.equipment.EquipmentAsset;\nimport net.minecraft.world.item.equipment.EquipmentAssets;\n\npublic final class ModMaterials {\n\t// ToolMaterial(incorrectBlocksTag, durability, miningSpeed, attackDamageBonus, enchantability, repairTag)\n\tpublic static final ToolMaterial BEDROCK_TOOLS = new ToolMaterial(BlockTags.INCORRECT_FOR_NETHERITE_TOOL, 5000, 30.0F, 4.0F, 25, ItemTags.NETHERITE_TOOL_MATERIALS);\n\tpublic static final ToolMaterial GALAXY_TOOLS = new ToolMaterial(BlockTags.INCORRECT_FOR_DIAMOND_TOOL, 2500, 12.0F, 5.0F, 22, ItemTags.DIAMOND_TOOL_MATERIALS);\n\tpublic static final ToolMaterial IMMORTAL_TOOLS = new ToolMaterial(BlockTags.INCORRECT_FOR_NETHERITE_TOOL, 5000, 35.0F, 8.0F, 30, ItemTags.NETHERITE_TOOL_MATERIALS);\n\tpublic static final ToolMaterial GODLY_TOOLS = new ToolMaterial(BlockTags.INCORRECT_FOR_NETHERITE_TOOL, 9999, 120.0F, 20.0F, 40, ItemTags.NETHERITE_TOOL_MATERIALS);\n\n\t// ArmorMaterial(durability, defense, enchantability, equipSound, toughness, knockbackResistance, repairTag, assetId)\n\tpublic static final ArmorMaterial GALAXY_ARMOR = new ArmorMaterial(\n\t\t\t35,\n\t\t\tMap.of(ArmorType.BOOTS, 2, ArmorType.LEGGINGS, 5, ArmorType.CHESTPLATE, 7, ArmorType.HELMET, 2, ArmorType.BODY, 9),\n\t\t\t22, SoundEvents.ARMOR_EQUIP_DIAMOND, 1.0F, 0.0F,\n\t\t\tItemTags.REPAIRS_DIAMOND_ARMOR, asset("galaxy"));\n\n\tpublic static final ArmorMaterial IMMORTAL_ARMOR = new ArmorMaterial(\n\t\t\t100,\n\t\t\tMap.of(ArmorType.BOOTS, 4, ArmorType.LEGGINGS, 8, ArmorType.CHESTPLATE, 10, ArmorType.HELMET, 4, ArmorType.BODY, 12),\n\t\t\t30, SoundEvents.ARMOR_EQUIP_NETHERITE, 6.0F, 0.2F,\n\t\t\tItemTags.REPAIRS_NETHERITE_ARMOR, asset("immortal"));\n\n\tpublic static final ArmorMaterial GODLY_ARMOR = new ArmorMaterial(\n\t\t\t100,\n\t\t\tMap.of(ArmorType.BOOTS, 5, ArmorType.LEGGINGS, 10, ArmorType.CHESTPLATE, 12, ArmorType.HELMET, 5, ArmorType.BODY, 15),\n\t\t\t40, SoundEvents.ARMOR_EQUIP_NETHERITE, 10.0F, 0.5F,\n\t\t\tItemTags.REPAIRS_NETHERITE_ARMOR, asset("godly"));\n\n\tpublic static final ArmorMaterial PURPLE_HERO_ARMOR = new ArmorMaterial(\n\t\t\t40,\n\t\t\tMap.of(ArmorType.BOOTS, 3, ArmorType.LEGGINGS, 6, ArmorType.CHESTPLATE, 8, ArmorType.HELMET, 3, ArmorType.BODY, 11),\n\t\t\t25, SoundEvents.ARMOR_EQUIP_IRON, 2.0F, 0.0F,\n\t\t\tItemTags.REPAIRS_DIAMOND_ARMOR, asset("purple_hero"));\n\n\tprivate ModMaterials() {\n\t}\n\n\tprivate static ResourceKey<EquipmentAsset> asset(String name) {\n\t\treturn ResourceKey.create(EquipmentAssets.ROOT_ID, ImmortalMod.id(name));\n\t}\n}\n', 'src/main/java/com/immortalmod/ModAttachments.java': 'package com.immortalmod;\n\nimport com.mojang.serialization.Codec;\nimport net.fabricmc.fabric.api.attachment.v1.AttachmentRegistry;\nimport net.fabricmc.fabric.api.attachment.v1.AttachmentType;\nimport net.minecraft.resources.Identifier;\nimport net.minecraft.server.level.ServerPlayer;\nimport net.minecraft.world.entity.ai.attributes.AttributeInstance;\nimport net.minecraft.world.entity.ai.attributes.AttributeModifier;\nimport net.minecraft.world.entity.ai.attributes.Attributes;\n\n/** Stores how much extra max health (in half-hearts) a player has gained from heart items. Survives death. */\npublic final class ModAttachments {\n\tprivate static final Identifier MODIFIER_ID = ImmortalMod.id("bonus_hearts");\n\n\tpublic static final AttachmentType<Integer> BONUS_HEALTH = AttachmentRegistry.create(\n\t\t\tImmortalMod.id("bonus_health"),\n\t\t\tbuilder -> builder.initializer(() -> 0).persistent(Codec.INT).copyOnDeath()\n\t);\n\n\tprivate ModAttachments() {\n\t}\n\n\tpublic static void init() {\n\t\t// touching the class registers the attachment\n\t}\n\n\t/** Adds half-hearts (2 = one heart) and applies them. */\n\tpublic static void addBonusHealth(ServerPlayer player, int halfHearts) {\n\t\tint total = player.getAttachedOrCreate(BONUS_HEALTH) + halfHearts;\n\t\tplayer.setAttached(BONUS_HEALTH, total);\n\t\tapply(player);\n\t\tplayer.heal(halfHearts);\n\t}\n\n\t/** Re-applies the stored bonus as a permanent max-health modifier. Safe to call any time. */\n\tpublic static void apply(ServerPlayer player) {\n\t\tAttributeInstance maxHealth = player.getAttribute(Attributes.MAX_HEALTH);\n\t\tif (maxHealth == null) {\n\t\t\treturn;\n\t\t}\n\t\tmaxHealth.removeModifier(MODIFIER_ID);\n\t\tint bonus = player.getAttachedOrCreate(BONUS_HEALTH);\n\t\tif (bonus > 0) {\n\t\t\tmaxHealth.addPermanentModifier(new AttributeModifier(MODIFIER_ID, bonus, AttributeModifier.Operation.ADD_VALUE));\n\t\t}\n\t}\n}\n', 'src/main/java/com/immortalmod/ModBlocks.java': 'package com.immortalmod;\n\nimport net.minecraft.core.Registry;\nimport net.minecraft.core.registries.BuiltInRegistries;\nimport net.minecraft.core.registries.Registries;\nimport net.minecraft.resources.ResourceKey;\nimport net.minecraft.world.level.block.Block;\nimport net.minecraft.world.level.block.SoundType;\nimport net.minecraft.world.level.block.state.BlockBehaviour;\n\npublic final class ModBlocks {\n\tpublic static final Block IRON_SWORD_BLOCK = register("iron_sword_block");\n\tpublic static final Block DIAMOND_SWORD_BLOCK = register("diamond_sword_block");\n\tpublic static final Block NETHERITE_SWORD_BLOCK = register("netherite_sword_block");\n\tpublic static final Block IMMORTAL_SWORD_BLOCK = register("immortal_sword_block");\n\tpublic static final Block GODLY_SWORD_BLOCK = register("godly_sword_block");\n\n\tprivate ModBlocks() {\n\t}\n\n\tprivate static Block register(String name) {\n\t\tResourceKey<Block> key = ResourceKey.create(Registries.BLOCK, ImmortalMod.id(name));\n\t\tBlock block = new Block(BlockBehaviour.Properties.of().strength(4.0F, 8.0F).sound(SoundType.METAL).setId(key));\n\t\treturn Registry.register(BuiltInRegistries.BLOCK, key, block);\n\t}\n\n\tpublic static void init() {\n\t}\n}\n', 'src/main/java/com/immortalmod/ModEvents.java': 'package com.immortalmod;\n\nimport java.util.HashSet;\nimport java.util.Set;\nimport java.util.UUID;\nimport net.fabricmc.fabric.api.entity.event.v1.ServerLivingEntityEvents;\nimport net.fabricmc.fabric.api.entity.event.v1.ServerPlayerEvents;\nimport net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;\nimport net.fabricmc.fabric.api.event.player.AttackBlockCallback;\nimport net.fabricmc.fabric.api.networking.v1.ServerPlayConnectionEvents;\nimport net.minecraft.server.level.ServerLevel;\nimport net.minecraft.server.level.ServerPlayer;\nimport net.minecraft.sounds.SoundEvents;\nimport net.minecraft.sounds.SoundSource;\nimport net.minecraft.tags.DamageTypeTags;\nimport net.minecraft.world.InteractionResult;\nimport net.minecraft.world.effect.MobEffectInstance;\nimport net.minecraft.world.effect.MobEffects;\nimport net.minecraft.world.entity.EquipmentSlot;\nimport net.minecraft.world.entity.player.Inventory;\nimport net.minecraft.world.item.Item;\nimport net.minecraft.world.item.ItemStack;\nimport net.minecraft.world.level.block.Block;\nimport net.minecraft.world.level.block.Blocks;\nimport net.minecraft.world.level.block.state.BlockState;\n\npublic final class ModEvents {\n\t/** Players we gave flight to (so we only take it back from players we gave it to). */\n\tprivate static final Set<UUID> FLYERS = new HashSet<>();\n\n\tprivate static final Set<Item> BEDROCK_BREAKERS = Set.of(ModItems.BEDROCK_PICKAXE, ModItems.IMMORTAL_PICKAXE, ModItems.GODLY_PICKAXE);\n\n\tprivate ModEvents() {\n\t}\n\n\tpublic static void init() {\n\t\tregisterHearts();\n\t\tregisterBedrockBreaking();\n\t\tregisterTotems();\n\t\tregisterArmourSets();\n\t}\n\n\t// ------------------------------------------------------------ hearts persist\n\n\tprivate static void registerHearts() {\n\t\tServerPlayConnectionEvents.JOIN.register((handler, sender, server) -> ModAttachments.apply(handler.getPlayer()));\n\t\tServerPlayerEvents.AFTER_RESPAWN.register((oldPlayer, newPlayer, alive) -> {\n\t\t\tModAttachments.apply(newPlayer);\n\t\t\tnewPlayer.setHealth(newPlayer.getMaxHealth());\n\t\t});\n\t\tServerPlayerEvents.LEAVE.register(player -> FLYERS.remove(player.getUUID()));\n\t}\n\n\t// ------------------------------------------------------------ bedrock pickaxe\n\n\tprivate static void registerBedrockBreaking() {\n\t\tAttackBlockCallback.EVENT.register((player, level, hand, pos, direction) -> {\n\t\t\tif (player.isSpectator() || !BEDROCK_BREAKERS.contains(player.getItemInHand(hand).getItem())) {\n\t\t\t\treturn InteractionResult.PASS;\n\t\t\t}\n\t\t\tBlockState state = level.getBlockState(pos);\n\t\t\tBlock block = state.getBlock();\n\t\t\tboolean breakable = block == Blocks.BEDROCK || block == Blocks.REINFORCED_DEEPSLATE || block == Blocks.END_PORTAL_FRAME;\n\t\t\tif (!breakable) {\n\t\t\t\treturn InteractionResult.PASS;\n\t\t\t}\n\t\t\tif (level instanceof ServerLevel serverLevel) {\n\t\t\t\tlevel.destroyBlock(pos, false, player);\n\t\t\t\tif (!player.isCreative()) {\n\t\t\t\t\tBlock.popResource(serverLevel, pos, new ItemStack(block.asItem()));\n\t\t\t\t}\n\t\t\t}\n\t\t\treturn InteractionResult.SUCCESS;\n\t\t});\n\t}\n\n\t// ------------------------------------------------------------ totems\n\n\tprivate static void registerTotems() {\n\t\tServerLivingEntityEvents.ALLOW_DEATH.register((entity, source, amount) -> {\n\t\t\tif (!(entity instanceof ServerPlayer player) || source.is(DamageTypeTags.BYPASSES_INVULNERABILITY)) {\n\t\t\t\treturn true;\n\t\t\t}\n\t\t\tboolean godly = hasInInventory(player, ModItems.GODLY_TOTEM);\n\t\t\tboolean immortal = hasInInventory(player, ModItems.IMMORTAL_TOTEM);\n\t\t\tif (!godly && !immortal) {\n\t\t\t\treturn true;\n\t\t\t}\n\t\t\tplayer.setHealth(godly ? player.getMaxHealth() : Math.max(1.0F, player.getMaxHealth() * 0.5F));\n\t\t\tplayer.removeAllEffects();\n\t\t\tplayer.addEffect(new MobEffectInstance(MobEffects.REGENERATION, godly ? 20 * 45 : 20 * 20, godly ? 3 : 1));\n\t\t\tplayer.addEffect(new MobEffectInstance(MobEffects.ABSORPTION, 20 * 30, godly ? 9 : 4));\n\t\t\tplayer.addEffect(new MobEffectInstance(MobEffects.FIRE_RESISTANCE, 20 * 40, 0));\n\t\t\tplayer.addEffect(new MobEffectInstance(MobEffects.RESISTANCE, 20 * 10, godly ? 4 : 2));\n\t\t\tServerLevel level = (ServerLevel) player.level();\n\t\t\tlevel.broadcastEntityEvent(player, (byte) 35); // vanilla totem pop animation\n\t\t\tlevel.playSound(null, player.getX(), player.getY(), player.getZ(), SoundEvents.TOTEM_USE, SoundSource.PLAYERS, 1.0F, 1.0F);\n\t\t\treturn false; // cancel the death; the totem is NOT consumed\n\t\t});\n\t}\n\n\tprivate static boolean hasInInventory(ServerPlayer player, Item item) {\n\t\tInventory inv = player.getInventory();\n\t\tfor (int i = 0; i < inv.getContainerSize(); i++) {\n\t\t\tif (inv.getItem(i).is(item)) {\n\t\t\t\treturn true;\n\t\t\t}\n\t\t}\n\t\treturn false;\n\t}\n\n\t// ------------------------------------------------------------ armour sets\n\n\tprivate static void registerArmourSets() {\n\t\t// godly armour: no fall damage\n\t\tServerLivingEntityEvents.ALLOW_DAMAGE.register((entity, source, amount) -> {\n\t\t\tif (entity instanceof ServerPlayer player && source.is(DamageTypeTags.IS_FALL) && wearing(player, ModItems.GODLY_HELMET, ModItems.GODLY_CHESTPLATE, ModItems.GODLY_LEGGINGS, ModItems.GODLY_BOOTS)) {\n\t\t\t\treturn false;\n\t\t\t}\n\t\t\treturn true;\n\t\t});\n\n\t\tServerTickEvents.END_SERVER_TICK.register(server -> {\n\t\t\tboolean refresh = server.getTickCount() % 10 == 0;\n\t\t\tfor (ServerPlayer player : server.getPlayerList().getPlayers()) {\n\t\t\t\tboolean godly = wearing(player, ModItems.GODLY_HELMET, ModItems.GODLY_CHESTPLATE, ModItems.GODLY_LEGGINGS, ModItems.GODLY_BOOTS);\n\t\t\t\tupdateFlight(player, godly);\n\t\t\t\tif (!refresh) {\n\t\t\t\t\tcontinue;\n\t\t\t\t}\n\t\t\t\tif (godly) {\n\t\t\t\t\teffect(player, MobEffects.RESISTANCE, 3);\n\t\t\t\t\teffect(player, MobEffects.STRENGTH, 2);\n\t\t\t\t\teffect(player, MobEffects.SPEED, 1);\n\t\t\t\t\teffect(player, MobEffects.HASTE, 2);\n\t\t\t\t\teffect(player, MobEffects.REGENERATION, 2);\n\t\t\t\t\teffect(player, MobEffects.JUMP_BOOST, 1);\n\t\t\t\t\teffect(player, MobEffects.SATURATION, 0);\n\t\t\t\t\teffect(player, MobEffects.FIRE_RESISTANCE, 0);\n\t\t\t\t\teffect(player, MobEffects.WATER_BREATHING, 0);\n\t\t\t\t\teffect(player, MobEffects.NIGHT_VISION, 0, 260);\n\t\t\t\t} else if (wearing(player, ModItems.IMMORTAL_HELMET, ModItems.IMMORTAL_CHESTPLATE, ModItems.IMMORTAL_LEGGINGS, ModItems.IMMORTAL_BOOTS)) {\n\t\t\t\t\teffect(player, MobEffects.RESISTANCE, 1);\n\t\t\t\t\teffect(player, MobEffects.STRENGTH, 0);\n\t\t\t\t\teffect(player, MobEffects.FIRE_RESISTANCE, 0);\n\t\t\t\t\teffect(player, MobEffects.WATER_BREATHING, 0);\n\t\t\t\t\teffect(player, MobEffects.NIGHT_VISION, 0, 260);\n\t\t\t\t}\n\t\t\t\tif (wearing(player, ModItems.GALAXY_HELMET, ModItems.GALAXY_CHESTPLATE, ModItems.GALAXY_LEGGINGS, ModItems.GALAXY_BOOTS)) {\n\t\t\t\t\teffect(player, MobEffects.SPEED, 0);\n\t\t\t\t\teffect(player, MobEffects.NIGHT_VISION, 0, 260);\n\t\t\t\t}\n\t\t\t\tif (wearing(player, ModItems.PURPLE_HERO_HELMET, ModItems.PURPLE_HERO_CHESTPLATE, ModItems.PURPLE_HERO_LEGGINGS, ModItems.PURPLE_HERO_BOOTS)) {\n\t\t\t\t\teffect(player, MobEffects.SPEED, 2);\n\t\t\t\t\teffect(player, MobEffects.JUMP_BOOST, 2);\n\t\t\t\t\teffect(player, MobEffects.STRENGTH, 1);\n\t\t\t\t\teffect(player, MobEffects.NIGHT_VISION, 0, 260);\n\t\t\t\t}\n\t\t\t}\n\t\t});\n\t}\n\n\tprivate static void updateFlight(ServerPlayer player, boolean godlySet) {\n\t\tif (player.isCreative() || player.isSpectator()) {\n\t\t\tFLYERS.remove(player.getUUID());\n\t\t\treturn;\n\t\t}\n\t\tif (godlySet) {\n\t\t\tif (!player.getAbilities().mayfly) {\n\t\t\t\tplayer.getAbilities().mayfly = true;\n\t\t\t\tplayer.onUpdateAbilities();\n\t\t\t}\n\t\t\tFLYERS.add(player.getUUID());\n\t\t} else if (FLYERS.remove(player.getUUID())) {\n\t\t\tplayer.getAbilities().mayfly = false;\n\t\t\tplayer.getAbilities().flying = false;\n\t\t\tplayer.onUpdateAbilities();\n\t\t}\n\t}\n\n\tprivate static boolean wearing(ServerPlayer player, Item head, Item chest, Item legs, Item feet) {\n\t\treturn player.getItemBySlot(EquipmentSlot.HEAD).is(head)\n\t\t\t\t&& player.getItemBySlot(EquipmentSlot.CHEST).is(chest)\n\t\t\t\t&& player.getItemBySlot(EquipmentSlot.LEGS).is(legs)\n\t\t\t\t&& player.getItemBySlot(EquipmentSlot.FEET).is(feet);\n\t}\n\n\tprivate static void effect(ServerPlayer player, net.minecraft.core.Holder<net.minecraft.world.effect.MobEffect> effect, int amplifier) {\n\t\teffect(player, effect, amplifier, 40);\n\t}\n\n\tprivate static void effect(ServerPlayer player, net.minecraft.core.Holder<net.minecraft.world.effect.MobEffect> effect, int amplifier, int duration) {\n\t\tplayer.addEffect(new MobEffectInstance(effect, duration, amplifier, true, false));\n\t}\n}\n', 'src/main/java/com/immortalmod/item/HeartItem.java': 'package com.immortalmod.item;\n\nimport com.immortalmod.ModAttachments;\nimport net.minecraft.core.particles.ParticleTypes;\nimport net.minecraft.network.chat.Component;\nimport net.minecraft.server.level.ServerLevel;\nimport net.minecraft.server.level.ServerPlayer;\nimport net.minecraft.sounds.SoundEvents;\nimport net.minecraft.sounds.SoundSource;\nimport net.minecraft.world.InteractionHand;\nimport net.minecraft.world.InteractionResult;\nimport net.minecraft.world.entity.player.Player;\nimport net.minecraft.world.item.Item;\nimport net.minecraft.world.item.ItemStack;\nimport net.minecraft.world.level.Level;\n\n/** Right-click to permanently gain extra max health. 1 heart = 2 half-hearts. */\npublic class HeartItem extends Item {\n\tprivate final int hearts;\n\n\tpublic HeartItem(Properties properties, int hearts) {\n\t\tsuper(properties);\n\t\tthis.hearts = hearts;\n\t}\n\n\t@Override\n\tpublic InteractionResult use(Level level, Player player, InteractionHand hand) {\n\t\tItemStack stack = player.getItemInHand(hand);\n\t\tif (level instanceof ServerLevel serverLevel && player instanceof ServerPlayer serverPlayer) {\n\t\t\tModAttachments.addBonusHealth(serverPlayer, hearts * 2);\n\t\t\tserverLevel.sendParticles(ParticleTypes.HEART, player.getX(), player.getY() + 1.0, player.getZ(), 12 + hearts * 2, 0.5, 0.6, 0.5, 0.1);\n\t\t\tlevel.playSound(null, player.getX(), player.getY(), player.getZ(), SoundEvents.PLAYER_LEVELUP, SoundSource.PLAYERS, 1.0F, 1.3F);\n\t\t\tint total = serverPlayer.getAttachedOrCreate(ModAttachments.BONUS_HEALTH) / 2;\n\t\t\tserverPlayer.sendSystemMessage(Component.literal("+" + hearts + " heart" + (hearts == 1 ? "" : "s") + " (bonus hearts: " + total + ")"), true);\n\t\t\tstack.consume(1, player);\n\t\t}\n\t\treturn InteractionResult.SUCCESS;\n\t}\n}\n', 'src/main/java/com/immortalmod/item/SlashSwordItem.java': 'package com.immortalmod.item;\n\nimport java.util.List;\nimport net.minecraft.core.particles.ParticleTypes;\nimport net.minecraft.server.level.ServerLevel;\nimport net.minecraft.sounds.SoundEvents;\nimport net.minecraft.sounds.SoundSource;\nimport net.minecraft.world.InteractionHand;\nimport net.minecraft.world.InteractionResult;\nimport net.minecraft.world.entity.LivingEntity;\nimport net.minecraft.world.entity.player.Player;\nimport net.minecraft.world.item.Item;\nimport net.minecraft.world.item.ItemStack;\nimport net.minecraft.world.level.Level;\nimport net.minecraft.world.phys.Vec3;\n\n/** Sword whose right-click is a special attack: a shockwave that damages and blasts away everything around you. */\npublic class SlashSwordItem extends Item {\n\tprivate final double radius;\n\tprivate final float damage;\n\tprivate final int cooldownTicks;\n\tprivate final double knockback;\n\n\tpublic SlashSwordItem(Properties properties, double radius, float damage, int cooldownTicks, double knockback) {\n\t\tsuper(properties);\n\t\tthis.radius = radius;\n\t\tthis.damage = damage;\n\t\tthis.cooldownTicks = cooldownTicks;\n\t\tthis.knockback = knockback;\n\t}\n\n\t@Override\n\tpublic InteractionResult use(Level level, Player player, InteractionHand hand) {\n\t\tItemStack stack = player.getItemInHand(hand);\n\t\tif (level instanceof ServerLevel serverLevel) {\n\t\t\tList<LivingEntity> targets = serverLevel.getEntitiesOfClass(\n\t\t\t\t\tLivingEntity.class,\n\t\t\t\t\tplayer.getBoundingBox().inflate(radius),\n\t\t\t\t\te -> e != player && e.isAlive() && !e.isAlliedTo(player));\n\t\t\tfor (LivingEntity target : targets) {\n\t\t\t\ttarget.hurtServer(serverLevel, serverLevel.damageSources().playerAttack(player), damage);\n\t\t\t\tVec3 away = target.position().subtract(player.position()).multiply(1, 0, 1);\n\t\t\t\tif (away.lengthSqr() > 1.0E-4) {\n\t\t\t\t\taway = away.normalize().scale(knockback);\n\t\t\t\t\ttarget.setDeltaMovement(target.getDeltaMovement().add(away.x, 0.45, away.z));\n\t\t\t\t\ttarget.hurtMarked = true;\n\t\t\t\t}\n\t\t\t}\n\t\t\t// ring of sweep particles around the player\n\t\t\tfor (int i = 0; i < 24; i++) {\n\t\t\t\tdouble angle = i * (Math.PI * 2 / 24);\n\t\t\t\tserverLevel.sendParticles(ParticleTypes.SWEEP_ATTACK,\n\t\t\t\t\t\tplayer.getX() + Math.cos(angle) * radius * 0.6, player.getY() + 1.0, player.getZ() + Math.sin(angle) * radius * 0.6,\n\t\t\t\t\t\t1, 0, 0, 0, 0);\n\t\t\t}\n\t\t\tlevel.playSound(null, player.getX(), player.getY(), player.getZ(), SoundEvents.PLAYER_ATTACK_SWEEP, SoundSource.PLAYERS, 1.5F, 0.7F);\n\t\t\tlevel.playSound(null, player.getX(), player.getY(), player.getZ(), SoundEvents.LIGHTNING_BOLT_THUNDER, SoundSource.PLAYERS, 0.6F, 1.6F);\n\t\t\tplayer.getCooldowns().addCooldown(stack, cooldownTicks);\n\t\t}\n\t\tplayer.swing(hand);\n\t\treturn InteractionResult.SUCCESS;\n\t}\n}\n', 'src/main/java/com/immortalmod/item/LungeSpearItem.java': 'package com.immortalmod.item;\n\nimport java.util.List;\nimport net.minecraft.core.particles.ParticleTypes;\nimport net.minecraft.server.level.ServerLevel;\nimport net.minecraft.sounds.SoundEvents;\nimport net.minecraft.sounds.SoundSource;\nimport net.minecraft.world.InteractionHand;\nimport net.minecraft.world.InteractionResult;\nimport net.minecraft.world.entity.LivingEntity;\nimport net.minecraft.world.entity.player.Player;\nimport net.minecraft.world.item.Item;\nimport net.minecraft.world.item.ItemStack;\nimport net.minecraft.world.level.Level;\nimport net.minecraft.world.phys.AABB;\nimport net.minecraft.world.phys.Vec3;\n\n/** Spear with long reach (set through attributes) whose right-click is a piercing lunge. */\npublic class LungeSpearItem extends Item {\n\tprivate final float damage;\n\tprivate final double speed;\n\tprivate final int cooldownTicks;\n\n\tpublic LungeSpearItem(Properties properties, float damage, double speed, int cooldownTicks) {\n\t\tsuper(properties);\n\t\tthis.damage = damage;\n\t\tthis.speed = speed;\n\t\tthis.cooldownTicks = cooldownTicks;\n\t}\n\n\t@Override\n\tpublic InteractionResult use(Level level, Player player, InteractionHand hand) {\n\t\tItemStack stack = player.getItemInHand(hand);\n\t\tif (level instanceof ServerLevel serverLevel) {\n\t\t\tVec3 look = player.getLookAngle();\n\t\t\tAABB path = player.getBoundingBox().expandTowards(look.scale(7.0)).inflate(1.0);\n\t\t\tList<LivingEntity> targets = serverLevel.getEntitiesOfClass(LivingEntity.class, path, e -> e != player && e.isAlive() && !e.isAlliedTo(player));\n\t\t\tfor (LivingEntity target : targets) {\n\t\t\t\ttarget.hurtServer(serverLevel, serverLevel.damageSources().playerAttack(player), damage);\n\t\t\t}\n\t\t\tplayer.setDeltaMovement(look.scale(speed));\n\t\t\tplayer.hurtMarked = true;\n\t\t\tfor (int i = 0; i < 12; i++) {\n\t\t\t\tVec3 p = player.position().add(look.scale(i * 0.5)).add(0, 1.0, 0);\n\t\t\t\tserverLevel.sendParticles(ParticleTypes.CRIT, p.x, p.y, p.z, 3, 0.1, 0.1, 0.1, 0.05);\n\t\t\t}\n\t\t\tlevel.playSound(null, player.getX(), player.getY(), player.getZ(), SoundEvents.TRIDENT_RIPTIDE_3, SoundSource.PLAYERS, 1.0F, 1.0F);\n\t\t\tplayer.getCooldowns().addCooldown(stack, cooldownTicks);\n\t\t}\n\t\tplayer.swing(hand);\n\t\treturn InteractionResult.SUCCESS;\n\t}\n}\n', 'src/main/java/com/immortalmod/item/InfinitePearlItem.java': 'package com.immortalmod.item;\n\nimport net.minecraft.server.level.ServerLevel;\nimport net.minecraft.sounds.SoundEvents;\nimport net.minecraft.sounds.SoundSource;\nimport net.minecraft.world.InteractionHand;\nimport net.minecraft.world.InteractionResult;\nimport net.minecraft.world.entity.player.Player;\nimport net.minecraft.world.entity.projectile.Projectile;\nimport net.minecraft.world.entity.projectile.throwableitemprojectile.ThrownEnderpearl;\nimport net.minecraft.world.item.Item;\nimport net.minecraft.world.item.ItemStack;\nimport net.minecraft.world.level.Level;\n\n/** An ender pearl that is never used up and has no cooldown. */\npublic class InfinitePearlItem extends Item {\n\tprivate final float power;\n\n\tpublic InfinitePearlItem(Properties properties, float power) {\n\t\tsuper(properties);\n\t\tthis.power = power;\n\t}\n\n\t@Override\n\tpublic InteractionResult use(Level level, Player player, InteractionHand hand) {\n\t\tItemStack stack = player.getItemInHand(hand);\n\t\tlevel.playSound(null, player.getX(), player.getY(), player.getZ(), SoundEvents.ENDER_PEARL_THROW, SoundSource.NEUTRAL, 0.5F, 0.4F / (level.getRandom().nextFloat() * 0.4F + 0.8F));\n\t\tif (level instanceof ServerLevel serverLevel) {\n\t\t\tProjectile.spawnProjectileFromRotation(ThrownEnderpearl::new, serverLevel, stack.copyWithCount(1), player, 0.0F, power, 1.0F);\n\t\t}\n\t\treturn InteractionResult.SUCCESS; // note: the stack is deliberately NOT shrunk and no cooldown is added\n\t}\n}\n', 'src/main/java/com/immortalmod/item/GoldenFoodItem.java': 'package com.immortalmod.item;\n\nimport java.util.List;\nimport net.minecraft.server.level.ServerLevel;\nimport net.minecraft.world.effect.MobEffectInstance;\nimport net.minecraft.world.entity.LivingEntity;\nimport net.minecraft.world.item.Item;\nimport net.minecraft.world.item.ItemStack;\nimport net.minecraft.world.level.Level;\n\n/** Food that also hands out status effects when eaten. */\npublic class GoldenFoodItem extends Item {\n\tprivate final List<MobEffectInstance> effects;\n\n\tpublic GoldenFoodItem(Properties properties, List<MobEffectInstance> effects) {\n\t\tsuper(properties);\n\t\tthis.effects = effects;\n\t}\n\n\t@Override\n\tpublic ItemStack finishUsingItem(ItemStack stack, Level level, LivingEntity entity) {\n\t\tItemStack result = super.finishUsingItem(stack, level, entity);\n\t\tif (level instanceof ServerLevel) {\n\t\t\tfor (MobEffectInstance effect : effects) {\n\t\t\t\tentity.addEffect(new MobEffectInstance(effect));\n\t\t\t}\n\t\t}\n\t\treturn result;\n\t}\n}\n', 'src/main/resources/fabric.mod.json': '{\n\t"schemaVersion": 1,\n\t"id": "immortal",\n\t"version": "${version}",\n\t"name": "Immortal & Godly",\n\t"description": "Golden food, a bedrock pickaxe, unbreakable Immortal and Godly gear, hearts, flight armour, enchantable sword blocks and purple superhero armour.",\n\t"authors": ["You"],\n\t"license": "CC0-1.0",\n\t"icon": "assets/immortal/icon.png",\n\t"environment": "*",\n\t"entrypoints": {\n\t\t"main": ["com.immortalmod.ImmortalMod"],\n\t\t"client": ["com.immortalmod.client.ImmortalModClient"]\n\t},\n\t"depends": {\n\t\t"fabricloader": ">=0.20.1",\n\t\t"minecraft": "~26.3",\n\t\t"java": ">=25",\n\t\t"fabric-api": "*"\n\t}\n}\n', 'src/client/java/com/immortalmod/client/ImmortalModClient.java': 'package com.immortalmod.client;\n\nimport net.fabricmc.api.ClientModInitializer;\n\npublic class ImmortalModClient implements ClientModInitializer {\n\t@Override\n\tpublic void onInitializeClient() {\n\t\t// Nothing needed on the client: models, textures and names are all resource-pack driven.\n\t}\n}\n'}

for _path, _text in FILES.items():
    os.makedirs(os.path.dirname(_path), exist_ok=True)
    with open(_path, "w") as _f:
        _f.write(_text)
print("wrote", len(FILES), "source files")

# ---------------------------------------------------------------- assets

ROOT = os.path.join(os.getcwd(), "src", "main", "resources")
A = f"{ROOT}/assets/immortal"
D = f"{ROOT}/data"
NS = "immortal"

def w(path, data, raw=False):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(data if raw else json.dumps(data, indent=2))

# ------------------------------------------------------------ palettes
PAL = {
    "iron":      dict(main=(205,205,210), dark=(120,120,128), light=(240,240,245)),
    "diamond":   dict(main=(70,225,215),  dark=(20,130,150),  light=(190,255,250)),
    "netherite": dict(main=(78,70,82),    dark=(35,30,40),    light=(130,120,138)),
    "bedrock":   dict(main=(95,95,95),    dark=(30,30,30),    light=(160,160,160)),
    "galaxy":    dict(main=(60,70,190),   dark=(14,12,60),    light=(140,175,255)),
    "immortal":  dict(main=(150,60,225),  dark=(45,10,95),    light=(235,170,255)),
    "godly":     dict(main=(246,247,255), dark=(165,185,225), light=(255,255,255)),
    "purple":    dict(main=(150,70,200),  dark=(80,30,120),   light=(215,170,245)),
    "gold":      dict(main=(250,200,50),  dark=(185,120,20),  light=(255,245,160)),
}
OUT = (20, 14, 24)
WOOD = (130, 90, 45)
WOOD_D = (85, 55, 25)

def canvas():
    return Image.new("RGBA", (16, 16), (0, 0, 0, 0))

def outline(img):
    px = img.load()
    out = img.copy()
    po = out.load()
    for y in range(16):
        for x in range(16):
            if px[x, y][3] == 0:
                for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    nx, ny = x+dx, y+dy
                    if 0 <= nx < 16 and 0 <= ny < 16 and px[nx, ny][3] > 0:
                        po[x, y] = OUT + (255,)
                        break
    return out

def line(img, pts, color):
    ImageDraw.Draw(img).line(pts, fill=color + (255,))

def px(img, pts, color):
    p = img.load()
    for x, y in pts:
        if 0 <= x < 16 and 0 <= y < 16:
            p[x, y] = color + (255,)

# ------------------------------------------------------------ item icons
def sword(c):
    im = canvas()
    line(im, [(3,12),(11,4)], c["main"]); line(im, [(4,12),(12,4)], c["main"]); line(im, [(3,11),(10,4)], c["light"])
    px(im, [(12,3),(13,2),(12,2),(13,3)], c["light"])
    line(im, [(3,9),(7,13)], c["dark"]); line(im, [(4,9),(7,12)], (190,160,60))
    line(im, [(1,14),(3,12)], WOOD); px(im, [(1,15),(0,14)], WOOD_D)
    return outline(im)

def pickaxe(c):
    im = canvas()
    line(im, [(2,14),(10,6)], WOOD); line(im, [(3,14),(10,7)], WOOD_D)
    for p in [(4,6),(5,4),(7,3),(9,3),(11,4),(12,6),(13,8)]:
        px(im, [p], c["main"]); px(im, [(p[0], p[1]+1)], c["dark"])
    px(im, [(7,2),(8,2),(10,3)], c["light"])
    return outline(im)

def axe(c):
    im = canvas()
    line(im, [(3,14),(11,5)], WOOD); line(im, [(4,14),(11,6)], WOOD_D)
    for (x, y) in [(8,2),(9,2),(10,2),(7,3),(8,3),(9,3),(10,3),(11,3),(7,4),(8,4),(9,4),(10,4),(11,4),(12,4),(8,5),(9,5),(10,5),(12,5)]:
        px(im, [(x, y)], c["main"])
    px(im, [(8,2),(9,2),(7,3),(8,3)], c["light"]); px(im, [(12,4),(12,5),(10,5),(11,4)], c["dark"])
    return outline(im)

def spear(c):
    im = canvas()
    line(im, [(1,14),(12,3)], WOOD); line(im, [(2,14),(12,4)], WOOD_D)
    for p in [(13,2),(14,1),(13,1),(14,2),(12,1),(14,3),(12,2),(13,3),(11,2),(14,0),(15,0)]:
        px(im, [p], c["main"])
    px(im, [(13,2),(14,1),(12,2)], c["light"]); px(im, [(14,3),(13,3),(11,2)], c["dark"])
    return outline(im)

def helmet(c):
    im = canvas()
    for y, (a, b) in zip(range(3, 12), [(5,10),(4,11),(3,12),(3,12),(3,12),(3,12),(3,4),(11,12),(3,4)]):
        for x in range(a, b+1): px(im, [(x, y)], c["main"])
    for x in range(3, 13): px(im, [(x, 4)], c["light"])
    for x in (3,4,11,12): px(im, [(x, 10)], c["dark"]); px(im, [(x, 9)], c["dark"])
    for x in range(5, 11): px(im, [(x, 8)], c["dark"])
    return outline(im)

def chestplate(c):
    im = canvas()
    for y in range(2, 14):
        if y < 5: xs = list(range(1, 5)) + list(range(11, 15))
        else: xs = list(range(3, 13))
        for x in xs: px(im, [(x, y)], c["main"])
    for y in range(5, 14): px(im, [(3, y)], c["light"]); px(im, [(12, y)], c["dark"])
    px(im, [(6,5),(9,5),(7,6),(8,6),(7,8),(8,8),(7,10),(8,10)], c["dark"])
    for x in range(1, 5): px(im, [(x, 2)], c["light"])
    return outline(im)

def leggings(c):
    im = canvas()
    for y in range(2, 14):
        for x in range(3, 13):
            if y > 6 and x in (7, 8): continue
            px(im, [(x, y)], c["main"])
    for y in range(2, 14): px(im, [(3, y)], c["light"]); px(im, [(12, y)], c["dark"])
    for x in range(3, 13): px(im, [(x, 3)], c["dark"])
    return outline(im)

def boots(c):
    im = canvas()
    for y in range(6, 13):
        for x in list(range(2, 6)) + list(range(10, 14)): px(im, [(x, y)], c["main"])
    for x in list(range(2, 7)) + list(range(9, 14)): px(im, [(x, 12)], c["main"]); px(im, [(x, 13)], c["dark"])
    for y in range(6, 13): px(im, [(2, y)], c["light"]); px(im, [(10, y)], c["light"])
    return outline(im)

def pearl(c):
    im = canvas()
    d = ImageDraw.Draw(im)
    d.ellipse([2, 2, 13, 13], fill=c["main"] + (255,))
    d.ellipse([4, 4, 11, 11], fill=c["dark"] + (255,))
    d.ellipse([3, 3, 7, 7], fill=c["light"] + (255,))
    px(im, [(5,5)], (255,255,255)); px(im, [(10,9),(9,10),(10,10)], c["main"])
    return outline(im)

def totem(c):
    im = canvas()
    for y, (a, b) in zip(range(1, 15), [(5,10),(4,11),(3,12),(3,12),(4,11),(5,10),(3,12),(2,13),(5,10),(5,10),(6,9),(6,9),(5,10),(5,10)]):
        for x in range(a, b+1): px(im, [(x, y)], c["main"])
    px(im, [(5,4),(10,4)], (30,30,30)); px(im, [(6,6),(7,6),(8,6),(9,6)], (30,30,30))
    for y in range(1, 15): px(im, [(5, y)], c["light"]) if y in (1,2,7,8) else None
    px(im, [(6,9),(9,9),(7,12),(8,12)], c["dark"])
    return outline(im)

HEART_MASK = ["..XX....XX..", ".XXXX..XXXX.", "XXXXXXXXXXXX", "XXXXXXXXXXXX", "XXXXXXXXXXXX", ".XXXXXXXXXX.", "..XXXXXXXX..", "...XXXXXX...", "....XXXX....", ".....XX....."]
def heart(c):
    im = canvas()
    for y, row in enumerate(HEART_MASK):
        for x, ch in enumerate(row):
            if ch == "X":
                col = c["main"]
                if y < 3 and x < 6: col = c["light"]
                if y > 6: col = c["dark"]
                px(im, [(x + 2, y + 3)], col)
    px(im, [(4,5),(5,5)], (255,255,255))
    return outline(im)

def ingot(c):
    im = canvas()
    for y in range(5, 12):
        for x in range(2 + (11 - y) // 2, 11 + (11 - y) // 2 + 1):
            px(im, [(x, y)], c["main"])
    for x in range(5, 14): px(im, [(x, 5)], c["light"])
    for y in range(6, 12): px(im, [(2 + (11 - y)//2, y)], c["light"])
    for x in range(2, 11): px(im, [(x, 11)], c["dark"])
    px(im, [(8,8),(9,7)], (255,255,255))
    return outline(im)

def apple(c):
    im = canvas()
    d = ImageDraw.Draw(im)
    d.ellipse([2, 4, 13, 14], fill=c["main"] + (255,))
    d.ellipse([3, 5, 7, 9], fill=c["light"] + (255,))
    d.ellipse([9, 9, 13, 14], fill=c["dark"] + (255,))
    px(im, [(8,3),(8,2),(9,1),(10,1),(10,2)], (60,160,60)); px(im, [(7,4),(8,4)], (90,60,30))
    px(im, [(5,6)], (255,255,255))
    return outline(im)

def food_steak(c):
    im = canvas(); d = ImageDraw.Draw(im)
    d.ellipse([1, 3, 14, 13], fill=c["main"] + (255,))
    d.ellipse([3, 5, 12, 11], fill=c["dark"] + (255,))
    d.ellipse([5, 6, 9, 8], fill=c["light"] + (255,))
    px(im, [(12,5),(4,10),(10,10)], c["light"])
    return outline(im)

def food_chop(c):
    im = canvas(); d = ImageDraw.Draw(im)
    d.ellipse([2, 4, 14, 13], fill=c["main"] + (255,))
    d.ellipse([4, 6, 11, 11], fill=c["dark"] + (255,))
    px(im, [(2,13),(1,14),(2,14),(3,14)], c["light"]); px(im, [(6,7),(7,7),(5,8)], c["light"])
    return outline(im)

def food_chicken(c):
    im = canvas(); d = ImageDraw.Draw(im)
    d.ellipse([2, 2, 11, 10], fill=c["main"] + (255,))
    d.ellipse([4, 4, 9, 8], fill=c["dark"] + (255,))
    line(im, [(9,9),(13,13)], c["light"]); px(im, [(13,13),(14,13),(13,14),(14,14)], c["light"])
    px(im, [(4,3),(5,3)], c["light"])
    return outline(im)

def food_fish(c):
    im = canvas()
    d = ImageDraw.Draw(im)
    d.ellipse([2, 4, 12, 11], fill=c["main"] + (255,))
    d.polygon([(11,7),(15,3),(15,12)], fill=c["dark"] + (255,))
    d.ellipse([4, 6, 7, 9], fill=c["light"] + (255,))
    px(im, [(5,6)], (20,20,20)); px(im, [(8,7),(8,8),(9,8)], c["dark"])
    return outline(im)

def food_potato(c):
    im = canvas(); d = ImageDraw.Draw(im)
    d.ellipse([2, 4, 13, 13], fill=c["main"] + (255,))
    d.ellipse([4, 6, 11, 11], fill=c["light"] + (255,))
    px(im, [(5,5),(10,5),(12,9),(3,10)], c["dark"])
    return outline(im)

def food_bread(c):
    im = canvas(); d = ImageDraw.Draw(im)
    d.rounded_rectangle([1, 5, 14, 12], radius=3, fill=c["main"] + (255,))
    d.rounded_rectangle([2, 6, 13, 9], radius=2, fill=c["light"] + (255,))
    for x in (4, 7, 10): line(im, [(x, 6), (x + 1, 9)], c["dark"])
    return outline(im)

ICONS = {}
def add(name, fn, pal): ICONS[name] = fn(PAL[pal])

# food
add("golden_steak", food_steak, "gold"); add("golden_porkchop", food_chop, "gold")
add("golden_chicken", food_chicken, "gold"); add("golden_mutton", food_chop, "gold")
add("golden_rabbit", food_chicken, "gold"); add("golden_cod", food_fish, "gold")
add("golden_salmon", food_fish, "gold"); add("golden_baked_potato", food_potato, "gold")
add("golden_bread", food_bread, "gold")
add("immortal_apple", apple, "immortal"); add("godly_apple", apple, "godly")
add("immortal_ingot", ingot, "immortal"); add("godly_ingot", ingot, "godly")
add("bedrock_pickaxe", pickaxe, "bedrock")
for tier in ("immortal", "godly"):
    add(f"{tier}_pickaxe", pickaxe, tier); add(f"{tier}_axe", axe, tier)
    add(f"{tier}_sword", sword, tier); add(f"{tier}_spear", spear, tier)
    add(f"{tier}_helmet", helmet, tier); add(f"{tier}_chestplate", chestplate, tier)
    add(f"{tier}_leggings", leggings, tier); add(f"{tier}_boots", boots, tier)
    add(f"{tier}_ender_pearl", pearl, tier); add(f"{tier}_totem", totem, tier)
    add(f"{tier}_heart", heart, tier)
add("heart", heart, "purple" if False else "gold")
ICONS["heart"] = heart(dict(main=(225,40,50), dark=(150,15,35), light=(255,130,130)))
add("purple_hero_helmet", helmet, "purple"); add("purple_hero_chestplate", chestplate, "purple")
add("purple_hero_leggings", leggings, "purple"); add("purple_hero_boots", boots, "purple")

STAR = {"galaxy": [(255,255,255),(170,200,255)], "immortal": [(255,255,255),(255,180,255),(120,240,255)], "godly": [(255,225,110),(255,245,170)]}
def sparkle(img, tier, name):
    rnd = random.Random(tier + name)
    p = img.load()
    cells = [(x, y) for y in range(16) for x in range(16) if p[x, y][3] > 0 and p[x, y][:3] != OUT]
    for x, y in rnd.sample(cells, min(len(cells), max(3, len(cells) // 9))):
        p[x, y] = rnd.choice(STAR[tier]) + (255,)

for tier in ("galaxy",):
    add(f"{tier}_pickaxe", pickaxe, tier); add(f"{tier}_axe", axe, tier); add(f"{tier}_sword", sword, tier)
    add(f"{tier}_helmet", helmet, tier); add(f"{tier}_chestplate", chestplate, tier)
    add(f"{tier}_leggings", leggings, tier); add(f"{tier}_boots", boots, tier)
add("galaxy_ingot", ingot, "galaxy")
for _n, _img in ICONS.items():
    for _t in STAR:
        if _n.startswith(_t + "_"):
            sparkle(_img, _t, _n)

HANDHELD = {n for n in ICONS if n.endswith(("_pickaxe", "_axe", "_sword", "_spear"))}

# sword blocks
SWORD_BLOCKS = {"iron": "iron", "diamond": "diamond", "netherite": "netherite", "immortal": "immortal", "godly": "godly"}
def block_texture(tier):
    c = PAL[tier]
    rnd = random.Random(tier)
    base = Image.new("RGBA", (16, 16))
    p = base.load()
    for y in range(16):
        for x in range(16):
            j = rnd.randint(-10, 10)
            col = tuple(max(0, min(255, v + j)) for v in c["dark"])
            p[x, y] = col + (255,)
    d = ImageDraw.Draw(base)
    d.rectangle([0, 0, 15, 15], outline=c["main"] + (255,))
    d.rectangle([1, 1, 14, 14], outline=tuple(int(v*0.7) for v in c["dark"]) + (255,))
    s = sword(c)
    base.alpha_composite(s)
    if tier in STAR:
        pp = base.load()
        for _ in range(10):
            pp[rnd.randint(1, 14), rnd.randint(1, 14)] = rnd.choice(STAR[tier]) + (255,)
    return base

# ------------------------------------------------------------ armour layer textures (64x32)
def armour_layer(tier, layer):
    c = PAL[tier]
    rnd = random.Random(tier + str(layer))
    im = Image.new("RGBA", (64, 32))
    p = im.load()
    for y in range(32):
        for x in range(64):
            band = (x // 4 + y // 4 + layer) % 3
            col = [c["main"], c["dark"], c["light"]][band] if (x + y) % 7 == 0 else c["main"]
            if band == 1: col = tuple(int(v * 0.85) for v in c["main"])
            j = rnd.randint(-8, 8)
            p[x, y] = tuple(max(0, min(255, v + j)) for v in col) + (255,)
    d = ImageDraw.Draw(im)
    for yy in range(0, 32, 8):
        d.line([(0, yy), (63, yy)], fill=(c["dark"] if tier != "godly" else (255, 225, 120)) + (255,))
    if tier in STAR:
        for _ in range(70):
            p[rnd.randint(0, 63), rnd.randint(0, 31)] = rnd.choice(STAR[tier]) + (255,)
    return im

# ------------------------------------------------------------ write textures + models
for name, img in ICONS.items():
    os.makedirs(f"{A}/textures/item", exist_ok=True)
    img.save(f"{A}/textures/item/{name}.png")
    parent = "minecraft:item/handheld" if name in HANDHELD else "minecraft:item/generated"
    w(f"{A}/models/item/{name}.json", {"parent": parent, "textures": {"layer0": f"{NS}:item/{name}"}})
    w(f"{A}/items/{name}.json", {"model": {"type": "minecraft:model", "model": f"{NS}:item/{name}"}})

for tier in SWORD_BLOCKS:
    name = f"{tier}_sword_block"
    os.makedirs(f"{A}/textures/block", exist_ok=True)
    block_texture(tier).save(f"{A}/textures/block/{name}.png")
    w(f"{A}/models/block/{name}.json", {"parent": "minecraft:block/cube_all", "textures": {"all": f"{NS}:block/{name}"}})
    w(f"{A}/blockstates/{name}.json", {"variants": {"": {"model": f"{NS}:block/{name}"}}})
    w(f"{A}/items/{name}.json", {"model": {"type": "minecraft:model", "model": f"{NS}:block/{name}"}})
    w(f"{D}/{NS}/loot_table/blocks/{name}.json", {
        "type": "minecraft:block",
        "pools": [{"rolls": 1, "entries": [{"type": "minecraft:item", "name": f"{NS}:{name}"}],
                   "conditions": [{"condition": "minecraft:survives_explosion"}]}]})

for tier in ("galaxy", "immortal", "godly", "purple"):
    key = "purple_hero" if tier == "purple" else tier
    w(f"{A}/equipment/{key}.json", {"layers": {
        "humanoid": [{"texture": f"{NS}:{key}"}],
        "humanoid_leggings": [{"texture": f"{NS}:{key}"}]}})
    os.makedirs(f"{A}/textures/entity/equipment/humanoid", exist_ok=True)
    os.makedirs(f"{A}/textures/entity/equipment/humanoid_leggings", exist_ok=True)
    armour_layer(tier, 1).save(f"{A}/textures/entity/equipment/humanoid/{key}.png")
    armour_layer(tier, 2).save(f"{A}/textures/entity/equipment/humanoid_leggings/{key}.png")

# mod icon
icon = Image.new("RGBA", (128, 128), (20, 10, 40, 255))
big = sword(PAL["godly"]).resize((128, 128), Image.NEAREST)
icon.alpha_composite(big)
icon.save(f"{A}/icon.png")

# ------------------------------------------------------------ recipes
def shaped(name, pattern, key, result, count=1):
    w(f"{D}/{NS}/recipe/{name}.json", {"type": "minecraft:crafting_shaped", "category": "misc",
        "pattern": pattern, "key": key, "result": {"id": result, "count": count}})
def shapeless(name, ings, result):
    w(f"{D}/{NS}/recipe/{name}.json", {"type": "minecraft:crafting_shapeless", "category": "misc",
        "ingredients": ings, "result": {"id": result, "count": 1}})
def stonecut(name, ing, result):
    w(f"{D}/{NS}/recipe/{name}.json", {"type": "minecraft:stonecutting", "ingredient": ing, "result": {"id": result, "count": 1}})

m = lambda n: f"minecraft:{n}"
i = lambda n: f"{NS}:{n}"

# golden food: 8 gold nuggets around the cooked item
for g, base in [("golden_steak","cooked_beef"),("golden_porkchop","cooked_porkchop"),("golden_chicken","cooked_chicken"),
                ("golden_mutton","cooked_mutton"),("golden_rabbit","cooked_rabbit"),("golden_cod","cooked_cod"),
                ("golden_salmon","cooked_salmon"),("golden_baked_potato","baked_potato"),("golden_bread","bread")]:
    shaped(g, ["###", "#X#", "###"], {"#": m("gold_nugget"), "X": m(base)}, i(g))

# ingots
shaped("galaxy_ingot", ["ALA", "LDL", "ALA"], {"A": m("amethyst_block"), "L": m("lapis_block"), "D": m("diamond")}, i("galaxy_ingot"))
shaped("galaxy_pickaxe", ["III", " S ", " S "], {"I": i("galaxy_ingot"), "S": m("stick")}, i("galaxy_pickaxe"))
shaped("galaxy_axe", ["II", "IS", " S"], {"I": i("galaxy_ingot"), "S": m("stick")}, i("galaxy_axe"))
shaped("galaxy_sword", ["I", "I", "S"], {"I": i("galaxy_ingot"), "S": m("stick")}, i("galaxy_sword"))
shaped("galaxy_helmet", ["III", "I I"], {"I": i("galaxy_ingot")}, i("galaxy_helmet"))
shaped("galaxy_chestplate", ["I I", "III", "III"], {"I": i("galaxy_ingot")}, i("galaxy_chestplate"))
shaped("galaxy_leggings", ["III", "I I", "I I"], {"I": i("galaxy_ingot")}, i("galaxy_leggings"))
shaped("galaxy_boots", ["I I", "I I"], {"I": i("galaxy_ingot")}, i("galaxy_boots"))
shaped("immortal_ingot", ["NGN", "GSG", "NGN"], {"N": m("netherite_ingot"), "G": i("galaxy_ingot"), "S": m("nether_star")}, i("immortal_ingot"))
shaped("godly_ingot", ["IEI", "ESE", "IEI"], {"I": i("immortal_ingot"), "E": m("enchanted_golden_apple"), "S": m("nether_star")}, i("godly_ingot"))
shapeless("immortal_apple", [m("enchanted_golden_apple"), i("immortal_ingot")], i("immortal_apple"))
shapeless("godly_apple", [i("immortal_apple"), i("godly_ingot")], i("godly_apple"))

# bedrock pickaxe (upgrade of a netherite pickaxe)
shaped("bedrock_pickaxe", ["ONO", "NPN", "ONO"], {"O": m("obsidian"), "N": m("netherite_ingot"), "P": m("netherite_pickaxe")}, i("bedrock_pickaxe"))

for tier in ("immortal", "godly"):
    ing = i(f"{tier}_ingot")
    stick = {"immortal": m("blaze_rod"), "godly": m("end_rod")}[tier]
    shaped(f"{tier}_pickaxe", ["III", " S ", " S "], {"I": ing, "S": stick}, i(f"{tier}_pickaxe"))
    shaped(f"{tier}_axe", ["II", "IS", " S"], {"I": ing, "S": stick}, i(f"{tier}_axe"))
    shaped(f"{tier}_sword", ["I", "I", "S"], {"I": ing, "S": stick}, i(f"{tier}_sword"))
    shaped(f"{tier}_spear", ["  I", " S ", "S  "], {"I": ing, "S": stick}, i(f"{tier}_spear"))
    shaped(f"{tier}_helmet", ["III", "I I"], {"I": ing}, i(f"{tier}_helmet"))
    shaped(f"{tier}_chestplate", ["I I", "III", "III"], {"I": ing}, i(f"{tier}_chestplate"))
    shaped(f"{tier}_leggings", ["III", "I I", "I I"], {"I": ing}, i(f"{tier}_leggings"))
    shaped(f"{tier}_boots", ["I I", "I I"], {"I": ing}, i(f"{tier}_boots"))

shaped("immortal_ender_pearl", ["PPP", "PIP", "PPP"], {"P": m("ender_pearl"), "I": i("immortal_ingot")}, i("immortal_ender_pearl"))
shaped("godly_ender_pearl", ["EEE", "EIE", "EEE"], {"E": m("ender_eye"), "I": i("godly_ingot")}, i("godly_ender_pearl"))
shaped("immortal_totem", ["GIG", "ITI", "GIG"], {"G": m("gold_block"), "I": i("immortal_ingot"), "T": m("totem_of_undying")}, i("immortal_totem"))
shaped("godly_totem", ["EGE", "GTG", "EGE"], {"E": m("emerald_block"), "G": i("godly_ingot"), "T": i("immortal_totem")}, i("godly_totem"))
shaped("heart", ["DRD", "RAR", "DRD"], {"D": m("diamond"), "R": m("redstone_block"), "A": m("golden_apple")}, i("heart"))
shaped("immortal_heart", ["GHG", "HIH", "GHG"], {"G": m("gold_block"), "H": i("heart"), "I": i("immortal_ingot")}, i("immortal_heart"))
shaped("godly_heart", ["EHE", "HGH", "EHE"], {"E": m("emerald_block"), "H": i("immortal_heart"), "G": i("godly_ingot")}, i("godly_heart"))

# purple superhero armour (amethyst shards)
A_ = {"A": m("amethyst_shard")}
shaped("purple_hero_helmet", ["AAA", "A A"], A_, i("purple_hero_helmet"))
shaped("purple_hero_chestplate", ["A A", "AAA", "AAA"], A_, i("purple_hero_chestplate"))
shaped("purple_hero_leggings", ["AAA", "A A", "A A"], A_, i("purple_hero_leggings"))
shaped("purple_hero_boots", ["A A", "A A"], A_, i("purple_hero_boots"))

# sword blocks via stonecutter
stonecut("iron_sword_block", m("iron_block"), i("iron_sword_block"))
stonecut("diamond_sword_block", m("diamond_block"), i("diamond_sword_block"))
stonecut("netherite_sword_block", m("netherite_block"), i("netherite_sword_block"))
stonecut("immortal_sword_block", i("immortal_ingot"), i("immortal_sword_block"))
stonecut("godly_sword_block", i("godly_ingot"), i("godly_sword_block"))

# ------------------------------------------------------------ tags
def tag(path, values):
    w(f"{D}/minecraft/tags/{path}.json", {"replace": False, "values": values})

sw = [i(f"{t}_sword_block") for t in SWORD_BLOCKS] + [i("galaxy_sword"), i("immortal_sword"), i("godly_sword")]
tag("item/swords", sw)
for t in ("enchantable/sword", "enchantable/sharp_weapon", "enchantable/fire_aspect", "enchantable/melee_weapon", "enchantable/weapon", "enchantable/sweeping", "enchantable/vanishing"):
    tag(f"item/{t}", sw)
spears = [i("immortal_spear"), i("godly_spear")]
for t in ("enchantable/sharp_weapon", "enchantable/melee_weapon", "enchantable/weapon", "enchantable/fire_aspect"):
    pass
w(f"{D}/minecraft/tags/item/enchantable/spear_extra.json", {"replace": False, "values": spears}) if False else None
# add spears into the weapon tags too (second pass merges in the same file)
for t in ("enchantable/sharp_weapon", "enchantable/melee_weapon", "enchantable/weapon", "enchantable/fire_aspect", "enchantable/vanishing"):
    tag(f"item/{t}", sw + spears)
picks = [i("bedrock_pickaxe"), i("galaxy_pickaxe"), i("immortal_pickaxe"), i("godly_pickaxe")]
axes_ = [i("galaxy_axe"), i("immortal_axe"), i("godly_axe")]
tag("item/pickaxes", picks); tag("item/axes", axes_)
for t in ("enchantable/mining", "enchantable/mining_loot", "enchantable/vanishing"):
    tag(f"item/{t}", picks + axes_ + (sw if t == "enchantable/vanishing" else []) + (spears if t == "enchantable/vanishing" else []))
heads = [i("immortal_helmet"), i("godly_helmet"), i("purple_hero_helmet"), i("galaxy_helmet")]
chests = [i("immortal_chestplate"), i("godly_chestplate"), i("purple_hero_chestplate"), i("galaxy_chestplate")]
legs = [i("immortal_leggings"), i("godly_leggings"), i("purple_hero_leggings"), i("galaxy_leggings")]
feet = [i("immortal_boots"), i("godly_boots"), i("purple_hero_boots"), i("galaxy_boots")]
tag("item/head_armor", heads); tag("item/chest_armor", chests); tag("item/leg_armor", legs); tag("item/foot_armor", feet)
tag("item/enchantable/head_armor", heads); tag("item/enchantable/chest_armor", chests)
tag("item/enchantable/leg_armor", legs); tag("item/enchantable/foot_armor", feet)
tag("item/enchantable/armor", heads + chests + legs + feet)
tag("item/enchantable/equippable", heads + chests + legs + feet)
# durability only matters for the breakable stuff: sword blocks (iron/diamond/netherite) and purple hero armour
tag("item/enchantable/durability", [i("iron_sword_block"), i("diamond_sword_block"), i("netherite_sword_block")] + heads[2:] + chests[2:] + legs[2:] + feet[2:] + [i("galaxy_sword"), i("galaxy_pickaxe"), i("galaxy_axe")])
tag("block/mineable/pickaxe", [i(f"{t}_sword_block") for t in SWORD_BLOCKS])

# ------------------------------------------------------------ language
NAMES = {
 "itemGroup.immortal": "Immortal & Godly",
 "item.immortal.immortal_ingot": "Immortal Ingot", "item.immortal.godly_ingot": "Godly Ingot",
 "item.immortal.golden_steak": "Golden Steak", "item.immortal.golden_porkchop": "Golden Porkchop",
 "item.immortal.golden_chicken": "Golden Chicken", "item.immortal.golden_mutton": "Golden Mutton",
 "item.immortal.golden_rabbit": "Golden Rabbit", "item.immortal.golden_cod": "Golden Cod",
 "item.immortal.golden_salmon": "Golden Salmon", "item.immortal.golden_baked_potato": "Golden Baked Potato",
 "item.immortal.golden_bread": "Golden Bread",
 "item.immortal.immortal_apple": "Immortal Apple", "item.immortal.godly_apple": "Godly Apple",
 "item.immortal.bedrock_pickaxe": "Bedrock Pickaxe",
 "item.immortal.heart": "Heart",
}
for tier, T in (("immortal", "Immortal"), ("godly", "Godly")):
    for k, v in (("pickaxe","Pickaxe"),("axe","Axe"),("sword","Sword"),("spear","Spear"),("helmet","Helmet"),
                 ("chestplate","Chestplate"),("leggings","Leggings"),("boots","Boots"),("ender_pearl","Ender Pearl"),
                 ("totem","Totem"),("heart","Heart")):
        NAMES[f"item.immortal.{tier}_{k}"] = f"{T} {v}"
NAMES["item.immortal.galaxy_ingot"] = "Galaxy Ingot"
for k, v in (("pickaxe","Pickaxe"),("axe","Axe"),("sword","Sword"),("helmet","Helmet"),("chestplate","Chestplate"),("leggings","Leggings"),("boots","Boots")):
    NAMES[f"item.immortal.galaxy_{k}"] = f"Galaxy {v}"
for k, v in (("helmet","Helmet"),("chestplate","Chestplate"),("leggings","Leggings"),("boots","Boots")):
    NAMES[f"item.immortal.purple_hero_{k}"] = f"Purple Hero {v}"
for t in SWORD_BLOCKS:
    NAMES[f"block.immortal.{t}_sword_block"] = f"{t.capitalize()} Sword Block"
w(f"{A}/lang/en_us.json", NAMES)
print("icons:", len(ICONS), "lang:", len(NAMES))
