package com.immortalmod;

import com.immortalmod.item.GoldenFoodItem;
import com.immortalmod.item.HeartItem;
import com.immortalmod.item.InfinitePearlItem;
import com.immortalmod.item.LungeSpearItem;
import com.immortalmod.item.SlashSwordItem;
import java.util.ArrayList;
import java.util.List;
import java.util.function.Function;
import net.minecraft.core.Registry;
import net.minecraft.core.component.DataComponents;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceKey;
import net.minecraft.util.Unit;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EquipmentSlotGroup;
import net.minecraft.world.entity.ai.attributes.AttributeModifier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.food.FoodProperties;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.Rarity;
import net.minecraft.world.item.ToolMaterial;
import net.minecraft.world.item.component.ItemAttributeModifiers;
import net.minecraft.world.item.component.ItemLore;
import net.minecraft.world.item.equipment.ArmorType;
import net.minecraft.world.level.block.Block;

public final class ModItems {
	/** Everything we register, in order, for the creative tab. */
	public static final List<Item> ALL = new ArrayList<>();

	// ---- materials ----
	public static final Item IMMORTAL_INGOT = simple("immortal_ingot", p -> p.rarity(Rarity.EPIC).fireResistant().component(DataComponents.ENCHANTMENT_GLINT_OVERRIDE, true));
	public static final Item GODLY_INGOT = simple("godly_ingot", p -> p.rarity(Rarity.EPIC).fireResistant().component(DataComponents.ENCHANTMENT_GLINT_OVERRIDE, true));

	// ---- golden cooked food ----
	public static final Item GOLDEN_STEAK = food("golden_steak", 10, 1.2F);
	public static final Item GOLDEN_PORKCHOP = food("golden_porkchop", 10, 1.2F);
	public static final Item GOLDEN_CHICKEN = food("golden_chicken", 8, 1.0F);
	public static final Item GOLDEN_MUTTON = food("golden_mutton", 8, 1.0F);
	public static final Item GOLDEN_RABBIT = food("golden_rabbit", 7, 1.0F);
	public static final Item GOLDEN_COD = food("golden_cod", 7, 1.0F);
	public static final Item GOLDEN_SALMON = food("golden_salmon", 8, 1.0F);
	public static final Item GOLDEN_BAKED_POTATO = food("golden_baked_potato", 7, 1.0F);
	public static final Item GOLDEN_BREAD = food("golden_bread", 6, 1.0F);

	// ---- power apples (instant full food, big effects) ----
	public static final Item IMMORTAL_APPLE = apple("immortal_apple", Rarity.EPIC, List.of(
			new MobEffectInstance(MobEffects.REGENERATION, 20 * 30, 3),
			new MobEffectInstance(MobEffects.ABSORPTION, 20 * 120, 4),
			new MobEffectInstance(MobEffects.RESISTANCE, 20 * 60, 2),
			new MobEffectInstance(MobEffects.FIRE_RESISTANCE, 20 * 120, 0)));
	public static final Item GODLY_APPLE = apple("godly_apple", Rarity.EPIC, List.of(
			new MobEffectInstance(MobEffects.REGENERATION, 20 * 60, 4),
			new MobEffectInstance(MobEffects.ABSORPTION, 20 * 300, 9),
			new MobEffectInstance(MobEffects.RESISTANCE, 20 * 120, 3),
			new MobEffectInstance(MobEffects.FIRE_RESISTANCE, 20 * 300, 0),
			new MobEffectInstance(MobEffects.STRENGTH, 20 * 120, 2),
			new MobEffectInstance(MobEffects.SPEED, 20 * 120, 1)));

