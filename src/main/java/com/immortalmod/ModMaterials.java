package com.immortalmod;

import java.util.Map;
import net.minecraft.resources.ResourceKey;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.tags.BlockTags;
import net.minecraft.tags.ItemTags;
import net.minecraft.world.item.ToolMaterial;
import net.minecraft.world.item.equipment.ArmorMaterial;
import net.minecraft.world.item.equipment.ArmorType;
import net.minecraft.world.item.equipment.EquipmentAsset;
import net.minecraft.world.item.equipment.EquipmentAssets;

public final class ModMaterials {
	// ToolMaterial(incorrectBlocksTag, durability, miningSpeed, attackDamageBonus, enchantability, repairTag)
	public static final ToolMaterial BEDROCK_TOOLS = new ToolMaterial(BlockTags.INCORRECT_FOR_NETHERITE_TOOL, 5000, 30.0F, 4.0F, 25, ItemTags.NETHERITE_TOOL_MATERIALS);
	public static final ToolMaterial GALAXY_TOOLS = new ToolMaterial(BlockTags.INCORRECT_FOR_DIAMOND_TOOL, 2500, 12.0F, 5.0F, 22, ItemTags.DIAMOND_TOOL_MATERIALS);
	public static final ToolMaterial IMMORTAL_TOOLS = new ToolMaterial(BlockTags.INCORRECT_FOR_NETHERITE_TOOL, 5000, 35.0F, 8.0F, 30, ItemTags.NETHERITE_TOOL_MATERIALS);
	public static final ToolMaterial GODLY_TOOLS = new ToolMaterial(BlockTags.INCORRECT_FOR_NETHERITE_TOOL, 9999, 120.0F, 20.0F, 40, ItemTags.NETHERITE_TOOL_MATERIALS);

	// ArmorMaterial(durability, defense, enchantability, equipSound, toughness, knockbackResistance, repairTag, assetId)
	public static final ArmorMaterial GALAXY_ARMOR = new ArmorMaterial(
			35,
			Map.of(ArmorType.BOOTS, 2, ArmorType.LEGGINGS, 5, ArmorType.CHESTPLATE, 7, ArmorType.HELMET, 2, ArmorType.BODY, 9),
			22, SoundEvents.ARMOR_EQUIP_DIAMOND, 1.0F, 0.0F,
			ItemTags.REPAIRS_DIAMOND_ARMOR, asset("galaxy"));

	public static final ArmorMaterial IMMORTAL_ARMOR = new ArmorMaterial(
			100,
			Map.of(ArmorType.BOOTS, 4, ArmorType.LEGGINGS, 8, ArmorType.CHESTPLATE, 10, ArmorType.HELMET, 4, ArmorType.BODY, 12),
			30, SoundEvents.ARMOR_EQUIP_NETHERITE, 6.0F, 0.2F,
			ItemTags.REPAIRS_NETHERITE_ARMOR, asset("immortal"));

	public static final ArmorMaterial GODLY_ARMOR = new ArmorMaterial(
			100,
			Map.of(ArmorType.BOOTS, 5, ArmorType.LEGGINGS, 10, ArmorType.CHESTPLATE, 12, ArmorType.HELMET, 5, ArmorType.BODY, 15),
			40, SoundEvents.ARMOR_EQUIP_NETHERITE, 10.0F, 0.5F,
			ItemTags.REPAIRS_NETHERITE_ARMOR, asset("godly"));

	public static final ArmorMaterial PURPLE_HERO_ARMOR = new ArmorMaterial(
			40,
			Map.of(ArmorType.BOOTS, 3, ArmorType.LEGGINGS, 6, ArmorType.CHESTPLATE, 8, ArmorType.HELMET, 3, ArmorType.BODY, 11),
			25, SoundEvents.ARMOR_EQUIP_IRON, 2.0F, 0.0F,
			ItemTags.REPAIRS_DIAMOND_ARMOR, asset("purple_hero"));

	private ModMaterials() {
	}

	private static ResourceKey<EquipmentAsset> asset(String name) {
		return ResourceKey.create(EquipmentAssets.ROOT_ID, ImmortalMod.id(name));
	}
}