	// ---- galaxy gear (lowest tier, breakable) ----
	public static final Item GALAXY_INGOT = simple("galaxy_ingot", p -> p.rarity(Rarity.UNCOMMON));
	public static final Item GALAXY_PICKAXE = register("galaxy_pickaxe", Item::new,
			base("galaxy_pickaxe").pickaxe(ModMaterials.GALAXY_TOOLS, 1.0F, -2.8F).rarity(Rarity.UNCOMMON));
	public static final Item GALAXY_AXE = register("galaxy_axe", Item::new,
			base("galaxy_axe").axe(ModMaterials.GALAXY_TOOLS, 5.0F, -3.0F).rarity(Rarity.UNCOMMON));
	public static final Item GALAXY_SWORD = register("galaxy_sword", Item::new,
			base("galaxy_sword").sword(ModMaterials.GALAXY_TOOLS, 3.0F, -2.4F).rarity(Rarity.UNCOMMON));
	public static final Item GALAXY_HELMET = armor("galaxy_helmet", ModMaterials.GALAXY_ARMOR, ArmorType.HELMET, Rarity.UNCOMMON, "Wear all 4: Speed, Night Vision");
	public static final Item GALAXY_CHESTPLATE = armor("galaxy_chestplate", ModMaterials.GALAXY_ARMOR, ArmorType.CHESTPLATE, Rarity.UNCOMMON, "Wear all 4: Speed, Night Vision");
	public static final Item GALAXY_LEGGINGS = armor("galaxy_leggings", ModMaterials.GALAXY_ARMOR, ArmorType.LEGGINGS, Rarity.UNCOMMON, "Wear all 4: Speed, Night Vision");
	public static final Item GALAXY_BOOTS = armor("galaxy_boots", ModMaterials.GALAXY_ARMOR, ArmorType.BOOTS, Rarity.UNCOMMON, "Wear all 4: Speed, Night Vision");

	// ---- bedrock pickaxe ----
	public static final Item BEDROCK_PICKAXE = register("bedrock_pickaxe", Item::new, unbreakable(
			base("bedrock_pickaxe").pickaxe(ModMaterials.BEDROCK_TOOLS, 1.0F, -2.8F).rarity(Rarity.EPIC).fireResistant()));

	// ---- immortal gear ----
	public static final Item IMMORTAL_PICKAXE = register("immortal_pickaxe", Item::new, unbreakable(
			base("immortal_pickaxe").pickaxe(ModMaterials.IMMORTAL_TOOLS, 1.0F, -2.8F).rarity(Rarity.EPIC).fireResistant()));
	public static final Item IMMORTAL_AXE = register("immortal_axe", Item::new, unbreakable(
			base("immortal_axe").axe(ModMaterials.IMMORTAL_TOOLS, 5.0F, -3.0F).rarity(Rarity.EPIC).fireResistant()));
	public static final Item IMMORTAL_SWORD = register("immortal_sword",
			p -> new SlashSwordItem(p, 6.0, 20.0F, 100, 1.4),
			unbreakable(base("immortal_sword").sword(ModMaterials.IMMORTAL_TOOLS, 3.0F, -2.4F).rarity(Rarity.EPIC).fireResistant()));
	public static final Item IMMORTAL_SPEAR = register("immortal_spear",
			p -> new LungeSpearItem(p, 24.0F, 2.2, 60),
			unbreakable(base("immortal_spear").component(DataComponents.ATTRIBUTE_MODIFIERS, spearAttributes("immortal", 13.0, 3.0)).enchantable(30).rarity(Rarity.EPIC).fireResistant()));
	public static final Item IMMORTAL_HELMET = armor("immortal_helmet", ModMaterials.IMMORTAL_ARMOR, ArmorType.HELMET, Rarity.EPIC, "Wear all 4: Resistance, Strength, Fire Resistance, Night Vision");
	public static final Item IMMORTAL_CHESTPLATE = armor("immortal_chestplate", ModMaterials.IMMORTAL_ARMOR, ArmorType.CHESTPLATE, Rarity.EPIC, "Wear all 4: Resistance, Strength, Fire Resistance, Night Vision");
	public static final Item IMMORTAL_LEGGINGS = armor("immortal_leggings", ModMaterials.IMMORTAL_ARMOR, ArmorType.LEGGINGS, Rarity.EPIC, "Wear all 4: Resistance, Strength, Fire Resistance, Night Vision");
	public static final Item IMMORTAL_BOOTS = armor("immortal_boots", ModMaterials.IMMORTAL_ARMOR, ArmorType.BOOTS, Rarity.EPIC, "Wear all 4: Resistance, Strength, Fire Resistance, Night Vision");
	public static final Item IMMORTAL_ENDER_PEARL = register("immortal_ender_pearl",
			p -> new InfinitePearlItem(p, 1.5F),
			base("immortal_ender_pearl").rarity(Rarity.EPIC).fireResistant().component(DataComponents.ENCHANTMENT_GLINT_OVERRIDE, true));
	public static final Item IMMORTAL_TOTEM = simple("immortal_totem", p -> p.rarity(Rarity.EPIC).fireResistant().stacksTo(1));
	public static final Item HEART = register("heart", p -> new HeartItem(p, ModAttachments.NORMAL_HEARTS, 1),
			base("heart").rarity(Rarity.RARE));
	public static final Item IMMORTAL_HEART = register("immortal_heart", p -> new HeartItem(p, ModAttachments.IMMORTAL_HEARTS, 5),
			base("immortal_heart").rarity(Rarity.EPIC).fireResistant().component(DataComponents.ENCHANTMENT_GLINT_OVERRIDE, true));

	// ---- godly gear ----
	public static final Item GODLY_PICKAXE = register("godly_pickaxe", Item::new, unbreakable(
			base("godly_pickaxe").pickaxe(ModMaterials.GODLY_TOOLS, 1.0F, -2.8F).rarity(Rarity.EPIC).fireResistant()
					.component(DataComponents.ENCHANTMENT_GLINT_OVERRIDE, true)));
	public static final Item GODLY_AXE = register("godly_axe", Item::new, unbreakable(
			base("godly_axe").axe(ModMaterials.GODLY_TOOLS, 5.0F, -3.0F).rarity(Rarity.EPIC).fireResistant()
					.component(DataComponents.ENCHANTMENT_GLINT_OVERRIDE, true)));
	public static final Item GODLY_SWORD = register("godly_sword",
			p -> new SlashSwordItem(p, 12.0, 60.0F, 60, 2.2),
			unbreakable(base("godly_sword").sword(ModMaterials.GODLY_TOOLS, 3.0F, -2.4F).rarity(Rarity.EPIC).fireResistant()
					.component(DataComponents.ENCHANTMENT_GLINT_OVERRIDE, true)));
	public static final Item GODLY_SPEAR = register("godly_spear",
			p -> new LungeSpearItem(p, 70.0F, 3.0, 40),
			unbreakable(base("godly_spear").component(DataComponents.ATTRIBUTE_MODIFIERS, spearAttributes("godly", 30.0, 5.0)).enchantable(40).rarity(Rarity.EPIC).fireResistant()
					.component(DataComponents.ENCHANTMENT_GLINT_OVERRIDE, true)));
	public static final Item GODLY_HELMET = armor("godly_helmet", ModMaterials.GODLY_ARMOR, ArmorType.HELMET, Rarity.EPIC, "Wear all 4: FLY, no fall damage, god-tier buffs");
	public static final Item GODLY_CHESTPLATE = armor("godly_chestplate", ModMaterials.GODLY_ARMOR, ArmorType.CHESTPLATE, Rarity.EPIC, "Wear all 4: FLY, no fall damage, god-tier buffs");
	public static final Item GODLY_LEGGINGS = armor("godly_leggings", ModMaterials.GODLY_ARMOR, ArmorType.LEGGINGS, Rarity.EPIC, "Wear all 4: FLY, no fall damage, god-tier buffs");
	public static final Item GODLY_BOOTS = armor("godly_boots", ModMaterials.GODLY_ARMOR, ArmorType.BOOTS, Rarity.EPIC, "Wear all 4: FLY, no fall damage, god-tier buffs");
	public static final Item GODLY_ENDER_PEARL = register("godly_ender_pearl",
			p -> new InfinitePearlItem(p, 3.0F),
			base("godly_ender_pearl").rarity(Rarity.EPIC).fireResistant().component(DataComponents.ENCHANTMENT_GLINT_OVERRIDE, true));
	public static final Item GODLY_TOTEM = simple("godly_totem", p -> p.rarity(Rarity.EPIC).fireResistant().stacksTo(1)
			.component(DataComponents.ENCHANTMENT_GLINT_OVERRIDE, true));
	public static final Item GODLY_HEART = register("godly_heart", p -> new HeartItem(p, ModAttachments.GODLY_HEARTS, 10),
			base("godly_heart").rarity(Rarity.EPIC).fireResistant().component(DataComponents.ENCHANTMENT_GLINT_OVERRIDE, true));

	// ---- purple superhero armour ----
	public static final Item PURPLE_HERO_CHESTPLATE = armor("purple_hero_chestplate", ModMaterials.PURPLE_HERO_ARMOR, ArmorType.CHESTPLATE, Rarity.RARE, "Wear all 4: Speed, Jump Boost, Strength");

	// ---- enchantable sword blocks (made in the stonecutter) ----
	public static final Item IRON_SWORD_BLOCK = swordBlock("iron_sword_block", ModBlocks.IRON_SWORD_BLOCK, net.minecraft.world.item.ToolMaterial.IRON, false);
	public static final Item DIAMOND_SWORD_BLOCK = swordBlock("diamond_sword_block", ModBlocks.DIAMOND_SWORD_BLOCK, net.minecraft.world.item.ToolMaterial.DIAMOND, false);
	public static final Item NETHERITE_SWORD_BLOCK = swordBlock("netherite_sword_block", ModBlocks.NETHERITE_SWORD_BLOCK, net.minecraft.world.item.ToolMaterial.NETHERITE, false);
	public static final Item IMMORTAL_SWORD_BLOCK = swordBlock("immortal_sword_block", ModBlocks.IMMORTAL_SWORD_BLOCK, ModMaterials.IMMORTAL_TOOLS, true);
	public static final Item GODLY_SWORD_BLOCK = swordBlock("godly_sword_block", ModBlocks.GODLY_SWORD_BLOCK, ModMaterials.GODLY_TOOLS, true);

	// ---- animated set blocks ----
	public static final Item GALAXY_BLOCK = setBlock("galaxy_block", ModBlocks.GALAXY_BLOCK, Rarity.UNCOMMON);
	public static final Item IMMORTAL_BLOCK = setBlock("immortal_block", ModBlocks.IMMORTAL_BLOCK, Rarity.EPIC);
	public static final Item GODLY_BLOCK = setBlock("godly_block", ModBlocks.GODLY_BLOCK, Rarity.EPIC);

	// ---- End ores ----
	public static final Item GALAXY_ORE = setBlock("galaxy_ore", ModBlocks.GALAXY_ORE, Rarity.UNCOMMON);
	public static final Item IMMORTAL_ORE = setBlock("immortal_ore", ModBlocks.IMMORTAL_ORE, Rarity.EPIC);
	public static final Item GODLY_ORE = setBlock("godly_ore", ModBlocks.GODLY_ORE, Rarity.EPIC);

	private ModItems() {
	}

	public static void init() {
	}

	// ------------------------------------------------------------------ helpers

	private static ResourceKey<Item> key(String name) {
		return ResourceKey.create(Registries.ITEM, ImmortalMod.id(name));
	}

	private static Item.Properties base(String name) {
		return new Item.Properties().setId(key(name));
	}

	private static Item.Properties unbreakable(Item.Properties p) {
		return p.component(DataComponents.UNBREAKABLE, Unit.INSTANCE);
	}

	private static ItemLore lore(String... lines) {
		List<Component> list = new ArrayList<>();
		for (String line : lines) {
			list.add(Component.literal(line));
		}
		return new ItemLore(list);
	}

	private static <T extends Item> T register(String name, Function<Item.Properties, T> factory, Item.Properties properties) {
		T item = Registry.register(BuiltInRegistries.ITEM, key(name), factory.apply(properties));
		ALL.add(item);
		return item;
	}

	private static Item simple(String name, Function<Item.Properties, Item.Properties> customiser) {
		return register(name, Item::new, customiser.apply(base(name)));
	}

	private static Item food(String name, int nutrition, float saturation) {
		FoodProperties food = new FoodProperties.Builder().nutrition(nutrition).saturationModifier(saturation).alwaysEdible().build();
		return register(name,
				p -> new GoldenFoodItem(p, List.of(
						new MobEffectInstance(MobEffects.REGENERATION, 20 * 5, 1),
						new MobEffectInstance(MobEffects.ABSORPTION, 20 * 60, 1))),
				base(name).food(food).rarity(Rarity.RARE));
	}

	private static Item apple(String name, Rarity rarity, List<MobEffectInstance> effects) {
		FoodProperties food = new FoodProperties.Builder().nutrition(20).saturationModifier(1.0F).alwaysEdible().build();
		return register(name, p -> new GoldenFoodItem(p, effects),
				base(name).food(food).rarity(rarity).fireResistant().component(DataComponents.ENCHANTMENT_GLINT_OVERRIDE, true));
	}

	private static Item armor(String name, net.minecraft.world.item.equipment.ArmorMaterial material, ArmorType slot, Rarity rarity, String loreLine) {
		Item.Properties p = base(name).humanoidArmor(material, slot).rarity(rarity);
		if (material != ModMaterials.PURPLE_HERO_ARMOR && material != ModMaterials.GALAXY_ARMOR) {
			p = unbreakable(p).fireResistant();
		}
		return register(name, Item::new, p);
	}

	private static ItemAttributeModifiers spearAttributes(String tier, double damage, double reach) {
		return ItemAttributeModifiers.builder()
				.add(Attributes.ATTACK_DAMAGE, new AttributeModifier(Item.BASE_ATTACK_DAMAGE_ID, damage, AttributeModifier.Operation.ADD_VALUE), EquipmentSlotGroup.MAINHAND)
				.add(Attributes.ATTACK_SPEED, new AttributeModifier(Item.BASE_ATTACK_SPEED_ID, -2.6, AttributeModifier.Operation.ADD_VALUE), EquipmentSlotGroup.MAINHAND)
				.add(Attributes.ENTITY_INTERACTION_RANGE, new AttributeModifier(ImmortalMod.id(tier + "_spear_reach"), reach, AttributeModifier.Operation.ADD_VALUE), EquipmentSlotGroup.MAINHAND)
				.build();
	}

	private static Item setBlock(String name, Block block, Rarity rarity) {
		Item.Properties p = base(name).useBlockDescriptionPrefix().rarity(rarity);
		BlockItem item = Registry.register(BuiltInRegistries.ITEM, key(name), new BlockItem(block, p));
		ALL.add(item);
		return item;
	}

	private static Item swordBlock(String name, Block block, ToolMaterial material, boolean indestructible) {
		Item.Properties p = base(name).useBlockDescriptionPrefix().sword(material, 3.0F, -2.4F);
		if (indestructible) {
			p = unbreakable(p).fireResistant().rarity(Rarity.EPIC);
		}
		BlockItem item = Registry.register(BuiltInRegistries.ITEM, key(name), new BlockItem(block, p));
		ALL.add(item);
		return item;
	}
}
